#!/bin/bash

: "${AIRFLOW_HOME:="/usr/local/airflow"}"
: "${AIRFLOW__CORE__EXECUTOR:=${EXECUTOR:-Sequential}Executor}"

export \
    AIRFLOW__CORE__EXECUTOR \
    AIRFLOW_HOME

airflow db init

airflow scheduler &

exec airflow webserver
