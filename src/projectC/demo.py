import os
from nemo_microservices import NeMoMicroservices

# Initialize the client
client = NeMoMicroservices(base_url="http://localhost:7331")


def leer_prompt(name):
    with open(f"./prompts/{name}.prompt", encoding="utf-8") as f:
        return f.read()


model_id = "openai/gpt-oss-20b"
#model_id = "nvidia_llama-3.1-nemotron-nano-8b-v1"

pattern_score = "METRIC_VALUE: (\\d)"
# METRIC_VALUE:\s*(\d+(?:\.\d+)?)

# Run a combined metrics live evaluation
job = client.evaluation.jobs.create(
    config={
        "project": "demo_oxigeno",
        "type": "custom",
        "timeout": None,
        "tasks": {
            "metricas_combinadas_3": {
                "type": "data",
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
                    "completitud": {
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
                                        "content": leer_prompt("COMPLETNESS"),
                                    },
                                ]
                            },
                            "scores": {
                                "completitud_score": {
                                    "type": "float",
                                    "parser": {
                                        "type": "regex",
                                        "pattern": pattern_score,
                                    },
                                }
                            },
                        },
                    },
                    "tono_adecuado": {
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
                                        "content": leer_prompt("tono_adecuado"),
                                    },
                                ]
                            },
                            "scores": {
                                "tono_resultado": {
                                    "type": "float",
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
