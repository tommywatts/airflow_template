FROM python:3.7-slim-buster

COPY daggen /daggen
COPY setup.py /setup.py
RUN pip install -e .

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

ARG AIRFLOW_USER_HOME=/usr/local/airflow
ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME}
ENV DAG_DIR=${AIRFLOW_USER_HOME}/dags

COPY entrypoint.sh /entrypoint.sh
COPY config/airflow.cfg ${AIRFLOW_USER_HOME}/airflow.cfg
COPY config/webserver_config.py ${AIRFLOW_USER_HOME}/webserver_config.py

EXPOSE 8080

# USER airflow
WORKDIR ${AIRFLOW_USER_HOME}

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
