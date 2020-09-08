import requests
import json
import pandas as pd
from pandas import json_normalize

import warnings
warnings.filterwarnings('ignore')

class Issues:
    def __init__(self, repos):
        self.repos = repos
        token = ''
        self.headers = {'Authorization': f'token {token}'}
        self.configure_pandas()
        self.df = self.init_df()

    def init_df(self):
        try:
            dfs = []
            for repo in self.repos:
                url = f'https://api.github.com/repos/filetrust/{repo}/issues'
                res = requests.get(url, headers=self.headers, params={'state': 'all'}).json()
                data = json_normalize(res, max_level=1)
                temp_df = pd.DataFrame(data)
                temp_df['repo']= repo
                dfs.append(temp_df)
            df = pd.concat(dfs, ignore_index=True)
            return df
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    def get_df(self):
        return self.df

    def configure_pandas(self):
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)
        pd.set_option('display.expand_frame_repr', False)

    def important(self):
        # Selecting Important Columns
        df= self.df[['assignee.login', 'state','milestone.state']]
        # Creating date columns
        df = df.rename({'assignee.login':'Assignee'}, axis=1)
        df = df.rename({'state':'Issue'}, axis=1)
        df = df.rename({'milestone.state':'In Progress'}, axis=1)
        df['Assignee'].fillna('Unassigned', inplace=True)
        self.df = df
    
    def status(self):
        table = self.df.groupby('Assignee')['Issue'].value_counts().unstack().fillna(0)
        print(table)

  