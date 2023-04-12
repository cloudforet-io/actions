from connector.github_connector import GithubConnector
from err.github_err import *


class GithubManager:
    def __init__(self):
        self.github_conn = GithubConnector()

    def get_repo(self, destination):
        return self.github_conn.get_repo(destination)

    def list_repo(self, org):
        return self.github_conn.list_repo(org)

    def get_topics(self, destination):
        return self.github_conn.get_topics(destination)

    def get_file_contents(self, destination, path):
        try:
            file_vo = self.github_conn.get_file(destination, path)

            return file_vo.decoded_content.decode('utf-8')
        except GithubException:
            raise None

    def commit(self, destination, workflows):
        for path, content in workflows.items():
            try:
                if self.get_file_contents(destination, path):
                    print(f'file {path} already exists, try to update')
                    file_vo = self.github_conn.get_file(destination, path)
                    if self._is_need_update(file_vo, content):
                        self.github_conn.update_file(destination, path, content)
                    else:
                        print(f'There is no change, file is not updated: {path}')
                else:
                    self.github_conn.create_file(destination, path, content)
            except GithubException as e:
                print(e)

    @staticmethod
    def _is_need_update(file_vo, workflow):
        contents = file_vo.decoded_content.decode('utf-8')

        if contents == workflow:
            return False

        return True
