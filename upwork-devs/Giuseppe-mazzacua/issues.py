import      requests
import      pandas            as pd
import      seaborn           as sns
import      matplotlib.pyplot as plt
from        pandas import json_normalize

""" Documentation for classes """
class Issues:

    def __init__(self, repos):
        self.repos      = repos
        token           = 'TOKEN'
        self.headers    = {'Authorization': f'token {token}'}
        self.configure_pandas()
        self.df         = self.init_df()

    """ Small documentation for methods """
    def init_df(self):
        try:
            dfs         = []
            for repo in self.repos:
                url                 = f'https://api.github.com/repos/filetrust/{repo}/issues'
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
        pd.set_option('display.max_rows'            , None )
        pd.set_option('display.max_columns'         , None )
        pd.set_option('display.width'               , None )
        pd.set_option('display.max_colwidth'        , -1.  )
        pd.set_option('display.expand_frame_repr'   , False)

    def normalize_data(self):
        df                      = self.df
        df                      = df[['created_at','user.login', 'user.url','author_association', 'title','body', 'state', 'milestone.title','milestone.state','repo']]
        df['created_at']        = pd.to_datetime(df['created_at']).dt.date
        self.df                 = df

    def show_pie(self, column):
        plt.figure                             (figsize = (8,8))
        self.df[column].value_counts().plot.   (kind    = 'pie', autopct = '%.2f', fontsize = 20)
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
        plt.show  ()        
