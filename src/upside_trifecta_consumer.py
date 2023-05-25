import json
import os
from datetime import datetime, timedelta
from github import Github

access_token = os.getenv("GITHUB_TOKEN")
organization_name = os.getenv("GITHUB_ORG", "dihuynh-org")

# For each message, get the repo and calculate the GHA stats
def handler(event, context):
    g = Github(access_token)