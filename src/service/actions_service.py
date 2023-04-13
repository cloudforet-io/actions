from manager.github_manager import GithubManager
from manager.workflow_manager import WorkflowManager
from manager.actions_manager import ActionsManager


class ActionsService:
    def __init__(self):
        self.github_mgr = GithubManager()
        self.workflow_mgr = WorkflowManager()
        self.actions_mgr = ActionsManager()

    def deploy(self, org, dest, type):
        destinations = self.actions_mgr.get_destinations(org, dest, type)

        for destination in destinations:
            workflows = self.actions_mgr.get_workflows(destination)

            for workflow in workflows:
                self.github_mgr.commit(destination, workflow)
