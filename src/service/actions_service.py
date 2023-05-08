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
            # self.deploy_all(org)
            pass
        else:
            destinations = self.actions_mgr.list_destinations(org, dest, type)

            for destination in destinations:
                workflows = self.actions_mgr.list_workflows(destination)

                for workflow in workflows:
                    self.github_mgr.commit(destination, workflow)

    def deploy_all(self, org):
        # TODO: Support single topic
        # Currently, only double topics are supported.
        # see workflow_mgr -> list_workflow_directory_name()
        destinations = self.actions_mgr.find_all_destinations(org)

        for destination in destinations:
            workflows = self.actions_mgr.list_workflows(destination)

            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                for workflow in workflows:
                    executor.submit(self.github_mgr.commit, destination, workflow)
