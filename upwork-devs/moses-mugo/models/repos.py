import pandas as pd
import requests
import config


class Repos:
    def __init__(self, username):
        self.username = username
        self.github_api = "https://api.github.com"
        self.gh_session = requests.Session()
        self.gh_session.auth = (config.GITHUB_USERNAME, config.GITHUB_TOKEN)
        self.df = self.get_repos()

    def get_repos(self):
        url = self.github_api + '/users/' + self.username + '/repos'
        try:
            repos = pd.DataFrame(self.gh_session.get(url=url).json())
            return repos
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    def list_repos(self):
        if self.df.shape[0] == 0:
            return "No repos found"
        else:
            return list(self.df.name.values)
