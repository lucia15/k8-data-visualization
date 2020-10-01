import warnings
warnings.filterwarnings('ignore')
from models.transform import transform_pr, transform_issues


# create a csv of pull requests
pr = transform_pr()
pr.to_csv("./data/pull_requests.csv", index=False)

# create a csv of pull issues
issues = transform_issues()
issues.to_csv("./data/issues.csv", index=False)
