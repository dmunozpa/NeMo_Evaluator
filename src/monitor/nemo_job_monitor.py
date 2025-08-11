import os
from nemo_microservices import NeMoMicroservices
from datetime import datetime

# Initialize the client
client = NeMoMicroservices(
    base_url="http://localhost:7331"
)

# List all evaluation jobs
jobs = client.evaluation.jobs.list()

# Iterate through the jobs
print("| Job ID \t| Status \t| Created | Updated | Processing Time")
for job in jobs:
    diff = round((job.updated_at - job.created_at).total_seconds(), 2)
    print(f"| {job.id} | {job.status} | {job.created_at} |{job.updated_at} | {diff} seg ")