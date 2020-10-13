import pandas as pd
from pull_requests import PR
from repos import Repos
from issues import Issues
import warnings
warnings.filterwarnings('ignore')


def transform_pr():
    data = pd.DataFrame()
    repos = Repos('k8-proxy').list_repos()
    for i in range(0, len(repos)):
        data = pd.concat([data, PR('k8-proxy', repos[i]).get_prs()], ignore_index=True)
    data.user = pd.json_normalize(data.user).login
    df = data.copy()
    df = df[['id','url', 'node_id', 'user', 'issue_url', 'number', 'state',
             'created_at', 'assignee', 'requested_reviewers', 'author_association']]
    df['assigne'] = None
    for i in range(0, len(df)):
        if df.assignee[i] ==None:
            df['assigne'][i] = None
        else:
            df['assigne'][i] = df.assignee[i]['login']
    df['review'] = [None if len(df.requested_reviewers.iloc[i]) == 0
                    else df.requested_reviewers.iloc[i][0]['login'] for i in range(0, len(df))]
    df = df.drop(['assignee', 'requested_reviewers'], 1)
    df = df.rename(columns={"assigne": "assignee", "review":"requested_reviewers"})
    df.requested_reviewers.replace({'dinis-cruz-gw':'DinisCruz'}, inplace=True)
    df['repo']= df.url.str.split('/').str[-3]
    df = df[df.columns[::-1]]
    df = df.rename(columns = {"user": "user_"})
    pr_df = df.copy()
    return pr_df


def transform_issues():
    data = pd.DataFrame()
    repos = Repos('k8-proxy').list_repos()
    for i in range(0, len(repos)):
        data = pd.concat([data, Issues('k8-proxy', repos[i]).get_issues()], ignore_index=True)
    data = data.drop(['labels_url', 'repository_url', 'locked', 'comments_url', 'performed_via_github_app',
                      'events_url', 'html_url', 'labels', 'assignee', 'milestone'], 1)
    data.user = pd.json_normalize(data.user).login
    data['repo'] = data.url.str.split('/').str[-3]
    data['assignee'] = None
    for i in range(0, len(data)):
        if len(data.assignees[i]) == 0:
            data['assignee'][i] = None
        elif len(data.assignees[i]) == 1:
            data['assignee'][i] = data.assignees[i][0]['login']
        else:
            data['assignee'][i] = list(pd.DataFrame(data.assignees[i]).login.values)
    data['pr'] = None
    for i in range(0, len(data)):
        if pd.isna(data.pull_request[i]):
            data['pr'][i] = None
        else:
            data['pr'][i] = data.pull_request[i]['url']
    data = data.drop(['assignees', 'pull_request'], 1)
    data = data.rename(columns={"user": "user_", "pr": "pull_request"})
    data = data[['title', 'state', 'url', 'repo', 'user_', 'author_association',
                 'assignee', 'created_at', 'updated_at', 'closed_at', 'number',
                 'comments', 'node_id', 'id', 'active_lock_reason', 'pull_request']]
    issues_df = data.copy()
    return issues_df
