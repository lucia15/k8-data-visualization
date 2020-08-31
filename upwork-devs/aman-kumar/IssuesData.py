# coding: utf-8
#
# Author(s): Aman Kumar
# Contact: aman.kumar@everlytics.io
# Module to return the the final DataFrame
#
# Dependencies: token.json, request, JSON
#
# INPUT: A list of reposetories whose data of whose issues is requires.

# OUTPUT: A pandas DataFrame with the attributes 'created_at', 'state', 'closed_at', 'user.login', 'author_association','title',   'body', 'milestone.title', 'milestone.state', 'project_name', 'project_duration'

# Importing the necessary libraries
def get_issues(repo):
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import requests
    import os
    import json
    import sys
    from pprint import pprint
    import pandas as pd
    from datetime import timedelta
    from pandas.io.json import json_normalize
    import warnings
    warnings.filterwarnings('ignore')
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    
    # Setting current working directory absolute path
    temp = os.getcwd().split('/')
    path = '/'.join(temp[:(len(temp))])
    
    # Reading and initializing the config values
    try:
        with open(path+'/token.json') as file:
            config = json.load(file)
    except Exception:
        print('Config file not found / JSON format wrong in file')
        sys.exit(0)
    
    # Defining the token, params and headers for the requests
    token = os.getenv('GITHUB_TOKEN', config['token'])
    parameters = {"state" : "all",}
    headers = {'Authorization' : f'token {token}'}
    
    # Fetching the issues data in JSON from the respective reposetories and appending them to a list
    data = []
    for i in range(0, len(repo)):
        data.append(requests.get('https://api.github.com/repos/filetrust/'+repo[i]+'/issues', headers = headers, params = parameters).json())
    
    # Normalizing the JSON objects in order to convert them to DataFrames and appending them to another list
    dataframes = []
    for i in range(0, len(data)):
        dataframes.append(json_normalize(data[i], max_level = 1))
    
    # Adding project_name attribite and concatenating the DataFrames in order to get a single DataFrame of all the rows
    for i in range(0, len(dataframes)):
        dataframes[i]['project_name'] = repo[i]
    df = pd.concat(dataframes, ignore_index = True)
    
    # Getting rid of irrelevent columns
    df= df[['created_at', 'state', 'closed_at','user.login','author_association', 'title','body', 'milestone.title','milestone.state','project_name']]
    
    # Extracting the creation and closure dates from the datetime variable created_at and closed_at
    df.created_at = pd.to_datetime(df.created_at).dt.date
    df.closed_at = pd.to_datetime(df.closed_at).dt.date
    
    # Creating a variable project_duration to reflect the total duration of the project in days
    df['project_duration'] = (df.closed_at - df.created_at) + timedelta(days=1)
    
    # Returning the final DataFrame
    return df