import os
from nemo_microservices import NeMoMicroservices

# Initialize the client
client = NeMoMicroservices(
    base_url="http://localhost:7331"
)

# List all evaluation jobs
jobs = client.evaluation.jobs.list()

# Iterate through the jobs
print("\t| Job ID \t| Status \t| Created |")
for job in jobs:
    print(f"| {job.id} | {job.status} | {job.created_at} | ")