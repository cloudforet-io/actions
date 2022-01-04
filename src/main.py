from github import Github
from github.GithubException import UnknownObjectException,GithubException
from module import argparse as ap
import logging, os, sys, requests, json
logging.basicConfig(level=logging.INFO)
ARGS = ap.parse_args()

def main():
    token = _get_token()
    client = _get_client(token)
    init = ARGS.init

    if ARGS.repo:
        repo_name = ARGS.repo
        deploy_to_repository(client, repo_name, init)
    elif ARGS.group:
        group = ARGS.group
        deploy_to_group(client, group, init)
    else:
        sys.exit(1)

def deploy_to_repository(client, repo_name, init):
    repo = _get_repo(client, repo_name)

    if init:
        workflows = _get_workflows('common')
    else:
        group = _get_group_compare_topics(repo)
        workflows = _get_workflows(group)

    _deploy(repo, workflows, init)

def deploy_to_group(client, group, init):
    repo_names = _get_all_repositories(group)

    for repo_name in  repo_names:
        repo = _get_repo(client, repo_name)

        if init:
            workflows = _get_workflows('common')
        else:
            workflows = _get_workflows(group)

        _deploy(repo, workflows, init)

def _deploy(repo, workflows, init):
    if init:
        _delete_all_workflows_in_repository(repo)
        _create_new_file_in_repository(repo, workflows)
    else:
        _update_file_in_repository(repo, workflows)

def _get_token():
    token = os.getenv('PAT_TOKEN',None)
    if not token:
        logging.error('PAT_TOKEN does not set')
        sys.exit(1)

    return token

def _get_client(token):
    try:
        return Github(token)
    except Exception as e:
        raise e

def _get_repo(client, repo_name):
    try:
        return client.get_repo(repo_name)
    except UnknownObjectException as e:
        logging.error(f'Failed to github client creation, Resource not found : {e}')
        sys.exit(1)
    except Exception as e:
        raise e

def _get_all_repositories(group):
    url = 'https://api.github.com/orgs/spaceone-dev/repos'

    headers = {
        "Accept" : "application/vnd.github.v3+json"
    }

    try:
        response = requests.get(url, headers=headers).json()
    except requests.exceptions.ConnectionError as e:
        raise Exception(f'Connection Error {e.response}')
    except requests.exceptions.HTTPError as e:
        raise Exception(f'HTTP Error {e.response}')
    except json.JSONDecodeError as e:
        raise Exception(f'Json Decode Error {e}')

    return _group_match_filter(group, response)

def _group_match_filter(group, repositories):
    result = []
    for repository in repositories:
        if group in repository['topics']:
            result.append(repository['full_name'])

    if not result:
        logging.error("No matching repositories.")
        sys.exit(1)

    return result

def _delete_all_workflows_in_repository(repo):
    try:
        contents = repo.get_contents(".github/workflows", ref="master")
        for content in contents:
            message = f'CI: remove workflows ({content.path})'
            repo.delete_file(path=content.path, message=message, sha=content.sha, branch="master")
    except UnknownObjectException as e:
        print(e)

def _create_new_file_in_repository(repo, workflows):
    try:
        for workflow in workflows:
            for path,content in workflow.items():
                ret = repo.create_file(path=path, message="[CI] Deploy CI", content=content, branch="master")
                logging.info(f'file has been created to {repo.full_name} : {ret}')
    except GithubException as e:
        logging.error(f'failed to file creation : {e}')
    except Exception as e:
        raise e

def _update_file_in_repository(repo, workflows):
    try:
        for workflow in workflows:
            for path,content in workflow.items():
                contents = repo.get_contents(path,ref="master")
                ret = repo.update_file(path=contents.path,message="[CI] Update CI",content=content,sha=contents.sha,branch="master")
                logging.info(f'file has been updated in {repo.full_name} : {ret}')
    except UnknownObjectException as e:
        logging.warning(f'failed to update to {repo.full_name}: {e}')
        logging.warning("The file may not exist, try to create a file.")
        _create_new_file_in_repository(repo, workflows)
    except Exception as e:
        raise e

def _get_group_compare_topics(repo):
    topics = repo.get_topics()
    groups = []

    list_dir = os.listdir('./')
    for dir in list_dir:
        if os.path.isdir(dir):
            groups.append(dir)

    for topic in topics:
        if topic in groups:
            return topic

    logging.error('There are no matching topics in the workflow group!')
    sys.exit(1)

def _get_workflows(group):
    try:
        workflow_path = f'./{group}/workflows'
        workflow_list = os.listdir(workflow_path)
        not_workflow_file = ['.gitkeep']
    except FileNotFoundError as e:
        logging.error(e)
        sys.exit(1)
    except Exception as e:
        raise e

    workflows = []
    for workflow_name in workflow_list:
        if workflow_name in not_workflow_file:
            continue
        full_workflow_info = _read_workflows(workflow_path, workflow_name)
        workflows.append(full_workflow_info)

    return workflows

def _read_workflows(workflow_path, workflow_name):
    workflow_info = {}
    with open(f'{workflow_path}/{workflow_name}','r') as f:
        body = f.read()
    path = f'.github/workflows/{workflow_name}'
    workflow_info[path] = body

    return workflow_info

if __name__ == "__main__":
    main()
