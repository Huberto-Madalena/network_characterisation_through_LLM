import os
from google import genai

def generate_ai_analysis(system_prompt: str, user_prompt: str) -> str:
    """
    AI analysis logic
    """
    #path to api key
    key_file_path = "/home/osprey/network_characterisation_build2/config/api_key.txt"
    
    # 2.check path and existence of api key file
    try:
        with open(key_file_path, 'r') as f:
             
            API_KEY = f.read().strip()
    except FileNotFoundError:
        return f"[-] api-key file in '{key_file_path}' not found."
    
    # 3. in case the APi file is empty:
    if not API_KEY:
        return "[-] Empty api-key file. Insert API key in file!"

    
    try:
        client = genai.Client(api_key=API_KEY)
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        
        config_path = "/home/osprey/network_characterisation/config/models.txt"
        fallback_models = []
        
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("models/"):
                        model_name = line.split("models/")[1]
                        invalid_keywords = ['embedding', 'imagen', 'veo', 'aqa', 'tts', 'audio', 'lyria', 'robotics', 'computer-use']
                        if any(kw in model_name for kw in invalid_keywords):
                            continue
                        fallback_models.append(model_name)
        
        # default model. check config for list of models
        if not fallback_models:
            fallback_models = ['gemini-2.0-flash', 'gemini-1.5-flash']

        # iterating through different models, in case dfault one is unavailable
        for model_name in fallback_models:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=full_prompt
                )
                print(f"[+] Analysis created with model: {model_name}")
                return response.text
                
            except Exception as e:
                print(f"[*] Model '{model_name}' not responding: {e}")
                continue
                
        return "[-] all models are either unavailable or out of tokens."
        
    except Exception as fatal_error:
        return f"[-]initialising error : {fatal_error}"
