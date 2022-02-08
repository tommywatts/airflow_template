# =====================================
#     CLOUD COMPOSER SETUP
#======================================

COMPOSER_ZONE=europe-west2-a
COMPOSER_SANDBOX_NAME=pyvarotti
COMPOSER_SANDBOX_LOCATION=europe-west2
COMPOSER_SANDBOX_BUCKET:= $(shell gcloud beta composer environments describe --location=europe-west2 ${COMPOSER_SANDBOX_NAME} \
	| grep -hnr "dagGcsPrefix" \
	| cut -d " " -f 4 \
	| sed -e "s/\/dags//")

composer-build:
	gcloud composer environments create ${COMPOSER_SANDBOX_NAME} \
    --location ${COMPOSER_SANDBOX_LOCATION} \
	--zone ${COMPOSER_ZONE} \
	--machine-type n1-standard-4

	gcloud composer environments update ${COMPOSER_SANDBOX_NAME} \
	--location ${COMPOSER_SANDBOX_LOCATION} \
	--update-env-variables=DAG_DIR=/home/airflow/gcs/dags/

composer-deploy-dags:
	gsutil cp daggen/generator.py ${COMPOSER_SANDBOX_BUCKET}/dags/
	gsutil cp daggen/utils.py ${COMPOSER_SANDBOX_BUCKET}/dags/
	rm -rf .dags/__pycache__
	gsutil -m cp -r ./dags ${COMPOSER_SANDBOX_BUCKET}/
	gsutil -m cp -r ./daggen ${COMPOSER_SANDBOX_BUCKET}/dags

composer-teardown:
	gcloud composer environments delete ${COMPOSER_SANDBOX_NAME} \
    --location ${COMPOSER_SANDBOX_LOCATION}

	COMPOSER_SANDBOX_BUCKET=$(call get_composer_bucket)
	gsutil rm -r ${COMPOSER_SANDBOX_BUCKET}


# =====================================
#     LOCAL BUILD
#======================================

build:
	docker-compose build

run:
	docker-compose up 

down:
	docker-compose down --remove-orphans
