import os
from nemo_microservices import NeMoMicroservices

# Initialize the client
client = NeMoMicroservices(base_url="http://localhost:7331")


def leer_prompt(name):
    with open(f"./prompts/{name}.prompt", encoding="utf-8") as f:
        return f.read()


model_id = "openai/gpt-oss-20b"
# model_id = "nvidia_llama-3.1-nemotron-nano-8b-v1"

metrica = "completness"

pattern_score = "METRIC_VALUE: (\\d)"

# METRIC_VALUE:\s*(\d+(?:\.\d+)

# Run a combined metrics live evaluation
job = client.evaluation.jobs.create(
    config={
        "project": "demo_oxigeno",
        "type": "custom",
        "timeout": None,
        "tasks": {
            f"metrica_{metrica}_formato_nuevo": {
                "type": "data",
                "metrics": {
                    f"completitud_nvidia_{model_id}": {
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
                                        "temperature": 0,
                                        "top_p": 0.9,
                                    },
                                    {
                                        "role": "user",
                                        "content": leer_prompt(f"{metrica}"),
                                    },
                                ]
                            },
                            "scores": {
                                f"{metrica}_score": {
                                    "type": "int",
                                    "parser": {
                                        "type": "regex",
                                        "pattern": pattern_score,
                                    },
                                }
                            },
                        },
                    },   
                },
            }
        },
    },
    target={
        "type": "rows",
        "rows": [
            {
                "id": "1",
                "input": "¿Hasta que edad me pueden dar una hipoteca Oxigeno?",
                "prediction": "Para primera vivienda, hasta los 75 años y hasta los 70 años segunda vivienda.",
                "ground_truth": "Puedes solicitar la Hipoteca Oxigeno siempre que la del plazo de esta y edad del mayor de los titulares no supere los 75 años en el caso de las primeras residencias o los 70 años en las segundas.",
            }
        ],
    },
)

# Get the job ID and status
job_id = job.id
print(f"Job ID: {job_id}")
print(f"Job status: {job.status}")
print(f"Created at: {job.created_at}")
print(f"Updated at: {job.updated_at}")
