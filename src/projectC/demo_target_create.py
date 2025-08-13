import huggingface_hub as hh
from nemo_microservices import NeMoMicroservices
import json

# Initialize the client
client = NeMoMicroservices(base_url="http://localhost:7331")

model_id = "nvidia_llama-3.1-nemotron-nano-8b-v1"

my_prompt_dataset = [
    {
        "prompt": "¿Hasta que edad me pueden dar una hipoteca Oxigeno?",
        "ideal_response": "Puedes solicitar la Hipoteca Oxigeno siempre que la del plazo de esta y edad del mayor de los titulares no supere los 75 años en el caso de las primeras residencias o los 70 años en las segundas.",
        "category": "Closed QA"
    },
]


# Write the dataset to disk.
my_prompt_dataset_filepath = 'my-prompt-dataset.json'
with open(my_prompt_dataset_filepath, "w") as json_file:
    json.dump(my_prompt_dataset, json_file, indent=4)

import requests
from huggingface_hub import HfApi # huggingface_hub version >= 0.26.2

DATASTORE_HOSTNAME = "localhost:3000" # Update this before you run the code

# Create the Hugging Face API client with the upload token and the Data Store endpoint URL
api = HfApi(endpoint=f"http://{DATASTORE_HOSTNAME}/v1/hf", token="")

repo_type = "dataset"
repo_id = "prueba" # Update this before you run the code
folder_path = "C://Projects//NeMo_Evaluator//" # Update this before you run the code

# create the repo
url = api.create_repo(
    repo_id=repo_id,
    repo_type=repo_type,
)

# Upload the dataset file to the Data Store.
upload_url = api.upload_folder(
    repo_id=repo_id, 
    folder_path=folder_path,
    repo_type=repo_type)

print(f"Uploaded File to {upload_url}")






class Nemo_Task:

    completion_task = """
    "completion-task":{
                "type": "completion",
                "params": {
                    "template": "Respponde a la siguiente pregunta: {{input}}\n Respuesta:"
                 },
                "metrics": {
                    "similaridad": {
                        "type": "llm-judge",
                        "params": {
                            "model": {
                                "api_endpoint": {
                                    "url": "http://host.docker.internal:1234/v1",
                                    "model_id": model_id,
                                }
                            },
                            "template": {
                                "messages": [
                                    {
                                        "role": "system",
                                        "content": leer_prompt("system"),
                                        "max_tokens": 100,
                                        "temperature": 0,
                                        "top_p": 0.9,
                                    },
                                    {
                                        "role": "user",
                                        "content": leer_prompt("similarity"),
                                    },
                                ]
                            },
                            "scores": {
                                "similaridad_score": {
                                    "type": "float",
                                    "parser": {
                                        "type": "regex",
                                        "pattern": pattern_score,
                                    },
                                }
                            },
                        },
                    },
                }
            }"
            """
