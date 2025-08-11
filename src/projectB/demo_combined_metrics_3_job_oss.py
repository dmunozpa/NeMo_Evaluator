import os
from nemo_microservices import NeMoMicroservices

# Initialize the client
client = NeMoMicroservices(
    base_url="http://localhost:7331"
)


def leer_prompt(name):
    with open(f"./prompts/{name}.prompt", encoding="utf-8") as f:
        return f.read()

model_id = "openai/gpt-oss-20b"
#model_id = "nvidia_llama-3.1-nemotron-nano-8b-v1"


# Run a combined metrics live evaluation
job = client.evaluation.jobs.create(
    config={
        "project": "demo_3_metricas",
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
                                    "model_id": model_id
                                }
                            },
                            "template": {
                                "messages": [
                                    {
                                        "role": "system",
                                        "content": "Your task is to evaluate the semantic similarity between two responses. Response just hte metric with this format: SIMILARITY: X. "
                                    },
                                    {
                                        "role": "user",
                                        "content": leer_prompt("similarity")
                                    }
                                ]
                            },
                            "scores": {
                                "similarity": {
                                    "type": "int",
                                    "parser": {
                                        "type": "regex",
                                        "pattern": "SIMILARITY: (\\d)"
                                    }
                                }
                            }
                        }
                    },
                    "completitud": {
                        "type": "llm-judge",
                        "params": {
                            "model": {
                                "api_endpoint": {
                                    "url": "http://host.docker.internal:1234/v1",
                                    "model_id": model_id
                                }
                            },
                            "template": {
                                "messages": [
                                    {
                                        "role": "system",
                                        "content": "Your task is to evaluate the semantic completness between two responses."
                                    },
                                    {
                                        "role": "user",
                                        "content": leer_prompt("COMPLETNESS")
                                    }
                                ]
                            },
                            "scores": {
                                "completness": {
                                    "type": "int",
                                    "parser": {
                                        "type": "regex",
                                        "pattern": "COMPLETNESS: (\\d)"
                                    }
                                }
                            }
                        }
                    },
                    "tono_adecuado": {
                        "type": "llm-judge",
                        "params": {
                            "model": {
                                "api_endpoint": {
                                    "url": "http://host.docker.internal:1234/v1",
                                    "model_id": model_id
                                }
                            },
                            "template": {
                                "messages": [
                                    {
                                        "role": "system",
                                        "content": "Your task is to evaluate the semantic tone between two responses."
                                    },
                                    {
                                        "role": "user",
                                        "content": leer_prompt("tono_adecuado")
                                    }
                                ]
                            },
                            "scores": {
                                "tono_resultado": {
                                    "type": "int",
                                    "parser": {
                                        "type": "regex",
                                        "pattern": "TONO_RESULTADO: (\\d)"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    },
    target={
        "type": "rows",
        "rows": [
            {
                "id": "1",
                "input": "¿Cuál es el tipo de interés actual de un depósito a plazo fijo?",
                "prediction": "El tipo de interés es del 2,5% para depósitos a 12 meses.",
                "ground_truth": "Actualmente, los depósitos a plazo fijo a 12 meses ofrecen un interés del 2,5%.",
            },
            {
                "id": "2",
                "input": "¿Cuáles son los requisitos para abrir una cuenta corriente?",
                "prediction": "Debes presentar tu DNI y una factura reciente.",
                "ground_truth": "Se requiere el DNI, una factura actual y un justificante de ingresos.",
            }
        ]
    }
)

# Get the job ID and status
job_id = job.id
print(f"Job ID: {job_id}")
print(f"Job status: {job.status}")

# Get job details
job = client.evaluation.jobs.retrieve(job_id)

# Get the status and other details
print(f"Job ID: {job.id}")
print(f"Job status: {job.status}")
print(f"Created at: {job.created_at}")
print(f"Updated at: {job.updated_at}")