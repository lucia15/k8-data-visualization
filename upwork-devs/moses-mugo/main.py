import pandas as pd
from models.pull_request import PR
from models import config
from models.repos import repo
import warnings
warnings.filterwarnings('ignore')


data = pd.DataFrame()
for i in range(0, len(repo)):
    data = pd.concat([data, PR(repo[i]).get_prs()], ignore_index=True)
data.user = pd.json_normalize(data.user).login
df = data.query("state=='open'").reset_index(drop=True)
df = df[['id','url', 'node_id', 'user', 'issue_url', 'number', 'state',
         'created_at', 'assignee', 'requested_reviewers', 'author_association']]
df['assigne'] = None
for i in range(0, len(df)):
    if df.assignee[i] ==None:
        df['assigne'][i] = None
    else:
        df['assigne'][i] = df.assignee[i]['login']
df['review'] = [None if len(df.requested_reviewers.iloc[i]) == 0 else df.requested_reviewers.iloc[i][0]['login'] for i in range(0, len(df))]
df = df.drop(['assignee', 'requested_reviewers'], 1)
df = df.rename(columns = {"assigne": "assignee", "review":"requested_reviewers"})
df['repo']= df.url.str.split('/').str[-3]
df = df[df.columns[::-1]]
df.to_csv("./data/pull_requests.csv", index=False)
