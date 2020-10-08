import requests
import json
import pandas as pd 
from pandas import json_normalize
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings('ignore')

class Issues:

    def __init__(self, repos):
        self.repos          = repos
        git_token           = 'TOKEN'
        self.git_headers    = {'Authorization': f'token {git_token}'}
        zen_token           = 'TOKEN'
        self.zen_headers    = {'X-Authentication-token': zen_token}
        self.zen_ws_id      = '5f43aa60e9220900139f4fb3'
        self.configure_pandas()
        self.df         = self.init_df()

    def init_df(self):
        try:
            dfs         = []
            for repo in self.repos:
                url                     = f'https://api.github.com/repositories/{repo[1]}/issues'
                res                     = requests.get(url, headers=self.git_headers, params={'state': 'all'}).json()
                zen_url                 = f'https://api.zenhub.com/p2/workspaces/{self.zen_ws_id}/repositories/{repo[1]}/board'
                zen_pipeline            = requests.get(zen_url, headers=self.zen_headers).json()
                zen_pipeline = zen_pipeline['pipelines'] if 'pipelines' in zen_pipeline.keys() else []
                for issue in res:
                    number = issue['number']
                    pipe_name = ''
                    flag = False
                    for panel in zen_pipeline:
                        panel_issues = panel['issues']
                        for item in panel_issues:
                            if item['issue_number'] == number:
                                pipe_name  = panel['name']
                                flag        = True
                                break
                        if flag == True:
                            break
                    issue['pipeline'] = pipe_name
                data                    = json_normalize(res, max_level=1)
                temp_df                 = pd.DataFrame(data)
                temp_df['repo']         = repo[0]
                dfs.append(temp_df)
            df                          = pd.concat(dfs, ignore_index=True)
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

    def normalize_data(self):
        df                      = self.df
        df                      = df[['created_at','user.login', 'user.url','author_association', 'title','body', 'state', 'repo', 'pipeline', 'assignee.login']]
        df['created_at']        = pd.to_datetime(df['created_at']).dt.date
        self.df                 = df

    def show_pie(self, column):
        plt.figure                             (figsize = (8,8))
        self.df[column].value_counts().plot(kind    = 'pie', autopct = '%.2f', fontsize = 20)
        plt.show()

    def show_bar_chart_by_repo(self):
        plt.figure                             (figsize = (15,10))
        self.df["repo"].value_counts().plot.bar(title   = "Bar Chart Showing Number of Issues By Repo")
        plt.ylabel('Number of Issues')
        plt.xlabel('Repo')
        plt.show()

    def show_bar_chart_by_date(self):
        plt.figure                             (figsize = (40,10))
        sns.countplot(self.df['created_at'],    label   = "Number of Issues")
        plt.show()        

    def show_grid_chart(self, column):
        df        = self.df
        keys      = [pair for pair, x in df.groupby([column])]
        plt.figure(figsize=(15,10))
        plt.plot  (keys, df.groupby([column]).count())
        plt.xticks(keys)
        plt.grid  ()
        plt.show  ()

    def show_bar_chart_by_user(self):
        df        = self.df
        user      = df.groupby('user.login')
        response  = user.count()['created_at']
        keys      = [pair for pair, df in user]
        plt.figure(figsize = (10,10))
        plt.bar   (keys, response)
        plt.xticks(keys, rotation='vertical', size=8)
        plt.ylabel('Number of Issues')
        plt.xlabel('Users')
        plt.show()       
         

    def show_tabular_report_by_repo(self):
        df          = self.df
        user        = df.groupby(['repo', 'pipeline'])
        pipe_df      = user['title'].count().unstack(-1, 0)
        return pipe_df

    def show_tabular_report_by_user(self):
        df          = self.df
        user        = df.groupby(['assignee.login', 'pipeline'])
        pipe_df      = user['title'].count().unstack(-1, 0)
        return pipe_df
