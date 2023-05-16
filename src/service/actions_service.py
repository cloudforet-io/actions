import concurrent.futures

from manager.github_manager import GithubManager
from manager.workflow_manager import WorkflowManager
from manager.actions_manager import ActionsManager


class ActionsService:
    def __init__(self):
        self.github_mgr = GithubManager()
        self.workflow_mgr = WorkflowManager()
        self.actions_mgr = ActionsManager()

    def deploy(self, org, dest, type):
        # TODO: Need to test concurrent.futures is working correctly
        if dest == 'all':
            # TODO: Support single topic
            # Currently, only double topics are supported.
            # see workflow_mgr -> list_workflow_directory_name()

            destinations = self.actions_mgr.find_all_destinations(org)
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(self._deploy_in_concurrent, destination) for destination in destinations]
                concurrent.futures.wait(futures)
        else:
            destinations = self.actions_mgr.list_destinations(org, dest, type)

            for destination in destinations:
                workflows = self.actions_mgr.list_workflows(destination)

                for workflow in workflows:
                    self.github_mgr.commit(destination, workflow)

    def _deploy_in_concurrent(self, destination):
        workflows = self.actions_mgr.list_workflows(destination)
        for workflow in workflows:
            self.github_mgr.commit(destination, workflow)
