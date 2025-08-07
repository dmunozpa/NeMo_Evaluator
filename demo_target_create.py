from nemo_microservices import NeMoMicroservices

# Initialize the client
client = NeMoMicroservices(
    base_url="http://localhost:7331"
)


# Create a rows target
client.evaluation.targets.create(
    type="rows",
    name="my-target-rows-1",
    namespace="POC",
    rows=[
        {
            "prompt": "Do you agree?",
            "response": "yes",
            "expected": "yes"
        },
        {
            "prompt": "What is the color of the sky?",
            "response": "Blue",
            "expected": "blue"
        }
        # Add more rows as needed
    ]
)

print("Rows target created successfully")