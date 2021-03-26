from airflow import DAG
import daggen

dag_generator = daggen.DagGen('/usr/local/airflow/dags/config.yaml')
dag_generator.generate_dags(globals())
