import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BEARER = os.getenv('BEARER')

def return_summary(comp_info, prod_info, tar_group):
    try: 
        headers = {"Authorization": f"Bearer {BEARER}"}

        url = "https://api.edenai.run/v2/text/chat"
        payload = {
            "providers": "openai",
            "text": f"Given the following information about a company and it's product : \nCompany Info : {comp_info} \n Product Info: {prod_info}\n Target Group profile: {tar_group}\n Generate content for video advertising of what our brand ambassador would say about it. You just need to have a monologue of what the person has to say and no actions or anything else. Have it shorter than 20 words.",
            "chatbot_global_action": "I want to help to generate content for an advertising video.",
            "previous_history": [],
            "temperature": 0.0,
            "max_tokens": 150,
        }

        response = requests.post(url, json=payload, headers=headers)

        result = json.loads(response.text)
        return(result['openai']['generated_text'])
    except Exception as e:
        print(f"An error occured while generating script : {e}")
        return f"{comp_info},  {prod_info}, {tar_group}"

# comp_info = "Apple"
# prod_info = "iPhone 14 which is very fast and smooth"
# tar_group = "young generation"
# print(return_summary(comp_info,prod_info,tar_group))