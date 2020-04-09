import pandas as pd
from pymongo import MongoClient

client = MongoClient()
db = client['rotten_tomatoes']
rating = db['ratings']

ratings_df = pd.DataFrame(list(rating.find()))
ratings_df = ratings_df.iloc[:,1:]

ratings_df['tomatometer']=[int(rating) for rating in ratings_df['tomatometer']]
ratings_df['audience']=[int(rating) for rating in ratings_df['audience']]
audience_opinions=[]
critic_opinions=[]
def get_fresh_and_rotten():
    for value in ratings_df['audience']:
        if value>=60:
            audience_opinions.append('Fresh')
        elif value<60:
            audience_opinions.append('Rotten')
    for value in ratings_df['tomatometer']:
        if value>=60:
            critic_opinions.append('Fresh')
        elif value<60:
            critic_opinions.append('Rotten')

get_fresh_and_rotten()
ratings_df['audience_tomatometer'] = audience_opinions
ratings_df['critic_tomatometer'] = critic_opinions
ratings_df.rename(columns={'tomatometer': 'critic_score', 'date': 'release_date','audience': 'audience_score'},inplace=True)
ratings_df['score_difference'] = ratings_df['audience_score'] - ratings_df['critic_score']