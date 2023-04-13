import logging

from connector.github_connector import GithubConnector
from err.github_err import *

logging.basicConfig(level=logging.INFO)


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
        file_vo = self.github_conn.get_file(destination, path)
        if file_vo is None:
            return None

        return file_vo.decoded_content.decode('utf-8')

    def commit(self, destination, workflow):
        for path, content in workflow.items():
            try:
                if self.get_file_contents(destination, path):
                    logging.info(f'[{destination}] file {path} already exists, try to update')
                    file_vo = self.github_conn.get_file(destination, path)
                    if self._is_need_update(file_vo, content):
                        self.github_conn.update_file(destination, path, content)
                    else:
                        logging.info(f'[{destination}] There is no change, file is not updated: {path}')
                else:
                    logging.info(f'[{destination}] Try to create {path} to {destination}')
                    self.github_conn.create_file(destination, path, content)
            except GithubException as e:
                logging.exception(e)

    @staticmethod
    def _is_need_update(file_vo, workflow):
        contents = file_vo.decoded_content.decode('utf-8')

        if contents == workflow:
            return False

        return True
