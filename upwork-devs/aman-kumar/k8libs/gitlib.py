# coding: utf-8
#
# Author(s): Aman Kumar
# Contact: aman.kumar@everlytics.io
# Module to return the the final DataFrame
#
# Dependencies: token.json, request, JSON
#
# INPUT: A list of reposetories whose data of whose issues OR PR is requires.

# OUTPUT: 
#        1. A pandas DataFrame of issues OR PR is obtained by get_issues_raw and get_PR_raw respectively.
#        2. Custom visuals of issues OR PR is obtained by get_issues_raw and get_PR_raw respectively.

# Importing the necessary libraries
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
import datetime as dt
from pandas.io.json import json_normalize
import warnings
warnings.filterwarnings('ignore')
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

class Issues:
    
    def get_issues_raw(repo):
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

        #Changign association
        df.author_association.replace({'NONE':'NO ASSOCIATION'}, inplace = True)
        
        # Returning the final DataFrame
        return df
    
    
    def get_issues_inferences(repo, df):
        print('|-----------------------------------------SUMMARY OF ISSUES---------------------------------------|')
        print('Total number of unique Issues:', len(df))
        print('Total number of unique projects:', len(df['project_name'].unique()))
        print('Total number of unique users:', len(df['user.login'].unique()))
        print('First Issue created on:', min(df.created_at))
        print('Last Issue created on:', max(df.created_at))
        print('Average number of issues created per day:', \
              np.round((len(df)/(max(df.created_at) - min(df.created_at)).days), decimals = 3))
        print('Average number of issues created per project:', \
              np.round((len(df)/(len(df['project_name'].unique()))), decimals = 3))
        print('|-------------------------------------------------------------------------------------------------|')
        print('\n')
        print('\n')
        
        print('|-----------------------------------------STATE OF ISSUES-----------------------------------------|')
        sns.set(rc={'figure.figsize':(7,7)})
        labels = 'Open', 'Closed'
        explode = (0, 0.1)
        plt.pie(df.state.value_counts(), explode=explode, colors='GR', labels = labels)
        plt.show()
        print('Number of open issues:', len(df[df.state=='open']))
        print('Number of closed issues:', len(df[df.state=='closed']))
        print('|-------------------------------------------------------------------------------------------------|')
        print('\n')
        print('\n')
        
        print('|-----------------------------------------DURATION OF ISSUES--------------------------------------|')
        sns.set(rc={'figure.figsize':(10,5)})
        sns.countplot((df[(df.state=='closed')].project_duration).dt.days, color='G')
        plt.xlabel('Duration of issue (day(s))')
        plt.ylabel('Count of issue')
        plt.show()
        print('Average duration of a closed issue (days):', np.round(np.mean(df.project_duration.dt.days), decimals=3))
        print('|-------------------------------------------------------------------------------------------------|')
        print('\n')
        print('\n')
        
        print('|------------------------------------SPREAD OF DURATION OF ISSUES---------------------------------|')
        sns.set(rc={'figure.figsize':(10,4)})
        sns.boxplot((df[(df.state=='closed') & (df.project_duration.dt.days>1)].project_duration).dt.days, color='R')
        plt.xlabel('Spread of duration of issue (day(s))')
        plt.show()
        print('Median duration of an issue, not closed on the same day (days):', \
              np.round(np.median(df[(df.state=='closed') & (df.project_duration.dt.days>1)].project_duration.dt.days)\
              ,decimals = 3))
        print('|-------------------------------------------------------------------------------------------------|')
        print('\n')
        print('\n')
        
        print('|-------------------------------------COUNT OF ISSUES BY PROJECTS---------------------------------|')
        sns.set(rc={'figure.figsize':(10,6)})
        sns.countplot(y = df.project_name, palette="Set3")
        plt.xlabel('Count of issue')
        plt.ylabel('Name of project')
        plt.show()
        print('|-------------------------------------------------------------------------------------------------|')
        print('\n')
        print('\n')
        
        print('|------------------------------SPREAD OF DURATION OF ISSUES BY PROJECTS---------------------------|')
        sns.set(rc={'figure.figsize':(8, 6)})
        sns.boxplot(x = df[(df.state=='closed')].project_duration.dt.days, y = df.project_name)
        plt.ylabel('Name of project')
        plt.xlabel('Spread of duration of issue (day(s))')
        plt.show()
        print('|-------------------------------------------------------------------------------------------------|')
        print('\n')
        print('\n')
        
        print('|-----------------------------------------ISSUE COUNT BY USER-------------------------------------|')
        sns.set(rc={'figure.figsize':(10,8)})
        sns.countplot(y = df['user.login'])
        plt.xlabel('Count of issue')
        plt.ylabel('Name of user')
        plt.show()
        print('|-------------------------------------------------------------------------------------------------|')
        print('\n')
        print('\n')
        
        print('|-----------------------------------ISSUE COUNT OF AUTHOR ASSOCIATION------------------------------|')
        sns.set(rc={'figure.figsize':(8,6)})
        sns.countplot(df.author_association)
        plt.xlabel('Type of author association')
        plt.ylabel('Count of issue')
        plt.show()
        
        
    def get_pr_raw(repo):
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

        # Fetching the PR data in JSON from the respective reposetories and appending them to a list
        data = []
        for i in range(0, len(repo)):
            data.append(requests.get('https://api.github.com/repos/filetrust/'+repo[i]+'/pulls', headers = headers, params = parameters).json())

        # Normalizing the JSON objects in order to convert them to DataFrames and appending them to another list
        dataframes = []
        for i in range(0, len(data)):
            dataframes.append(json_normalize(data[i], max_level = 1))

        # Adding project_name attribite and concatenating the DataFrames in order to get a single DataFrame of all the rows
        for i in range(0, len(dataframes)):
            dataframes[i]['project_name'] = repo[i]
        df = pd.concat(dataframes, ignore_index = True)

        # Getting rid of irrelevent columns
        df= df[['number', 'locked', 'created_at', 'updated_at', 'state', 'closed_at','merged_at', 'requested_reviewers', 'labels', 'author_association', 'user.login', 'project_name', 'active_lock_reason']]

        # Extracting the creation and closure dates from the datetime variable created_at and closed_at
        df.created_at = pd.to_datetime(df.created_at).dt.date
        df.closed_at = pd.to_datetime(df.closed_at).dt.date
        df.updated_at = pd.to_datetime(df.updated_at).dt.date

        # Creating a variable project_duration to reflect the total duration of the project in days
        df['PR_duration'] = (df.closed_at - df.created_at) + timedelta(days=1)

        #Changing association
        df.author_association.replace({'NONE':'NO ASSOCIATION'}, inplace = True)
        
        # Returning the final DataFrame
        return df
    
    
    def get_pr_inferences(repo, df):
        print('|------------------------------------------SUMMARY OF PR-----------------------------------------|')
        print('Total number of unique PR:', len(df))
        print('Total number of unique projects:', len(df['project_name'].unique()))
        print('Total number of unique users:', len(df['user.login'].unique()))
        print('First PR created on:', min(df.created_at))
        print('Last PR created on:', max(df.created_at))
        print('Average number of PR created per day:', \
              np.round((len(df)/(max(df.created_at) - min(df.created_at)).days), decimals = 3))
        print('Average number of PR created per project:', \
              np.round((len(df)/(len(df['project_name'].unique()))), decimals = 3))
        print('|-------------------------------------------------------------------------------------------------|')
        print('\n')
        print('\n')
        
        print('|-------------------------------------------STATE OF PR-------------------------------------------|')
        sns.set(rc={'figure.figsize':(7,7)})
        labels = 'Closed', 'Open'
        explode = (0, 0.1)
        plt.pie(df.state.value_counts(), explode=explode, colors='RG', labels = labels)
        plt.show()
        print('Number of open PR:', len(df[df.state=='open']))
        print('Number of closed PR:', len(df[df.state=='closed']))
        print('|-------------------------------------------------------------------------------------------------|')
        print('\n')
        print('\n')
        
        print('|-------------------------------------------DURATION OF PR----------------------------------------|')
        sns.set(rc={'figure.figsize':(10,5)})
        sns.countplot((df[(df.state=='closed')].PR_duration).dt.days, color='B')
        plt.xlabel('Duration of PR (day(s))')
        plt.ylabel('Count of PR')
        plt.show()
        print('Average duration of a closed PR (days):', np.round(np.mean(df.PR_duration.dt.days), decimals=3))
        print('|-------------------------------------------------------------------------------------------------|')
        print('\n')
        print('\n')
        
        print('|--------------------------------------SPREAD OF DURATION OF PR-----------------------------------|')
        sns.set(rc={'figure.figsize':(10,4)})
        sns.boxplot((df[(df.state=='closed') & (df.PR_duration.dt.days>1)].PR_duration).dt.days, color='R')
        plt.xlabel('Spread of duration of PR (day(s))')
        plt.show()
        print('Median duration of a PR, not closed on the same day (days):', \
              np.round(np.median(df[(df.state=='closed') & (df.PR_duration.dt.days>1)].PR_duration.dt.days)\
              ,decimals = 3))
        print('|-------------------------------------------------------------------------------------------------|')
        print('\n')
        print('\n')
        
        print('|---------------------------------------COUNT OF PR BY PROJECTS-----------------------------------|')
        sns.set(rc={'figure.figsize':(10,6)})
        sns.countplot(y = df.project_name, palette="Set3")
        plt.xlabel('Count of PR')
        plt.ylabel('Name of project')
        plt.show()
        print('|-------------------------------------------------------------------------------------------------|')
        print('\n')
        print('\n')
        
        print('|--------------------------------SPREAD OF DURATION OF PR BY PROJECTS-----------------------------|')
        sns.set(rc={'figure.figsize':(8, 6)})
        sns.boxplot(x = df[(df.state=='closed')].PR_duration.dt.days, y = df.project_name)
        plt.ylabel('Name of project')
        plt.xlabel('Spread of duration of PR (day(s))')
        plt.show()
        print('|-------------------------------------------------------------------------------------------------|')
        print('\n')
        print('\n')
        
        print('|-------------------------------------------PR COUNT BY USER--------------------------------------|')
        sns.set(rc={'figure.figsize':(10,8)})
        sns.countplot(y = df['user.login'])
        plt.xlabel('Count of PR')
        plt.ylabel('Name of user')
        plt.show()
        print('|-------------------------------------------------------------------------------------------------|')
        print('\n')
        print('\n')
        
        print('|-------------------------------------PR COUNT OF AUTHOR ASSOCIATION--------------------------------|')
        sns.set(rc={'figure.figsize':(8,6)})
        sns.countplot(df.author_association)
        plt.xlabel('Type of author association')
        plt.ylabel('Count of PR')
        plt.show()