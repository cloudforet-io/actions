import concurrent.futures

from manager.github_manager import GithubManager
from manager.actions_manager import ActionsManager


class ActionsService:
    def __init__(self):
        self.github_mgr = GithubManager()
        self.actions_mgr = ActionsManager()

    def deploy(self, org, dest, type):
        if dest == 'all':
            # TODO: Support single topic
            # Currently, only double topics are supported.

            destinations = self.actions_mgr.find_all_destinations(org)
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(self._commit, destination) for destination in destinations]
                concurrent.futures.wait(futures)
        else:
            destinations = self.actions_mgr.list_destinations(org, dest, type)

            for destination in destinations:
                self._commit(destination)

    def _commit(self, destination):
        workflows = self.actions_mgr.list_workflows(destination)
        for workflow in workflows:
            self.github_mgr.commit(destination, workflow)
