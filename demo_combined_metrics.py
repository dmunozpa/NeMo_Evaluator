import os
from nemo_microservices import NeMoMicroservices

# Initialize the client
client = NeMoMicroservices(
    base_url="http://localhost:7331"
)


# Run a combined metrics live evaluation
response = client.evaluation.live(
    config={
        "type": "custom",
        "tasks": {
            "qa": {
                "type": "data",
                "metrics": {
                    "accuracy": {
                        "type": "string-check",
                        "params": {
                            "check": ["{{some_output}}", "contains", "{{expected}}"]
                        }
                    },
                    "accuracy-2": {
                        "type": "llm-judge",
                        "params": {
                            "model": {
                                "api_endpoint": {
                                    "url": "http://host.docker.internal:1234/v1",
                                    "model_id": "nvidia_llama-3.1-nemotron-nano-8b-v1"
                                }
                            },
                            "template": {
                                "messages": [
                                    {
                                        "role": "system",
                                        "content": "Your task is to evaluate the semantic similarity between two responses."
                                    },
                                    {
                                        "role": "user",
                                        "content": "Respond in the following format SIMILARITY: 4. The similarity should be a score between 0 and 10.\n\nRESPONSE 1: {{some_output}}\n\nRESPONSE 2: {{expected}}.\n\n"
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
                    }
                }
            }
        }
    },
    target={
        "type": "rows",
        "rows": [
            {
                "some_input": "Do you agree?",
                "some_output": "yes",
                "expected": "yes"
            }
        ]
    }
)

print(f"Status: {response.status}")
print(f"Results: {response.result}")