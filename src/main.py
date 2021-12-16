from github import Github
from github.GithubException import UnknownObjectException,GithubException
from module import argparse as ap
import logging, os, sys
logging.basicConfig(level=logging.INFO)
ARGS = ap.parse_args()

def main():
    token = os.getenv('PAT_TOKEN',None)
    if not token:
        logging.error('PAT_TOKEN does not set')
        sys.exit(1)

    try:
        client = Github(token)
    except Exception as e:
        raise e

    repo_name = ARGS.repo
    try:
        repo = client.get_repo(repo_name)
    except UnknownObjectException as e:
        logging.error(f'Failed to github client creation, Resource not found : {e}')
        sys.exit(1)
    except Exception as e:
        raise e

    if ARGS.init:
        group = 'common'
    else:
        group = get_matching_group(repo)
    workflows = get_workflows(group)

    update_file_in_repository(repo, workflows)

def create_new_file_in_repository(repo, workflows):
    try:
        for workflow in workflows:
            for path,content in workflow.items():
                ret = repo.create_file(path=path, message="[CI] Deploy CI", content=content, branch="master")
                logging.info(f'file has been created to {repo.full_name} : {ret}')
    except GithubException as e:
        logging.error(f'failed to file creation : {e}')
    except Exception as e:
        raise e

def update_file_in_repository(repo, workflows):
    try:
        for workflow in workflows:
            for path,content in workflow.items():
                contents = repo.get_contents(path,ref="master")
                ret = repo.update_file(path=contents.path,message="[CI] Update CI",content=content,sha=contents.sha,branch="master")
                logging.info(f'file has been updated in {repo.full_name} : {ret}')
    except UnknownObjectException as e:
        logging.warning(f'failed to update to {repo.full_name}: {e}')
        logging.warning("The file may not exist, try to create a file.")
        create_new_file_in_repository(repo, workflows)
    except Exception as e:
        raise e

def get_matching_group(repo):
    topics = repo.get_topics()
    groups = []

    list_dir = os.listdir('./')
    for dir in list_dir:
        if os.path.isdir(dir):
            groups.append(dir)

    for topic in topics:
        if topic in groups:
            return topic

    logging.error(f'There are no matching topics in the workflow group!')
    sys.exit(1)

def get_workflows(group):
    workflow_path = f'./{group}/workflows'
    workflow_names = os.listdir(workflow_path)
    ignore = ['.gitkeep']

    ret = []
    for workflow_name in workflow_names:
        if workflow_name in ignore:
            continue
        workflow_info = {}
        with open(f'{workflow_path}/{workflow_name}','r') as f:
            body = f.read()
        path = f'.github/workflows/{workflow_name}'
        workflow_info[path] = body
        ret.append(workflow_info)

    return ret

if __name__ == "__main__":
    main()
