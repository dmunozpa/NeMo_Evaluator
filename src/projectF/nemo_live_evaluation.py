import os
from nemo_microservices import NeMoMicroservices

# Initialize the client
client = NeMoMicroservices(base_url="http://localhost:7331")

# @TODO Eliminar el API Key
os.environ['NVIDIA_API_KEY'] = "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"

def leer_prompt(name):
    
    with open(f"C:/Projects/NeMo_Evaluator/src/projectF/prompts/{name}.prompt", encoding="utf-8") as f:
        return f.read()

### MODELO EN LOCAL
#model_id = "openai/gpt-oss-20b"
#model_id = "nvidia_llama-3.1-nemotron-nano-8b-v1"
#base_url = "http://host.docker.internal:1234/v1"

### MODELO EN ONLINE
#model_id = "meta/llama-3.3-70b-instruct"
#model_id = "deepseek-ai/deepseek-v3.1"
model_id = "nvidia/llama-3.3-nemotron-super-49b-v1.5"
base_url = "https://integrate.api.nvidia.com/v1"

metrica = "hallucination_rate"

pattern_score = "METRIC_VALUE: (\\d)"

# METRIC_VALUE:\s*(\d+(?:\.\d+)

# Run a combined metrics live evaluation
response = client.evaluation.live(
    config={
        "project": "demo_oxigeno",
        "type": "custom",
        "timeout": None,
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
                                    "api_key": "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"
                                
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

EvaluationResult = response.result

print(f"Job ID: {EvaluationResult.job}")
print(f"Tasks: {EvaluationResult.tasks}")
print(f"Groups: {EvaluationResult.groups}")

Task = EvaluationResult.tasks

# Download evaluation results
#results_zip = client.evaluation.jobs.download_results(response.result.job)

# Save to file
#results_zip.write_to_file(f'./result/Result_1.zip')