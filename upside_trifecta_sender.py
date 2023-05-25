import boto3
import os
from datetime import datetime, timedelta
from github import Github

access_token = os.getenv("GITHUB_TOKEN")
organization_name = os.getenv("GITHUB_ORG", "dihuynh-org")
recently_updated_repo_sns_arn = os.getenv("SNS_RECENT_REPOS_ARN", "arn:aws:sns:us-east-1:612245820181:recently_updated_repos")
calculate_actions_stats_sqs_arn = os.getenv("SQS_CALCULATE_ACTIONS_STATS_ARN")

sns = boto3.client('sns')

# Get a list of repos updated in the last 24, 
# for each one, send a message to SNS
# the upside_trifecta_consumer will process each message 
def handler(event, context):
    repos: dict = get_repos()
    for item in repos:
        send_message(item)


def get_repos():
    g = Github(access_token)

    current_time = datetime.utcnow()
    last_24 = current_time - timedelta(hours=24)
    query = f'org:{organization_name} pushed:>{last_24.isoformat()}'
    result = g.search_repositories(query=query)
 
    repos_map = {}
    for repo in result:
        repos_map[repo.name] = repo.updated_at.isoformat()

    return repos_map


def send_message(repo):
    # send sns message with boto3
    response = sns.publish(
        TopicArn=recently_updated_repo_sns_arn,
        Message=repo
    )
    print(f"publish message for {repo} {response}")


handler({}, {})