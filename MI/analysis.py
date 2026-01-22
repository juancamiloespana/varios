import pandas as pd
import time
import numpy as np
import os
import google.genai as genai
from google.genai import types
import json
from pydantic import BaseModel
import openpyxl



data=pd.read_csv("airline.csv")

data_sam=data
# Create a new column removing the starting airline tag (e.g. @Airline)
data_sam['text_no_tag'] = data_sam['text'].str.replace(r'^@\w+\s*', '', regex=True)


client = genai.Client()

# List available models to verify access
print("--- Available Models ---")
for model in client.models.list():
    print(model.name)
print("------------------------")

# 1. Select a larger sample to define the categories (e.g., 50 tweets)
# We use the regex to clean them on the fly for the sample list
taxonomy_sample = data_sam['text_no_tag'].tolist()

# --- Token Usage & Capacity Analysis ---

user_prompt=f"""You are a Senior Customer Experience Analyst for a major airline.
Your task is to analyze the provided customer tweets to define a structured taxonomy of Categories and Subcategories.

The taxonomy will be used for root cause analysis, so definitions must be precise and actionable.

Do not classify the individual tweets. Return only the taxonomy definitions based on the themes observed below:
\n{json.dumps(taxonomy_sample)}"""

# Count tokens for the sample prompt
count_resp = client.models.count_tokens(model='gemini-2.0-flash-lite', contents=user_prompt)

print(f"\nTokens used for {len(taxonomy_sample)} tweets: {count_resp.total_tokens}")

# --- Strategy: Create Taxonomy from Sample ---


# 2. Define the schema for Categories and Subcategories
class Category(BaseModel):
    category: str
    subcategories: list[str]
    description: str | None = None



for attempt in range(5):
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash-lite',
            contents=user_prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=list[Category],
                max_output_tokens=3000)
        )
        break
    except Exception as e:
        print(f"Attempt {attempt + 1} failed: {e}")
        if attempt == 4:
            raise
        time.sleep(2 ** attempt) # Exponential backoff


taxonomy = json.loads(response.text)
print(json.dumps(taxonomy, indent=2))

taxonomy_df = pd.DataFrame(taxonomy)
taxonomy_df_long = taxonomy_df.explode('subcategories').reset_index(drop=True)

taxonomy_df_long.to_csv("taxonomy.csv", index=False)
taxonomy_df_long.to_excel("taxonomy.xlsx", index=False)






client.close()

    
  
