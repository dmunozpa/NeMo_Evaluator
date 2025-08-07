import os
from nemo_microservices import NeMoMicroservices

# Initialize the client
client = NeMoMicroservices(
    base_url="http://localhost:7331"
)


# Download evaluation results
results_zip = client.evaluation.jobs.download_results("eval-UroEGZoCEXRs66hqWQkJby")

# Save to file
results_zip.write_to_file('result.zip')
    
print("Download completed.")