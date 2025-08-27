from huggingface_hub import HfApi, upload_file
import os

# Configure microservice host URLs # MODIFY TO OS
DATA_STORE_BASE_URL = "http://data-store:3000"
#DATA_STORE_BASE_URL = "http://host.docker.internal:3000"
#DATA_STORE_BASE_URL = "http://data-store:3000"


# Define entity details
NAMESPACE = "default" # Namespace that you create using NeMo Entity Store
DATASET_NAME = "test-dataset"

# Provide HF token ## MODIFY TO OS
#HF_TOKEN = "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"
HF_TOKEN = "mock"

try:
   # Initialize Hugging Face API client
   # Note: A valid token is required for most operations
   hf_api = HfApi(endpoint=f"{DATA_STORE_BASE_URL}/v1/hf", token=HF_TOKEN)

   # Set the dataset repository details
   repo_id = f"{NAMESPACE}/{DATASET_NAME}"
   path_to_local_file = "./src/demo/training_data.json"
   file_name = "training_data.json"  

   # Upload the dataset
   # This will create the repository if it doesn't exist
   hf_api.upload_file(
       repo_type="dataset",
       repo_id=repo_id,
       revision="main",
       path_or_fileobj=path_to_local_file,
       path_in_repo=file_name
   )
   print(f"Successfully uploaded dataset to {repo_id}")

except Exception as e:
   print(f"Error uploading dataset: {str(e)}")
   raise