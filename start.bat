SET EVALUATOR_IMAGE=nvcr.io/nvidia/nemo-microservices/evaluator:25.07
SET DATA_STORE_IMAGE=nvcr.io/nvidia/nemo-microservices/datastore:25.07
SET USER_ID=$(id -u)
SET GROUP_ID=$(id -g)
:: SET API_KEY = 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
:: docker login -u '$oauthtoken' -p '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' nvcr.io
docker login -u '$oauthtoken' nvcr.io
docker compose -f docker_compose.yaml up evaluator -d

