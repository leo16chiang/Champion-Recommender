# Use League of Legends API to get match history of a username

import urllib.request
from urllib.request import urlopen
import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

#Riot Games API Key
key = "RGAPI-ecc1eb93-5d4e-473e-9c94-830c0774aab5"

#Load Champion Metadata
metadata = pd.read_csv('Champion Metadata.csv', low_memory=False)

tfidf = TfidfVectorizer(stop_words='english')
metadata['Lore'] = metadata['Lore'].fillna('')
tfidf_matrix = tfidf.fit_transform(metadata['Lore'])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
indices = pd.Series(metadata.index, index=metadata['Name']).drop_duplicates()

#Get PUUID using Summoner Name:
def get_puuid(username):
    data = urllib.request.urlopen(
        "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + username + "?api_key=" + key).read()
    puuid = json.loads(data)["puuid"]
    return puuid

#Get MatchIDs for past 100 Games using PUUID:
def get_match_history(puuid):
    data = urllib.request.urlopen(
        "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/" + puuid + "/ids?start=0&count=100&api_key=" + key).read()
    matchhistory = json.loads(data)
    return matchhistory

#Get Match Information from MatchID:
def get_champion_played(matchid, puuid):
    index = 0
    data = urllib.request.urlopen(
        "https://americas.api.riotgames.com/lol/match/v5/matches/" + matchid + "?api_key=" + key).read()
    for i in range(10):
        summonernumber = json.loads(data)["metadata"]["participants"][i]
        if summonernumber == puuid:
            index = i
    champplayed = json.loads(data)["info"]["participants"][index]["championName"]
    return champplayed

#Get Total Champion Plays for last 100 games
def total_plays(matchistory, puuid):
    lst = []
    for i in range(matchistory):
        lst = lst + get_champion_played(matchistory[i], puuid)
    return lst

# Recommendation function
def get_recommendations(name, cosine_sim=cosine_sim):
    index = indices[name]
    sim_scores = list(enumerate(cosine_sim[index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    print("The recommended champions for " + name + " are: \n")
    return metadata['Name'].iloc[movie_indices]

def most_common(lst):
    return max(set(lst), key=lst.count)


def main():
    summonername = input("Type in your summoner name: \n")
    puuid = get_puuid(summonername)
    matchhistory = get_match_history(puuid)
    totalplays = total_plays(matchhistory, puuid)
    main = most_common(totalplays)
    print("Your most played champ was: " + main)
    print(get_recommendations(main))

main()