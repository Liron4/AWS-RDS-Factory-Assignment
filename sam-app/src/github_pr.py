import os
import json
import boto3
from github import Github
from github.GithubException import GithubException

GITHUB_TOKEN_SECRET_ARN = os.environ['GITHUB_TOKEN_SECRET_ARN']
REPO_NAME = os.environ['GITHUB_REPO']

boto_client = boto3.client('secretsmanager')
github_client = None

def _get_github_client():
    global github_client
    if github_client:
        return github_client

    response = boto_client.get_secret_value(
        SecretId=GITHUB_TOKEN_SECRET_ARN
    )
    token = json.loads(response['SecretString'])['GitHubToken']
    
    github_client = Github(token)
    return github_client

def create_pr(db_name, file_path, file_content, pr_title) -> str:
    g = _get_github_client()
    repo = g.get_repo(REPO_NAME)
    
    base_branch = repo.get_branch("main")
    new_branch_name = f"rds/provision-{db_name}"

    try:
        repo.create_git_ref(
            ref=f"refs/heads/{new_branch_name}",
            sha=base_branch.commit.sha
        )
    except GithubException as e:
        if e.status == 422:
            pass
        else:
            raise
    
    repo.create_file(
        path=file_path,
        message=f"Add terraform config for {db_name}",
        content=file_content,
        branch=new_branch_name
    )
    
    pr = repo.create_pull(
        title=pr_title,
        body=f"Automated PR to provision the '{db_name}' RDS cluster.",
        head=new_branch_name,
        base="main"
    )
    
    return pr.html_url
