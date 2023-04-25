import logging

from connector.github_connector import GithubConnector

logging.basicConfig(level=logging.INFO)


class GithubManager:
    def __init__(self):
        self.github_conn = GithubConnector()

    def get_repo(self, destination):
        logging.info(f'[{destination}] get repo')
        return self.github_conn.get_repo(destination)

    def list_repo(self, org):
        return self.github_conn.list_repo(org)

    def search_repo(self, org, keyword):
        logging.info(f'[{org}] search repo: {keyword}')
        return self.github_conn.search_repo(org, keyword)

    def get_topics(self, destination):
        logging.info(f'[{destination}] get topics')
        return self.github_conn.get_topics(destination)

    def get_file_contents(self, destination, path):
        logging.info(f'[{destination}] get file contents: {path}')
        file_vo = self.github_conn.get_file(destination, path)
        if file_vo is None:
            return None

        return file_vo.decoded_content.decode('utf-8')

    def commit(self, destination, workflow):
        for path, content in workflow.items():

            if self.get_file_contents(destination, path):
                logging.info(f'[{destination}] file {path} already exists, try to update')

                file_vo = self.github_conn.get_file(destination, path)
                if not self._is_need_update(file_vo, content):
                    logging.info(f'[{destination}] There is no change, file is not updated: {path}')
                    continue

                try:
                    self.github_conn.update_file(destination, path, content)
                except Exception as e:
                    logging.error(f'[{destination}] Failed to update {path} to {destination} : {e}')

            else:
                try:
                    logging.info(f'[{destination}] Try to create {path} to {destination}')
                    self.github_conn.create_file(destination, path, content)
                except Exception as e:
                    logging.error(f'[{destination}] Failed to create {path} to {destination} : {e}')

    @staticmethod
    def _is_need_update(file_vo, workflow):
        contents = file_vo.decoded_content.decode('utf-8')

        if contents == workflow:
            return False

        return True
