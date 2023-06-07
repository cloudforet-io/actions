import os
import logging
from manager.github_manager import GithubManager

logging.basicConfig(level=logging.INFO)


# TODO: improve workflow_directory_name and topic

class WorkflowManager:
    def __init__(self):
        self.github_mgr = GithubManager()

    def list_workflows(self, dest):
        github_topics = self.github_mgr.get_topics(dest)
        workflow_directory_name = self.list_workflow_directory_name()

        topic = self._filter_topic(github_topics, workflow_directory_name)
        workflows = self.list_workflows_data(topic)

        return workflows

    def list_workflow_directory_name(self):
        path = './workflows/'
        topics = {}

        main_topics = self._only_directory(path)
        for main_topic in main_topics:
            sub_topic = self._only_directory(f'{path}/{main_topic}')
            # If there is no sub topic, set None
            topics[main_topic] = sub_topic if sub_topic else []

        return topics

    @staticmethod
    def list_workflows_data(topic):
        try:
            workflow_files = []

            base_common_path = './workflows/common'
            workflow_files += WorkflowManager._read_workflow_files(base_common_path)

            base_path = f'./workflows/{topic}'
            workflow_files += WorkflowManager._read_workflow_files(base_path)

            return workflow_files
        except Exception as e:
            logging.info(f'Failed to list workflows data(invalid or lack of topics): {e}')
            raise Exception(e)

    @staticmethod
    def _read_workflow_files(base_path):
        ret = []

        list_dir = os.listdir(base_path)
        for workflow_name in list_dir:
            with open(f'{base_path}/{workflow_name}', 'r') as f:
                workflow_contents = f.read()

            ret.append({
                f'.github/workflows/{workflow_name}': workflow_contents
            })

        return ret

    @staticmethod
    def _only_directory(path):
        ignore = ['__pycache__']
        return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d)) and d not in ignore]

    @staticmethod
    def _filter_topic(github_topics, workflow_directory_name):
        main_topic = ''
        sub_topic = ''

        for topic_for_main in github_topics:
            if topic_for_main in workflow_directory_name.keys():
                main_topic = topic_for_main

        if main_topic == '':
            raise Exception(f'No topic matched for workflows: {github_topics}')

        if workflow_directory_name[main_topic]:
            for topic_for_sub in github_topics:
                if topic_for_sub in workflow_directory_name[main_topic]:
                    sub_topic = topic_for_sub

        logging.info(f'Found topic for workflows: {main_topic}/{sub_topic}')

        return f'{main_topic}/{sub_topic}'
