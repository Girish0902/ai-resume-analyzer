import google.generativeai as genai
import os
import toml

# Load secrets
try:
    secrets = toml.load(".streamlit/secrets.toml")
    api_key = secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    print("Writing ALL models to model_list.txt...")
    with open("model_list.txt", "w") as f:
        for m in genai.list_models():
            f.write(m.name + "\n")
    print("Done")
except Exception as e:
    print(f"Error: {e}")
