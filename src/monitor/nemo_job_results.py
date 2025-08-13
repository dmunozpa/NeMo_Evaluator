from nemo_microservices import NeMoMicroservices

# Initialize the client
client = NeMoMicroservices(
    base_url="http://localhost:7331"
)

# Download job logs
job_id = "eval-GhcbhYqDYevDRMwCxopo4j"



# Get job results
results = client.evaluation.jobs.results(job_id)

# Access the results
print(f"Result ID: {results.id}")
print(f"Job ID: {results.job}")
print(f"Tasks: {results.tasks}")
print(f"Groups: {results.groups}")

# Download evaluation results
results_zip = client.evaluation.jobs.download_results(job_id)

# Save to file
results_zip.write_to_file(f'./result/Result_{job_id}.zip')
    
print("Download completed.")