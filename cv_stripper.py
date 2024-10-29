from pdfminer.high_level import extract_text
from dotenv import load_dotenv
from openai import OpenAI
import json
import os

# Models
from classes.cv import Cv

load_dotenv("./config/.env")

OPENAI_KEY = os.getenv('OPENAI_KEY')

class CVStripper:
    def __init__(self):
      self.client = OpenAI(api_key = OPENAI_KEY)
        
    def extract(self, path):
        try:
            extracted_text = extract_text(path)

            # Prepare messages for GPT-4
            messages = [
                {"role": "system", "content": "You analyze CV's and turn it into an Cv model"},
                {"role": "user", "content": f"<CV>\n{extracted_text}\n</CV>\nGive me an Cv model based on this CV information."}
            ]

            # Send request to GPT-4
            response = self.client.beta.chat.completions.parse(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.4,
                response_format=Cv
            )

            # Parse the response and create Cv object
            cv_data = response.choices[0].message.content
            
            return json.loads(cv_data)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None