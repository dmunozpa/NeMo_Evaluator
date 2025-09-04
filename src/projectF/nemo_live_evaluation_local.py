import os
import httpx
from nemo_microservices import NeMoMicroservices

# Initialize the client
client = NeMoMicroservices(base_url="http://localhost:7331")


httpx.Timeout(900.0)


def leer_prompt(name):
    with open(f"./prompts/{name}.prompt", encoding="utf-8") as f:
        return f.read()


# model_id = "openai/gpt-oss-20b"
model_id = "nvidia_llama-3.1-nemotron-nano-8b-v1"
base_url = "http://host.docker.internal:1234/v1"


# model_id = "meta/llama-3.3-70b-instruct"
# base_url = "https://integrate.api.nvidia.com/v1"

metrica = "hallucination_rate"

pattern_score = "METRIC_VALUE: (\\d)"

# METRIC_VALUE:\s*(\d+(?:\.\d+)

# Run a combined metrics live evaluation
response = client.evaluation.live(
    config={
        "project": "demo_oxigeno",
        "type": "custom",
        "params": {"request_timeout": 999, "parallelism": 2},
        "tasks": {
            f"metrica_{metrica}_formato_nuevo": {
                "type": "data",
                "metrics": {
                    f"{metrica}_{model_id}": {
                        "type": "llm-judge",
                        "params": {
                            "model": {
                                "api_endpoint": {
                                    "url": base_url,
                                    "model_id": model_id,
                                    "api_key": "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",
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
                "prediction": "Viva el Real Madrid",
                "ground_truth": "Puedes solicitar la Hipoteca Oxigeno siempre que la del plazo de esta y edad del mayor de los titulares no supere los 75 años en el caso de las primeras residencias o los 70 años en las segundas.",
            },
        ],
    },
)

# Get the job ID and status
print(f"Status: {response.status}")
print(f"Results: {response.result}")


# Download evaluation results

# Save to file
# results_zip.write_to_file(f'./result/Result_1.zip')
