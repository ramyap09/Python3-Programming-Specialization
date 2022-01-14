#!/usr/bin/env python3
"""
Project : OMDB and TasteDive

This program mash up data from two APIs - TasteDive and OMDB - to make movie recommendations.
To avoid problems with rate limits and site accessibility, a cache file ("permanent_cache.txt") is provided with results 
for all the queries we need to make to both OMDB and TasteDive and a special module 'requests_with_caching' is used to 
fetch this data from the cache file.

Input is a list of movie titles.
Output is a sorted list of related movie titles in the descending order of their Rotten Tomato rating 
(5 movie titles for each input movie title, with duplicates removed)

Be sure to use only those queries for which data is present in the cache file. 

"""

import json
import requests_with_caching
#import requests 


def get_movies_from_tastedive(word):
    """
    Input :
    word - A string that is the name of a movie or music artist

    Output :
    Returns a list of 5 TasteDive results (Only movies) that are associated with the input string. 
    """
    baseurl = "https://tastedive.com/api/similar"
    params_diction = {}
    params_diction["limit"] = 5
    params_diction["q"] = word
    params_diction["type"] = "movies"
    #resp = requests.get(baseurl, params=params_diction)
    resp = requests_with_caching.get(baseurl, params=params_diction,permanent_cache_file="permanent_cache.txt")
    #word_ds = resp.json()
    return resp 




def extract_movie_titles(word):
    """
    Inputs :
    word - A string that is the name of a movie or music artist

    Outputs :
    Returns a list of 5 movie names from TasteDive, that are associated with the input string.    
    """
    out = get_movies_from_tastedive(word)
    lst = []
    for i in out["Similar"]["Results"]:
        lst.append(i["Name"])
    return lst




def get_related_titles(lst):
    """
    Inputs :
    lst - A list of movie titles

    Outputs :
    A list of movie titles from TasteDive, related to the input movie titles.    
    """
    newlst = []
    for movie in lst:
        newlst += extract_movie_titles(movie)
    newlst= list(set(newlst))
    return newlst
        
    
    
    
def get_movie_data(movie_name):
    """
    Input :
    movie_name - Name of the movie (string)

    Output :
    returns a dictionary with information about the movie input.    
    """
    baseurl = "http://www.omdbapi.com/"
    params_diction = {}
    params_diction["t"] = movie_name
    params_diction["r"] = "json"
    resp = requests_with_caching.get(baseurl, params=params_diction,permanent_cache_file="permanent_cache.txt")
    return resp


def get_movie_rating(movie_name):
    """
    Input :
    movie_name - Name of a movie (string)

    Output :
    Returns the Rotten Tomato rating of the movie input.
    Returns 0 if movie has no rating in the Rotten Tomato    
    """
    out = get_movie_data(movie_name)
    for dic in out["Ratings"]:
        if dic['Source'] == "Rotten Tomatoes" :
            value = dic['Value']
            value = int(value.rstrip('%'))
            return value 
        else:
            value = 0
    return value




def get_sorted_recommendations(lst):
    """
    Input :
    A list of movie titles.

    Output :
    Returns a sorted list of related movie titles as output, in descending order by their Rotten Tomatoes rating.     
    """
    newlst = get_related_titles(lst)
    rating = {}
    for movie in newlst:
        rating[movie] = get_movie_rating(movie)
    final = sorted(rating.items(), key = lambda x:(x[1],x[0]), reverse=True)
    new = [x[0] for x in final]
    return new

input = ["Bridesmaids", "Sherlock Holmes"]
output = get_sorted_recommendations(input)
print(output)
    



