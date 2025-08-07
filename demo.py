import os
from nemo_microservices import NeMoMicroservices

# Initialize the client
client = NeMoMicroservices(
    base_url="http://localhost:7331"
)

# Run a basic string check live evaluation
response = client.evaluation.live(
    config={
        "type": "custom",
        "tasks": {
            "qa": {
                "type": "data",
                "metrics": {
                    "accuracy": {
                        "type": "string-check",
                        "params": {"check": ["{{some_output}}", "contains", "{{expected}}"]}
                    }
                }
            }
        }
    },
    target={
        "name": "my-target-rows-2",
        "namespace" : "POC"
    }
)

print(f"Status: {response.status}")
print(f"Results: {response.result}")