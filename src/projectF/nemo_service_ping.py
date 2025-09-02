from openai import OpenAI
import os

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = "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"
)

message = "Ping"

#model_id = "meta/llama-3.3-70b-instruct"
model_id = "nvidia_llama-3.1-nemotron-nano-8b-v1"

completion = client.chat.completions.create(
  model=model_id,
  messages=[{"role":"user","content":f"{message}"}],
  temperature=0.2,
  top_p=0.7,
  max_tokens=1024,
  stream=False
)

print(completion.choices[0].message)
