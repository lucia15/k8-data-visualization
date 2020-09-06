import pandas as pd
import requests
from models import config


class PR:
    def __init__(self, repo):
        self.repo = repo
        self.github_api = "https://api.github.com"
        self.gh_session = requests.Session()
        self.gh_session.auth = (config.GITHUB_USERNAME, config.GITHUB_TOKEN)
        self.df = self.get_prs()

    def get_prs(self):
        url = self.github_api + '/repos/filetrust/'+self.repo+'/pulls'
        try:
            pr = pd.DataFrame(self.gh_session.get(url=url).json())
            return pr
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    def get_summary(self):
        if self.df.shape[0] == 0:
            return "No PR found"
        else:
            return {
                "total_number_of_PR": len(self.df),
                "number_of_open_PR": self.df.query("state=='open'").shape[0],
                "number_of_closed_PR": self.df.query("state=='closed'").shape[0],
                "pr_numbers": self.df.number.to_list()
            }

    def get_pr_details(self, num):
        try:
            pr = self.df.loc[self.df.number == int(num)]
            return {"pr_number": pr.number.iloc[0],
                    "repo": self.repo,
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

