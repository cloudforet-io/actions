from manager.github_manager import GithubManager
from manager.workflow_manager import WorkflowManager


class ActionsManager:
    def __init__(self):
        self.github_mgr = GithubManager()
        self.workflow_mgr = WorkflowManager()

    def list_destinations(self, org, dest, dest_type):
        if dest_type == 'repository':
            return [f'{org}/{dest}']
        elif dest_type == 'topic':
            topics = dest.split("/")
            keyword = self._make_keyword(topics, org)
            repositories = self.github_mgr.search_repo(org, keyword)
            return [repository.full_name for repository in repositories]

    @staticmethod
    def _make_keyword(topics, org):
        keyword = f'org:{org} ' + ' '.join(f'topic:{topic}' for topic in topics if topic != '')
        return keyword
