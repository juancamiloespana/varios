import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os
import google.generativeai as genai
from google.generativeai import types
import json

load_dotenv()

gemini_api=os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=gemini_api)


data=pd.read_csv("airline.csv")

np.random.seed(42)


data_sam=data.sample(3)


data_sam['text']
system_promt=""

generation_config=types.GenerationConfig(
        temperature=0.9,
        system_instruction=system_prompt
    )

model = genai.GenerativeModel(
    model_name='gemini-2.5-flash-preview-09-2025',
    
)

prompt=""

response = model.generate_content(prompt, 
                                  generation_config=generation_config)


json_string = response.candidates[0].content.parts[0].text

# Parse the JSON string into a Python dictionary
data_json = json.loads(json_string)



    
  
