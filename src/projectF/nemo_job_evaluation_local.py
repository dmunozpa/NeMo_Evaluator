import os
import httpx
from nemo_microservices import NeMoMicroservices

# Initialize the client
client = NeMoMicroservices(base_url="http://localhost:7331")


httpx.Timeout(900.0)

def leer_prompt(name):
    with open(f"./prompts/{name}.prompt", encoding="utf-8") as f:
        return f.read()




#model_id = "openai/gpt-oss-20b"
model_id = "nvidia_llama-3.1-nemotron-nano-8b-v1"
base_url = "http://host.docker.internal:1234/v1"


#model_id = "meta/llama-3.3-70b-instruct"
#base_url = "https://integrate.api.nvidia.com/v1"

metrica = "helpfulness"

pattern_score = "METRIC_VALUE: (\\d)"

# METRIC_VALUE:\s*(\d+(?:\.\d+)

# Run a combined metrics live evaluation
job = client.evaluation.jobs.create(
    config={
        "project": "demo_oxigeno",
        "type": "custom",
        "timeout": None,
        "params":{
          "parallelism" : 10,  
        },
        "tasks": {
            f"Task_metrica_{metrica}": {
                "type": "data",
                "metrics": {
                    f"{metrica}_{model_id}": {
                        "type": "llm-judge",
                        "params": {
                            "model": {
                                "api_endpoint": {
                                    "url": base_url,
                                    "model_id": model_id,
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
                                        "content": leer_prompt(f"{metrica}"),
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
                    },
                },
            }
        },
    },
    target={
        "type": "rows",
        "rows": [
            {
                "id": "1A",
                "Consulta": "¿Qué documentos necesito para solicitar la Hipoteca Joven de Unicaja?",
                "Respuesta": "Para solicitar productos hipotecarios necesitas documentación. Consulta en oficina.",
            },
            {
                "id": "1B",
                "Consulta": "¿Puedo financiar el 100% con la Hipoteca Joven de Unicaja?",
                "Respuesta": "Las hipotecas tienen diferentes porcentajes de financiación. Hay varios tipos disponibles.",
            },
            {
                "id": "1C",
                "Consulta": "¿Qué documentos necesito para solicitar la Hipoteca Joven de Unicaja?",
                "Respuesta": "Para la Hipoteca Joven de Unicaja necesitarás: DNI, últimas tres nóminas, declaración de la renta, extractos bancarios de 6 meses, y tasación del inmueble. Recuerda que debes ser menor de 35 años y la vivienda debe ser tu residencia habitual en España.",
            },
        ],
    },
)

'''
* Ejemplo 1A:
- Consulta: "¿Qué documentos necesito para solicitar la Hipoteca Joven de Unicaja?"
- Respuesta IA: "Para solicitar productos hipotecarios necesitas documentación. Consulta en oficina."
- Puntuación esperada: 1 - No proporciona información específica de Unicaja ni útil

* Ejemplo 1B:
- Consulta: "¿Puedo financiar el 100% con la Hipoteca Joven de Unicaja?"
- Respuesta IA: "Las hipotecas tienen diferentes porcentajes de financiación. Hay varios tipos disponibles."
- Puntuación esperada: 1 - Respuesta vaga que no menciona el programa ICO de Unicaja

* Ejemplo 3A:
- Consulta: "¿Qué documentos necesito para solicitar la Hipoteca Joven de Unicaja?"
- Respuesta IA: "Para la Hipoteca Joven de Unicaja necesitarás: DNI, últimas tres nóminas, declaración de la renta, extractos bancarios de 6 meses, y tasación del inmueble. Recuerda que debes ser menor de 35 años y la vivienda debe ser tu residencia habitual en España."
- Puntuación esperada: 3 - Respuesta completa con requisitos específicos de Unicaja
'''

# Get the job ID and status
job_id = job.id
print(f"Job ID: {job_id}")
print(f"Job status: {job.status}")
print(f"Created at: {job.created_at}")
print(f"Updated at: {job.updated_at}")