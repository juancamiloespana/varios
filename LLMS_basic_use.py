import pandas as pd
import numpy as np
import os
from google import genai
from google.genai import types
import json
from pathlib import Path




################################################################################################################
################################################################################################################
#################### Gemini basics #############################################################################
################################################################################################################
################################################################################################################

# to confirm the api Key used
# os.environ.get("GEMINI_API_KEY")

### Setup ####
client = genai.Client()


system_prompt="Hablemos en español"
user_promt={"text": "GEmini es un sistema multiagente que usa tools"}

gen_config=types.GenerateContentConfig(
        temperature=0.9,
        candidate_count=1,
        system_instruction=system_prompt
        )


class (Basemodel)

response=client.models.generate_content(
    model='gemini-2.5-flash-lite',
    contents=user_promt,
    config=gen_config
)


print(response.text)

client.close()