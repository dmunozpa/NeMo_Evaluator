import os, json
from nemo_microservices import NeMoMicroservices
from datetime import datetime


# Initialize the client
client = NeMoMicroservices(base_url="http://localhost:7331")

# @TODO Eliminar el API Key
os.environ["NVIDIA_API_KEY"] = (
    "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"
)


def leer_prompt(name):

    with open(
        f"C:/Projects/NeMo_Evaluator/src/projectF/prompts/{name}.prompt",
        encoding="utf-8",
    ) as f:
        return f.read()


### MODELO EN ONLINE
# model_id = "meta/llama-3.3-70b-instruct"
model_id = "meta/llama-3.1-8b-instruct"
# model_id = "deepseek-ai/deepseek-v3.1"
# model_id = "nvidia/llama-3.3-nemotron-super-49b-v1.5"
base_url = "https://integrate.api.nvidia.com/v1"


pattern_score = "METRIC_VALUE: (\\d)"


def build_config(
    project_name, base_url, model_id, api_key, lista_metricas, rows, pattern_score
):
    """
    Construye dinámicamente la configuración para client.evaluation.live

    Args:
        project_name (str): Nombre del proyecto
        base_url (str): Endpoint base del modelo
        model_id (str): ID del modelo
        api_key (str): API key del modelo
        lista_metricas (list): Listas de métricas por grupo (ej: ["relevancia", "precision"])
        rows (list[dict]): Lista de objetos tipo row (id, Consulta, Respuesta)
        pattern_score (str): Patrón regex para parsear scores

    Returns:
        dict: Configuración lista para pasarse a client.evaluation.live
    """

    def make_metric_config(metrica):
        """Construye la configuración de una métrica individual"""
        return {
            f"{metrica}_{model_id}": {
                "type": "llm-judge",
                "params": {
                    "model": {
                        "api_endpoint": {
                            "url": base_url,
                            "model_id": model_id,
                            "api_key": api_key,
                        }
                    },
                    "extra": {
                        "batch-size": 2, 
                        "max-tokens": 10, 
                        "temperature": 0.1
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
                                "content": leer_prompt(metrica),
                            },
                        ]
                    },
                    "scores": {
                        f"{metrica}_score": {
                            "type": "int",
                            "parser": {
                                "type": "regex",
                                "pattern": pattern_score,
                            },
                        }
                    },
                },
            }
        }

    # Creamos una Task por cada métrica
    tasks = {}
    for metrica in lista_metricas:
        tasks[f"Task_{metrica}"] = {
            "type": "data",
            "metrics": make_metric_config(metrica),
        }

    # --- Config principal ---
    config = {
        "project": project_name,
        "type": "custom",
        "timeout": None,
        "params": {
            "parallelims": 10,
            "max-tokens": 10,
        },
        "tasks": tasks,
    }

    target = {
        "type": "rows",
        "rows": rows,
    }

    return config, target


# Ejemplo de uso
lista_metricas = [
    "toxicidad",
    "tonalidad",
    "sesgo",
    "claridad",
    "calidad_razonamiento",
    "coherencia",
    "helpfulness",
    "sentimiento",
    "instruccion_following",
]


rows = [
    {
        "id": "1C",
        "Consulta": "¿Qué documentos necesito para solicitar la Hipoteca Joven de Unicaja?",
        "Respuesta": "Para la Hipoteca Joven de Unicaja necesitarás: DNI, últimas tres nóminas, declaración de la renta, extractos bancarios de 6 meses, y tasación del inmueble. Recuerda que debes ser menor de 35 años y la vivienda debe ser tu residencia habitual en España.",
    },
]

config, target = build_config(
    project_name="demo_oxigeno",
    base_url=base_url,
    model_id=model_id,
    api_key="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",  # usa tu API key real
    lista_metricas=lista_metricas,
    rows=rows,
    pattern_score=pattern_score,
)


now = datetime.now()

response = client.evaluation.live(
    config=config,
    target=target,
)

latencia = datetime.now() - now
print(f"Latencia: {latencia.seconds} seg.")

# Get the job ID and
# print status
print(f"Status: {response.status}")
print(f"Results: {response.result}")
print(f"Status Details: {response.status_details}")

id = response.result.id

log = response.logs
with open(f"results_{id}.json", "w+", encoding="utf-8") as jf:
    json.dump(log, jf, ensure_ascii=False, indent=4)


EvaluationStatusDetails = response.status_details
evalutationResult_json = response.result.model_dump_json


# Función para serializar objetos no compatibles con JSON
def custom_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif hasattr(obj, "__dict__"):
        return {key: custom_serializer(value) for key, value in obj.__dict__.items()}
    elif isinstance(obj, dict):
        return {key: custom_serializer(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [custom_serializer(item) for item in obj]
    else:
        return obj


# Ejemplo de uso con tu objeto (reemplaza 'evaluation' con tu instancia real)
json_output = json.dumps(response.result, default=custom_serializer, indent=2)

with open(f"response_{id}.json", "w+") as f:
    f.write(json_output)
