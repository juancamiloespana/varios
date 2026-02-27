"""
Este script muestra cómo utilizar un modelo lingüístico para procesar textos usando
una plantilla para el prompt.

Dicha plantilla se basa en el trabajo expuesto en el artículo:

Erhard, L., Hanke, S., Remer, U., Falenska, A., & Heiberger, R. H. (2025).
PopBERT. Detecting populism and its host ideologies in the German Bundestag.
Political Analysis, 33(1), 1-17.

https://scholar.google.com/scholar?cluster=4674681322621775846&hl=en&as_sdt=0,5

Una declaración se considera populista si contiene una referencia moralizante
tanto a la 'élite corrupta' (Anti-Elitismo) como al 'pueblo virtuoso'
(People-Centrism).

En consecuencia, el modelo lingüístico debe clasificar el texto en cuatro
dimensiones independientes:

- Anti-Elitism: Crítica peyorativa y moralizante a la élite.
- People-Centrism: Referencia positiva y moralizante al 'pueblo' o a un subgrupo
  representativo (p. ej., 'contribuyentes', 'inquilinos' o 'agricultores').
- Ideología de izquierda: la retórica se enmarca en torno a la privación
  socioeconómica/de clase o al antagonismo contra las élites financieras.
- Ideología de derecha: la retórica se enmarca en torno al nativismo o al
  antagonismo dirigido a grupos no nativos (p. ej., 'política de asilo',
  'inmigrantes').

Así, un texto será considerado populista solo cuando Anti-Elitism y People-Centrism
estén presentes.

Los textos de ejemplo proceden de la Tabla 3 del mismo artículo.

Más sobre ingeniería de prompts: https://www.promptingguide.ai/

El enfoque seguido en este script se denomina "zero-shot", puesto que se utiliza
un modelo lingüístico general que no ha sido entrenado previamente para identificar
textos populistas y al que tampoco se le muestran ejemplos específicos para la
tarea (few-shot). En un enfoque zero-shot el modelo interpreta y clasifica los
textos basándose únicamente en la descripción de la tarea incluida en el prompt,
aplicando lo aprendido de manera general a partir de los textos de entrenamiento.

"""

import requests
import pandas as pd
import json

data=pd.read_csv("airline.csv")

data_sam=data
#data_sam=data.sample(5000, random_state=42)
# Create a new column removing the starting airline tag (e.g. @Airline)
data_sam['text_no_tag'] = data_sam['text'].str.replace(r'^@\w+\s*', '', regex=True)
taxonomy_sample = data_sam['text_no_tag'].tolist()



template = f"""

You are a Senior Customer Experience Analyst for a major airline. Your task is to analyze the provided customer tweets to define a structured taxonomy of Categories and Subcategories.

The taxonomy will be used for root cause analysis, so definitions must be precise and actionable.

Do not classify the individual tweets. Return only the taxonomy definitions based on the themes observed below:

Input:

  * {json.dumps(taxonomy_sample)}

Output format (JSON):

```json
{{
  "type": "object",
  "properties": {{
    "category": {{"type": "string"}},
    "subcategories": {{"type": "array", "items": {{"type": "string"}}}},
    "description": {{"type": "string"}}
  }},
  "required": ["category", "subcategories"]
}}
```
"""


###models: 
#### deepseek-r1:14b

##### qwen2.5:7b
def enviar_prompt(prompt, modelo="gemma3:12b"):
    """
    Aquí podéis ver los modelos desplegados: http://156.35.160.77:11434/api/tags
    """

    url = "http://156.35.160.77:11434/api/generate"

    data = {
            "model": modelo,
            "prompt": prompt,
            "stream": False
            
                 #
        }

    response = requests.post(url, json=data)

    return response.json()["response"]




prompt = template

respuesta = enviar_prompt(prompt)

if "```json" in respuesta:
    partes = respuesta.split("```json")
    respuesta= partes[1].split("```")[0]

print(respuesta)
print("----")



import pandas as pd
import json

data_pd=pd.DataFrame(json.loads(respuesta))

data_long_gemma = data_pd.explode('subcategories').reset_index(drop=True)

data_long_gemma.to_csv("gemma_all.csv", index=False)



