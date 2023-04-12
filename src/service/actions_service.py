from manager.github_manager import GithubManager
from manager.workflow_manager import WorkflowManager


class ActionsService:
    def __init__(self):
        self.github_mgr = GithubManager()
        self.workflow_mgr = WorkflowManager()

    def deploy(self, org, dest, type, init):
        destinations = []

        if type == 'repository':
            destinations.append(dest)
        elif type == 'topic':
            destinations = self._convert_topic_to_repository_name(org, dest)

        for destination in destinations:
            if type == 'topic':
                workflows = self.workflow_mgr.list_workflows_data(dest)
            elif type == 'repository':
                github_topics = self.github_mgr.get_topics(destination)
                workflow_topics = self.workflow_mgr.list_workflow_directory_name()
                topic = self._get_topic_with_dest(github_topics, workflow_topics)
                workflows = self.workflow_mgr.list_workflows_data(topic)
            else:
                raise Exception('invalid type')

            if init:
                workflows += self.workflow_mgr.list_workflows_data('common')

            for workflow in workflows:
                self.github_mgr.commit(destination, workflow)

    def _convert_topic_to_repository_name(self, org, destination):

        repositories = self.github_mgr.list_repo(org)

        results = []
        if len(destination.split("/")) == 2:
            topic1 = destination.split("/")[0]
            topic2 = destination.split("/")[1]

            for repository in repositories:
                topics = repository.get_topics()
                if topic1 in topics and topic2 in topics:
                    results.append(repository.full_name)

        elif len(destination.split("/")) == 1:
            topic = destination.split("/")[0]

            for repository in repositories:
                topics = repository.get_topics()
                if topic in topics:
                    results.append(repository.full_name)

        return results

    @staticmethod
    def _get_topic_with_dest(github_topics, workflow_topics):
        topic_1 = ''
        topic_2 = ''

        for topic in github_topics:
            if topic in workflow_topics.keys():
                topic_1 = topic

        for topic in github_topics:
            if topic_1 and topic in workflow_topics[topic_1]:
                topic_2 = topic

        return f'{topic_1}/{topic_2}'
