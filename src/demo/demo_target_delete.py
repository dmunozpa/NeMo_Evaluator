import os
import requests

from nemo_microservices import NeMoMicroservices

# Initialize the client
client = NeMoMicroservices(
    base_url="http://localhost:7331"
)


# Delete an evaluation target
response = client.evaluation.targets.delete(
    namespace="POC",
    target_name="my-target-rows-2"
)

print(f"Target deleted: {response.message}")
print(f"Deleted at: {response.deleted_at}")