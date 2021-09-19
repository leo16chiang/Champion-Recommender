# Use League of Legends API to get match history of a username

import urllib.request
from urllib.request import urlopen
import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

#Riot Games API Key
key = "RGAPI-ced52b64-2200-4651-b293-e1352c0302b4"

#Load Champion Metadata
metadata = pd.read_csv('Champion Metadata.csv', low_memory=False)


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
def get_champion_played(matchid):
    data = urllib.request.urlopen(
        "https://americas.api.riotgames.com/lol/match/v5/matches/" + matchid + "?api_key=" + key).read()
    champplayed = json.loads(data)["info"]


