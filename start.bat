SET EVALUATOR_IMAGE=nvcr.io/nvidia/nemo-microservices/evaluator:25.07
SET DATA_STORE_IMAGE=nvcr.io/nvidia/nemo-microservices/datastore:25.07
SET USER_ID=$(id -u)
SET GROUP_ID=$(id -g)
:: docker login -u '$oauthtoken' -p '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' nvcr.io
docker compose -f docker_compose.yaml up evaluator -d