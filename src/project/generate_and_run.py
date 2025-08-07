import json
import requests

def leer_prompt(nombre):
    with open(f"prompts/{nombre}.prompt", encoding="utf-8") as f:
        return f.read()

with open("dataset.json", encoding="utf-8") as f:
    dataset = json.load(f)

payload = {
    "evaluator": {
        "type": "llmAsJudge",
        "llmAsJudge": {
            "implementation": "openai",
            "model": "gpt-4",
            "endpoint": "http://localhost:8000",
            "prompts": [
                {
                    "name": "claridad",
                    "prompt": leer_prompt("claridad"),
                    "scoring": "numeric",
                    "scaleMin": 1,
                    "scaleMax": 5
                },
                {
                    "name": "completitud",
                    "prompt": leer_prompt("completitud"),
                    "scoring": "numeric",
                    "scaleMin": 1,
                    "scaleMax": 5
                },
                {
                    "name": "tono_adecuado",
                    "prompt": leer_prompt("tono_adecuado"),
                    "scoring": "numeric",
                    "scaleMin": 1,
                    "scaleMax": 5
                }
            ]
        }
    },
    "data": {
        "source": "inline",
        "format": "json",
        "instances": dataset
    }
}

response = requests.post("http://localhost:8080/v1/evaluation/jobs", json=payload)

print("Status code:", response.status_code)
try:
    print("Response JSON:", json.dumps(response.json(), indent=2, ensure_ascii=False))
except:
    print("Response text:", response.text)
