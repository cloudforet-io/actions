import concurrent.futures

from manager.github_manager import GithubManager
from manager.actions_manager import ActionsManager
from manager.workflow_manager import WorkflowManager


class ActionsService:
    def __init__(self):
        self.github_mgr = GithubManager()
        self.actions_mgr = ActionsManager()
        self.workflow_mgr = WorkflowManager()

    def deploy(self, org, dest, dest_type):
        destinations = self.actions_mgr.list_destinations(org, dest, dest_type)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self._commit, destination) for destination in destinations]
            concurrent.futures.wait(futures)

    def _commit(self, destination):
        workflows = self.workflow_mgr.list_workflows(destination)
        for workflow in workflows:
            self.github_mgr.commit(destination, workflow)
