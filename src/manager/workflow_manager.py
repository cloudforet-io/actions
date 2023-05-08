import os
import logging

logging.basicConfig(level=logging.INFO)


class WorkflowManager:

    @staticmethod
    def list_workflows_data(topic):
        try:
            base_path = f'./workflows/{topic}'
            list_dir = os.listdir(base_path)

            workflow_files = []
            for workflow_name in list_dir:
                with open(f'{base_path}/{workflow_name}', 'r') as f:
                    workflow_contents = f.read()
                workflow_files.append({
                    f'.github/workflows/{workflow_name}': workflow_contents
                })
            return workflow_files
        except Exception as e:
            logging.info(f'Failed to list workflows data(invalid or lack of topics): {e}')
            raise Exception(e)

    def list_workflow_directory_name(self):
        path = './workflows/'
        topics = {}

        topic_1 = self._only_directory(path)
        for topic in topic_1:
            topic_2 = self._only_directory(f'{path}/{topic}')
            topics[topic] = topic_2

        return topics

    @staticmethod
    def _only_directory(path):
        ignore = ['__pycache__']
        return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d)) and d not in ignore]
