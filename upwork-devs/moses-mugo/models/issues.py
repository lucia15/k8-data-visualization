import pandas as pd
import requests
import config


class Issues:
    def __init__(self, repo):
        self.repo = repo
        self.github_api = "https://api.github.com"
        self.gh_session = requests.Session()
        self.gh_session.auth = (config.GITHUB_USERNAME, config.GITHUB_TOKEN)
        self.df = self.get_issues()

    def get_issues(self):
        url = self.github_api + '/repos/filetrust/'+self.repo+'/issues'
        try:
            issues = pd.DataFrame(self.gh_session.get(url=url).json())
            return issues
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    def report(self):
        if self.df.shape[0] == 0:
            return "No issues found"
        else:
            return {
                "total_number_of_issues": len(self.df),
                "number_of_open_issues": self.df.query("state=='open'").shape[0],
                "number_of_closed_issues": self.df.query("state=='closed'").shape[0]
            }



