from github import Github
from github.GithubException import GithubException, UnknownObjectException
import os, requests, json, logging, sys

def main():
    token = os.getenv('PAT_TOKEN', None)
    if not token:
        logging.error('PAT_TOKEN does not set')
        sys.exit(1)

    if len(sys.argv) < 2:
        logging.error('Command argument not enough')
        sys.exit(1)

    group = sys.argv[1]

    try:
        client = Github(token)
    except Exception as e:
        raise e

    repo_names = get_all_repositories(group)
    for repo_name in repo_names:
        repo = client.get_repo(repo_name)

        delete_all_workflows(repo)

        workflows = get_workflows('common')
        create_new_file_in_repository(repo, workflows)

def get_all_repositories(group):
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

    return group_match_filter(group, response)

def group_match_filter(group, repositories_info):
    result = []
    for repository_info in repositories_info:
        if group in repository_info['topics']:
            result.append(repository_info['full_name'])

    if not result:
        logging.error("No matching repositories.")
        sys.exit(1)

    return result

def delete_all_workflows(repo):
    try:
        contents = repo.get_contents(".github/workflows", ref="master")
        for content in contents:
            message = f'CI: remove workflows ({content.path})'
            repo.delete_file(path=content.path, message=message, sha=content.sha, branch="master")
    except UnknownObjectException as e:
        print(e)

def create_new_file_in_repository(repo, workflows):
    try:
        for workflow in workflows:
            for path, content in workflow.items():
                message = f'CI: Deploy CI ({path})'
                ret = repo.create_file(path=path, message=message, content=content, branch="master")
                print(f'file has been created to {repo.full_name} : {ret}')
    except GithubException as e:
        print(f'failed to file creation : {e}')
    except Exception as e:
        raise e

def get_workflows(group):
    workflow_path = f'./{group}/workflows'
    workflow_names = os.listdir(workflow_path)
    ignore = ['.gitkeep']

    ret = []
    for workflow_name in workflow_names:
        if workflow_name in ignore:
            continue
        workflow_info = {}
        with open(f'{workflow_path}/{workflow_name}', 'r') as f:
            body = f.read()
        path = f'.github/workflows/{workflow_name}'
        workflow_info[path] = body
        ret.append(workflow_info)

    return ret


if __name__ == "__main__":
    main()