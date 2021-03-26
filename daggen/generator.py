import yaml
from airflow.models import DAG, BaseOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from datetime import timedelta, datetime

from daggen.utils import date_transform, import_str_module

class DagGen:

    def __init__(self, config_path):
        self.config = self.parse_config(config_path)

    @staticmethod
    def parse_config(config_path):
        with open(config_path) as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
        return {dag: {'dag_id':dag, **config[dag]} for dag in config.keys()}

    @staticmethod
    def format_params(params):
        start_date = params.get('default_args', {}).get('start_date')
        if start_date:
            params['default_args']['start_date'] = date_transform(start_date)

        end_date = params.get('default_args', {}).get('start_date')
        if end_date:
            params['default_args']['end_date'] = date_transform(end_date)
            
        return params

    @staticmethod
    def generate_task(config):

        obj = import_str_module(config['operator'])
        params = {k: v for k, v in config.items() if k not in ['operator', 'dependencies']}

        if obj == PythonOperator:
            pass

        if obj == KubernetesPodOperator:
            pass

        if obj == BashOperator:
            pass

        return obj(**params)

    def generate_dags(self, globals):
        
        for name, config in self.config.items():

            dag_id = config['dag_id']

            dag = DAG(
                dag_id = dag_id,
                **self.format_params(config['params'])
                )

            tasks = config['tasks']
            task_objs = {}

            for task_name, task_config in tasks.items():
                task_config['task_id'] = task_name
                task_config['dag'] = dag
                task = self.generate_task(task_config)
                task_objs[task.task_id] = task

            for task_name, task_config in tasks.items():
                if task_config.get("dependencies"):
                    source_task = task_objs[task_name]
                    for dependency in task_config["dependencies"]:
                        dependency_task = task_objs[dependency]
                        source_task.set_upstream(dependency_task)

            globals[dag_id] = dag
           