import pandas as pd
from pymongo import MongoClient

client = MongoClient()
db = client['rotten_tomatoes']
rating = db['ratings']

ratings_df = pd.DataFrame(list(rating.find()))
ratings_df = ratings_df.iloc[:,1:]

df['tomatometer']=[int(rating) for rating in df['tomatometer']]
df['audience']=[int(rating) for rating in df['audience']]