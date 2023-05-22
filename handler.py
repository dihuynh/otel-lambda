import json
import os
from datetime import datetime, timedelta
from github import Github

access_token = os.getenv("GITHUB_TOKEN")
organization_name = os.getenv("GITHUB_ORG", "dihuynh-org")


def get_repos(event, context):
    g = Github(access_token)
    organization = g.get_organization(organization_name)
    repos = organization.get_repos()

    current_time = datetime.utcnow()
    last_24 = current_time - timedelta(hours=24)
 
    repos_map = {}
    for repo in repos:
        if last_24 <= repo.updated_at <= current_time:
            repos_map[repo.name] = repo.raw_data
        
    body = {
        "num_repos_updated_last_24": len(repos_map),
        "repos": repos_map
    }

    return {"statusCode": 200, "body": json.dumps(body)}
