import os, json
from nemo_microservices import NeMoMicroservices

# Initialize the client
client = NeMoMicroservices(base_url="http://localhost:7331")

# @TODO Eliminar el API Key
os.environ['NVIDIA_API_KEY'] = "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"

def leer_prompt(name):
    
    with open(f"C:/Projects/NeMo_Evaluator/src/projectF/prompts/{name}.prompt", encoding="utf-8") as f:
        return f.read()


### MODELO EN ONLINE
#model_id = "meta/llama-3.3-70b-instruct"
model_id = "deepseek-ai/deepseek-v3.1"
#model_id = "nvidia/llama-3.3-nemotron-super-49b-v1.5"
base_url = "https://integrate.api.nvidia.com/v1"

metrica1 = "hallucination_rate"
metrica2 = "claridad"

pattern_score = "METRIC_VALUE: (\\d)"

# METRIC_VALUE:\s*(\d+(?:\.\d+)

# Run a combined metrics live evaluation
response = client.evaluation.live(
    config={
        "project": "demo_oxigeno",
        "type": "custom",
        "timeout": None,
        "params":{
          "parallelism" : 10,  
        },
        "tasks": {
            f"metrica_combiandas_formato_nuevo": {
                "type": "data",
                "metrics": {
                    f"{metrica1}_{model_id}": {
                       "type": "llm-judge",
                        "params": {
                            "model": {
                                "api_endpoint": {
                                    "url": base_url,
                                    "model_id": model_id,
                                    "api_key": "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"
                                
                                }
                            },
                            "template": {
                                "messages": [
                                    {
                                        "role": "system",
                                        "content": leer_prompt("system"),
                                        "temperature": 0,
                                        "top_p": 0.9,
                                    },
                                    {
                                        "role": "user",
                                        "content": leer_prompt(f"{metrica1}"),
                                    },
                                ]
                            },
                            "scores": {
                                f"{metrica1}_score": {
                                    "type": "int",
                                    "parser": {
                                        "type": "regex",
                                        "pattern": pattern_score,
                                    },
                                }
                            },
                        },
                    },
                    f"{metrica2}_{model_id}": {
                       "type": "llm-judge",
                        "params": {
                            "model": {
                                "api_endpoint": {
                                    "url": base_url,
                                    "model_id": model_id,
                                    "api_key": "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"
                                
                                }
                            },
                            "template": {
                                "messages": [
                                    {
                                        "role": "system",
                                        "content": leer_prompt("system"),
                                        "temperature": 0,
                                        "top_p": 0.9,
                                    },
                                    {
                                        "role": "user",
                                        "content": leer_prompt(f"{metrica2}"),
                                    },
                                ]
                            },
                            "scores": {
                                f"{metrica2}_score": {
                                    "type": "int",
                                    "parser": {
                                        "type": "regex",
                                        "pattern": pattern_score,
                                    },
                                }
                            },
                        },
                    },
                },
            }
        },
    },
    target={
        "type": "rows",
        "rows": [
            {
                "id": "1",
                "Consulta": "¿Hasta que edad me pueden dar una hipoteca Oxigeno?",
                "Respuesta": "Viva el Real Madrid",
                "ground_truth": "Puedes solicitar la Hipoteca Oxigeno siempre que la del plazo de esta y edad del mayor de los titulares no supere los 75 años en el caso de las primeras residencias o los 70 años en las segundas.",
            },
        ],
    },
)


# Get the job ID and status
print(f"Status: {response.status}")
print(f"Results: {response.result}")
print(f"Status Details: {response.status_details}" )

id = response.result.id

log = response.logs
with open(f'results_{id}.json','w+', encoding="utf-8") as jf:
    json.dump(log, jf, ensure_ascii=False, indent=4)



EvaluationStatusDetails = response.status_details
evalutationResult_json = response.result.model_dump_json


from datetime import datetime
 
# Función para serializar objetos no compatibles con JSON
def custom_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif hasattr(obj, '__dict__'):
        return {key: custom_serializer(value) for key, value in obj.__dict__.items()}
    elif isinstance(obj, dict):
        return {key: custom_serializer(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [custom_serializer(item) for item in obj]
    else:
        return obj
 
# Ejemplo de uso con tu objeto (reemplaza 'evaluation' con tu instancia real)
json_output = json.dumps(response.result, default=custom_serializer, indent=2)
 
with open(f'response_{id}.json', "w+") as f:
    f.write(json_output)