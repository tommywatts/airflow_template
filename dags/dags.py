from airflow import DAG
import daggen
import os

dag_generator = daggen.DagGen(os.path.join(os.getenv('DAG_DIR'), 'config.yaml'))
dag_generator.generate_dags(globals())
