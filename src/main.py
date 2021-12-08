from github import Github
from github.GithubException import UnknownObjectException,GithubException
from module import argparse as ap
import logging, os, sys, yaml
logging.basicConfig(level=logging.INFO)
args = ap.parse_args()

def main():
    token = os.getenv('PAT_TOKEN',None)
    if not token:
        logging.error('PAT_TOKEN does not set')
        sys.exit(1)
    client = Github(token)

    config = get_config()
    rTypes = config.get('rTypes',None)
    if not rTypes:
        logging.error('config file is empty')
        sys.exit(1)

    group = args.group
    specified_repo = args.repo

    workflows = get_workflows(group)
    for repo in rTypes[group]:
        if specified_repo and repo['name'] != specified_repo:
            continue
        repo_name = repo['name']
        update_file_in_repository(client, repo_name, workflows)

def create_new_file_in_repository(client, repo_name, workflows):
    repo = client.get_repo(repo_name)

    try:
        for workflow in workflows:
            for path,content in workflow.items():
                ret = repo.create_file(path=path, message="[CI] Deploy CI", content=content, branch="master")
                logging.info(f'file has been created to {repo_name} : {ret}')
    except GithubException as e:
        logging.info(f'failed to file creation (Maybe file already exists or Resource not found): {e}')
    except Exception as e:
        raise e

def update_file_in_repository(client, repo_name, workflows):
    repo = client.get_repo(repo_name)

    try:
        for workflow in workflows:
            for path,content in workflow.items():
                contents = repo.get_contents(path,ref="master")
                ret = repo.update_file(path=contents.path,message="[CI] Update CI",content=content,sha=contents.sha,branch="master")
                logging.info(f'file has been updated in {repo_name} : {ret}')
    except UnknownObjectException as e:
        logging.warning(f'failed to update {repo_name}: {e}')
        logging.warning("Maybe the file doesn't exist. Attempt to create a file")
        create_new_file_in_repository(client, repo_name, workflows)
    except Exception as e:
        raise e

def get_config():
    try:
        with open('./conf.yaml', "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        return config
    except FileNotFoundError as e:
        logging.error(e)
        sys.exit(1)
    except yaml.YAMLError as e:
        logging.error(f"Invalid yaml format! {e}")
        sys.exit(1)

def get_workflows(group):
    workflow_path = f'./{group}/workflows'
    workflow_names = os.listdir(workflow_path)

    github_actions = []
    for workflow_name in workflow_names:
        github_action_set = {}
        with open(f'{workflow_path}/{workflow_name}','r') as f:
            body = f.read()
        path = f'.github/workflows/{workflow_name}'
        github_action_set[path] = body
        github_actions.append(github_action_set)

    return github_actions

if __name__ == "__main__":
    main()
