import pandas as pd
import requests
from models import config


class Issues:
    github_api = "https://api.github.com/repos/"
    gh_session = requests.Session()
    gh_session.auth = (config.GITHUB_USERNAME, config.GITHUB_TOKEN)

    def __init__(self, username, repo):
        self.username = username
        self.repo = repo
        self.df = self.get_issues()

    def get_issues(self):
        url = self.github_api+self.username+'/'+self.repo+'/issues'
        try:
            issues = self.gh_session.get(url=url).json()
            if type(issues) == 'dict':
                return pd.DataFrame()
            else:
                return pd.DataFrame(issues)
        except requests.exceptions.RequestException as e:
            return pd.DataFrame()

    def report(self):
        if self.df.shape[0] == 0:
            return "No issues found"
        else:
            return {
                "total_number_of_issues": len(self.df),
                "number_of_open_issues": self.df.query("state=='open'").shape[0],
                "number_of_closed_issues": self.df.query("state=='closed'").shape[0]
            }
