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

template = """
You are an expert political speech analyst, specialized in identifying the core components of populist rhetoric.

Your task is to analyze the provided `TEXT_TO_ANALYZE` and determine the presence of populist language.

Core Populism Criteria

A statement is considered populist if it establishes an antagonistic, moralistic relationship between a "virtuous people" and a "corrupt elite"

1.  Anti-Elitism (Required for Populism): Is there a moralizing, pejorative, or strong negative reference to the perceived elite (e.g., politicians, bankers, government, speculators)?
2.  People-Centrism (Required for Populism): Is there a moralizing, positive, or explicit claim to represent "the virtuous people" or a representative part of them (e.g., "taxpayers," "workers," "the nation")?
3.  Moral Dichotomy (Required): Is the language used to describe the elite and the people based on a simple, moral divide (good vs. evil, virtuous vs. corrupt)?

Host Ideology (If Populism is Present)

If populism is present (i.e., if Anti-Elitism and People-Centrism are both identified), determine the attached host ideology that "thickens" the statement:

  * Left-Wing: Focuses on class, socio-economic deprivation, or antagonism against financial/capitalist elites.
  * Right-Wing: Focuses on nativism, national identity, or antagonism/exclusion directed at non-native groups (e.g., immigrants, asylum seekers).

Input:

  * `TEXT_TO_ANALYZE`: <<INSERT TEXT HERE>>

Output format (JSON):

```json
{
  "is_populist": true/false,
  "anti_elitism_detected": true/false,
  "people_centrism_detected": true/false,
  "moral_dichotomy_summary": "Summary of the moral framing, or 'Not detected' if absent.",
  "host_ideology": "Left-Wing" / "Right-Wing" / "None" / "Not Applicable"
}
```
"""

def enviar_prompt(prompt, modelo="gemma3:12b"):
    """
    Aquí podéis ver los modelos desplegados: http://156.35.160.77:11434/api/tags
    """

    url = "http://156.35.160.77:11434/api/generate"

    data = {
        "model": modelo,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=data)

    return response.json()["response"]

def main():
    textos = [
        "A Syrian with 4 wives and 23 children already costs the German taxpayer 400,000 euros per year in support, without ever having contributed a single cent.",
        "For tenants, this government inaction is really costing them dearly.",
        "In great haste, you stumble through the country with your policies, hastily passing one asylum package after another.",
        "The deregulation of financial markets is what initially sparked dollar signs in the eyes of speculators.",
        "The opposition is already on an intellectual summer break.",
        "This is class warfare from above; this is class warfare in the interests of the wealthy and the propertied against the majority of taxpayers on this earth.",
        "We do not demand any social policy measures for these people, but we demand: Stop the permanent social exclusion!",
        "You are the ones who are widening the gender pay gap by trampling upon poor German female retirees, while lavishly giving money to asylum seekers, who are predominantly young and male."
    ]

    for texto in textos:
        print(f"Texto: {texto}")

        prompt = template.replace("<<INSERT TEXT HERE>>", texto)

        respuesta = enviar_prompt(prompt)

        if "```json" in respuesta:
            partes = respuesta.split("```json")
            respuesta= partes[1].split("```")[0]

        print(respuesta)
        print("----")

if __name__ == '__main__':
    main()