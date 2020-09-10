import requests
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pprint import pprint
from datetime import timedelta
import datetime as dt
from pandas.io.json import json_normalize
import warnings
warnings.filterwarnings('ignore')

class PR:
    def __init__(self, repos):
        self.repos      = repos
        token           = 'token'
        self.headers    = {'Authorization': f'token {token}'}
        self.configure_pandas()
        self.df         = self.init_df()

    def init_df(self):
        try:
            dfs         = []
            for repo in self.repos:
                url                 = f'https://api.github.com/repos/filetrust/{repo}/pulls'
                res                 = requests.get(url, headers=self.headers, params={'state': 'all'}).json()
                data                = json_normalize(res, max_level=1)
                temp_df             = pd.DataFrame(data)
                temp_df['repo']     = repo
                dfs.append(temp_df)
            df                      = pd.concat(dfs, ignore_index=True)
            return df
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        
    def get_df(self):
        return self.df

    def configure_pandas(self):        
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        
    def normalize_data(self):
        df                      = self.df
        df                      = df[['number', 'locked', 'created_at', 'updated_at', 'state', 'closed_at','merged_at', 'requested_reviewers', 'labels', 'author_association', 'user.login', 'repo', 'active_lock_reason']]
        df.created_at           = pd.to_datetime(df.created_at).dt.date
        df.closed_at            = pd.to_datetime(df.closed_at).dt.date
        df.updated_at           = pd.to_datetime(df.updated_at).dt.date

        # Creating a variable project_duration to reflect the total duration of the project in days
        df['PR_duration']       = (df.closed_at - df.created_at) + timedelta(days=1)

        #Changing association
        df.author_association.replace({'NONE':'NO ASSOCIATION'}, inplace = True)
        self.df = df

    def get_pr_details(self, num):
        try:
            pr = self.df.loc[self.df.number == int(num)]
            return {"pr_number": pr.number.iloc[0],
                    "repo": self.repos,
                    "node_id": pr.node_id.iloc[0],
                    "state": pr.state.iloc[0],
                    "locked": pr.locked.iloc[0],
                    "title": pr.title.iloc[0],
                    "user": pr.user.iloc[0]['login'],
                    "created_at": pr.created_at.iloc[0],
                    "updated_at": pr.updated_at.iloc[0],
                    "closed_at": pr.closed_at.iloc[0],
                    "merged_at": pr.merged_at.iloc[0],
                    "assignee": [None if pr.assignee.iloc[0] == None else pr.assignee.iloc[0]['login']],
                    "assignees": [None if len(pr.assignees.iloc[0]) ==0 else pr.assignee.iloc[0]['login']],
                    "requested_reviewers": [None if len(pr.requested_reviewers.iloc[0]) == 0 else pr.requested_reviewers.iloc[0][0]['login']],
                    "labels": [None if len(pr.labels.iloc[0]) ==0 else pr.labels.iloc[0][0]['name']],
                    "author_association": pr.author_association.iloc[0],
                    "active_lock_reason": pr.active_lock_reason.iloc[0]
                    }
        except:
            return {"no PR with that number"}

    def get_summary(self):
        df      = self.df
        print('Total number of unique PR:',                 len(df))
        print('Total number of unique projects:',           len(df['repo'].unique()))
        print('Total number of unique users:',              len(df['user.login'].unique()))
        print('First PR created on:',                       min(df.created_at))
        print('Last PR created on:',                        max(df.created_at))
        print('Average number of PR created per day:',      np.round((len(df)/(max(df.created_at) - min(df.created_at)).days), decimals = 3))
        print('Average number of PR created per project:',  np.round((len(df)/(len(df['repo'].unique()))), decimals = 3))

    def show_state(self):
        df      = self.df
        sns.set(rc={'figure.figsize':(7,7)})
        labels  = 'Closed', 'Open'
        explode = (0, 0.1)
        plt.pie(df.state.value_counts(), explode=explode, colors='RG', labels = labels)
        plt.show()
        print('Number of open PR:', len(df[df.state=='open']))
        print('Number of closed PR:', len(df[df.state=='closed']))

    def show_duration(self):
        df          = self.df
        sns.set         (rc={'figure.figsize':(10,5)})
        sns.countplot   ((df[(df.state=='closed')].PR_duration).dt.days, color='B')
        plt.xlabel      ('Duration of PR (day(s))')
        plt.ylabel      ('Count of PR')
        plt.show()
        print('Average duration of a closed PR (days):', np.round(np.mean(df.PR_duration.dt.days), decimals=3))

    def show_spread_duration(self):
        df          = self.df
        sns.set         (rc={'figure.figsize':(10,4)})
        sns.boxplot     ((df[(df.state=='closed') & (df.PR_duration.dt.days>1)].PR_duration).dt.days, color='R')
        plt.xlabel      ('Spread of duration of PR (day(s))')
        plt.show()
        print('Median duration of a PR, not closed on the same day (days):', \
              np.round(np.median(df[(df.state=='closed') & (df.PR_duration.dt.days>1)].PR_duration.dt.days)\
              ,decimals = 3))

    def show_count_by_repo(self):
        df          = self.df
        sns.set         (rc = {'figure.figsize':(10,6)})
        sns.countplot   (y  = df.repo, palette="Set3")
        plt.xlabel      ('Count of PR')
        plt.ylabel      ('Name of project')
        plt.show()

    def show_spread_of_duration_by_repo(self):
        df          = self.df
        sns.set         (rc = {'figure.figsize':(8, 6)})
        sns.boxplot     (x  = df[(df.state=='closed')].PR_duration.dt.days, y = df.repo)
        plt.ylabel      ('Name of project')
        plt.xlabel      ('Spread of duration of PR (day(s))')
        plt.show()

    def show_count_by_user(self):
        df          = self.df
        sns.set         (rc = {'figure.figsize':(10,8)})
        sns.countplot   (y  = df['user.login'])
        plt.xlabel      ('Count of PR')
        plt.ylabel      ('Name of user')
        plt.show()

    def show_count_by_author_association(self):
        df          = self.df
        sns.set         (rc = {'figure.figsize':(8,6)})
        sns.countplot   (df.author_association)
        plt.xlabel      ('Type of author association')
        plt.ylabel      ('Count of PR')
        plt.show()
