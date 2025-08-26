import os
from nemo_microservices import NeMoMicroservices

# Initialize the client
client = NeMoMicroservices(base_url="http://localhost:7331")


def leer_prompt(name):
    with open(f"./prompts/{name}.prompt", encoding="utf-8") as f:
        return f.read()


# model_id = "openai/gpt-oss-20b"
model_id = "nvidia_llama-3.1-nemotron-nano-8b-v1"

metrica = "standarMetrics"

pattern_score = "METRIC_VALUE: (\\d)"

# METRIC_VALUE:\s*(\d+(?:\.\d+)

# Run a combined metrics live evaluation
job = client.evaluation.jobs.create(
    config={
        "project": "demo_oxigeno",
        "type": "custom",
        "params": {"parallelism": 4},
        "tasks": {
            "qa": {
                "type": "chat-completion",
                "params": {
                    "template": {
                        "messages": [
                            {"role": "user", "content": "{{input}}"},
                            {"role": "assistant", "content": "{{prediction}}"},
                        ],
                        "max_tokens": 200,
                        "temperature": 0.7,
                        "top_p": 0.9,
                    }
                },
            },
            "metrics": {
                "bleu": {
                    "type": "bleu",
                    "params": {"references": ["{{item.ground_truth | trim}}"]},
                },
                "rouge": {
                    "type": "rouge",
                    "params": {"ground_truth": "{{item.ground_truth | trim}}"},
                },
                "f1": {
                    "type": "f1",
                    "params": {"ground_truth": "{{item.ground_truth | trim}}"},
                },
                "em": {
                    "type": "em",
                    "params": {"ground_truth": "{{item.ground_truth | trim}}"},
                },
            },
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
            },
            {
                "id": "2",
                "input": "¿Cual es la edad máxima de un ser humano?",
                "prediction": "130 años",
                "ground_truth": "122 años y 164 días",
            },
            {
                "id": "3",
                "input": "¿Cual es la edad máxima de un ser humano?",
                "prediction": "No dispongo de esa información",
                "ground_truth": "122 años y 164 días",
            },
        ],
    },
)

# Get the job ID and status
job_id = job.id
print(f"Job ID: {job_id}")
print(f"Job status: {job.status}")
print(f"Created at: {job.created_at}")
print(f"Updated at: {job.updated_at}")
