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
                    "model": {
                        "api_endpoint": {
                            "url": "http://host.docker.internal:1234/v1",
                            "model_id": model_id,
                        }
                    },
                    "template": {
                        "messages": [
                            {"role": "user", "content": "{{input}}"},
                            {"role": "assistant", "content": "{{prediction}}"},
                        ]
                    },
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
        "dataset": {
            "files_url": "file://C:/Projects/NeMo_Evaluator/src/demo/training_data.json"
        }
    }
)

# Get the job ID and status
job_id = job.id
print(f"Job ID: {job_id}")
print(f"Job status: {job.status}")
print(f"Created at: {job.created_at}")
print(f"Updated at: {job.updated_at}")
