import pandas as pd
import ast
import seaborn as sns
import re
import numpy as np
import matplotlib.pyplot as plt
import spacy
from itertools import chain
from collections import Counter

import warnings
warnings.filterwarnings('ignore') # ignore warnings

pd.set_option("display.max_columns", None)
pd.set_option("display.max_colwidth", 50)


ingredients = "x"
name = "x"
cooktime = "x"
preptime = "x"
totaltime = "x"
dish = "All"
searchword = ""

def seeker(df, ingredients, name, cooktime, preptime, totaltime, dish, searchword, calories, carbs, protein):
    filtered = df.copy()
    if ingredients != "x":
        filtered = df[df["ingredients"].str.contains(ingredients, case=False, na=False)]
    if name != "x":
        filtered.dropna(subset="name", inplace=True)
        filtered = filtered[filtered["name"].str.contains(name, case=False, na=False)]
    if cooktime != 0:
        filtered.dropna(subset="cooktime", inplace=True)
        filtered["cooktime"] = filtered["cooktime"].apply(to_minutes)
        filtered = filtered[filtered["cooktime"] <= cooktime]
    if preptime != 0:
        filtered.dropna(subset="preptime", inplace=True)
        filtered["preptime"] = filtered["preptime"].apply(to_minutes)
        filtered = filtered[filtered["preptime"] <= preptime]
    if totaltime != 0:
        filtered.dropna(subset="totaltime", inplace=True)
        filtered["totaltime"] = filtered["totaltime"].apply(to_minutes)
        filtered = filtered[filtered["totaltime"] <= totaltime]
    if dish != "All":
        if dish == "Main Dish":
            dish = "main-dish"
        filtered["check"] = filtered["tags"].apply(lambda x: dish.lower() in str(x).lower())
        filtered = filtered[filtered["check"] == True]
    if searchword != "":
        filtered["check2"] = filtered.applymap(lambda x: searchword.lower() in str(x).lower()).any(axis=1)
        filtered = filtered[filtered["check2"] == True]
    if calories != 0:
        filtered.dropna(subset="calories", inplace=True)
        filtered = filtered[filtered["calories"] <= calories]
    if carbs != 0:
        filtered.dropna(subset="carbohydratecontent", inplace=True)
        filtered = filtered[filtered["carbohydratecontent"] <= carbs]
    if protein != 0:
        filtered.dropna(subset="proteincontent", inplace=True)
        filtered = filtered[filtered["proteincontent"] <= protein]
    
    filtered = filtered.sort_values(by="aggregatedrating", ascending=False)
    return filtered


def to_minutes(x):
    if pd.notnull(x):
        total = 0
        hours = re.search(r"(\d+)H", x)
        if hours:
            total += int(hours.group(1)) * 60
        minutes = re.search(r"(\d+)M", x)
        if minutes:
            total += int(minutes.group(1))
        return total
    return None



