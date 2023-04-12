import os
import github
import logging

from github import Github
from err.github_err import *

logging.basicConfig(level=logging.INFO)


class GithubConnector:
    def __init__(self):
        self.token = os.getenv('PAT_TOKEN', None)
        self.github_client = Github(self.token)
        self.committer = github.InputGitAuthor(name='cloudforet-admin', email='admin@cloudforet.io')

    def list_repo(self, org):
        repositories = []
        for repo in self.github_client.get_organization(org).get_repos():
            repositories.append(repo)

        return repositories

    def get_repo(self, destination):
        return self.github_client.get_repo(destination)

    def get_topics(self, destination):
        repo_vo = self.get_repo(destination)
        return repo_vo.get_topics()

    def get_file(self, destination, path):
        repo_vo = self.get_repo(destination)

        try:
            return repo_vo.get_contents(path=path, ref="master")
        except GithubException as e:
            return None
        except Exception as e:
            raise Exception(e)

    def create_file(self, destination, path, content):
        repo_vo = self.get_repo(destination)
        try:
            repo_vo.create_file(path=path, message="[CI] Deploy CI", content=content, branch="master",
                                committer=self.committer)
            return 200
        except GithubException as e:
            logging.exception(f'Failed to file creation: {e}')
            raise Exception(e)
        except Exception as e:
            raise Exception(e)

    def update_file(self, destination, path, content):
        repo_vo = self.get_repo(destination)
        file_vo = self.get_file(destination, path)

        try:
            repo_vo.update_file(path=path, message="[CI] Deploy CI", content=content, sha=file_vo.sha,
                                branch="master",
                                committer=self.committer)
            return 200
        except GithubException as e:
            raise GithubException(e)
        except Exception as e:
            raise Exception(e)
