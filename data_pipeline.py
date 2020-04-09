import pandas as pd
from pymongo import MongoClient

client = MongoClient()
db = client['rotten_tomatoes']
rating = db['ratings']

def initial_cleaning():
    '''
        Gets data from mongo and puts it into a database. Casts audience and critic scores from an integer to a string.

        Parameters: None
        Returns: None
    '''
    ratings_df = pd.DataFrame(list(rating.find()))
    ratings_df = ratings_df.iloc[:,1:]
    ratings_df['tomatometer']=[int(rating) for rating in ratings_df['tomatometer']]
    ratings_df['audience']=[int(rating) for rating in ratings_df['audience']]

def get_fresh_and_rotten():
    '''
        Adds two columns to dataframe. The columns list whether the critics and audience thought a movie was fresh or rotten.

        Parameters: None
        Returns: None

    '''
    audience_opinions=[]
    critic_opinions=[]
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
    ratings_df['audience_tomatometer'] = audience_opinions
    ratings_df['critic_tomatometer'] = critic_opinions

def create_and_rename_cols():
    '''
        Renames Columns.

        Parameters: None
        Returns: None
    '''
    ratings_df.rename(columns={'tomatometer': 'critic_score', 'date': 'release_date','audience': 'audience_score'},inplace=True)

def add_score_diff():
    '''
       Adds a column of the difference between the critic and audience scores.

       Parameters: None
       Returns: None
    ''' 
    ratings_df['score_difference'] = ratings_df['audience_score'] - ratings_df['critic_score']

def drop_duplicates():
    '''
        Drops duplcates in the dataframe.

        Parameters: None
        Returns: None
    '''
    ratings_df = ratings_df.drop_duplicates().reset_index()
    ratings_df = ratings_df.drop(columns='index')

initial_cleaning()
get_fresh_and_rotten()
create_and_rename_cols()
add_score_diff()
drop_duplicates()