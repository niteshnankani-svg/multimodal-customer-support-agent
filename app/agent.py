import openai
import base64
import os
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def encode_image(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def analyze_complaint(image_path: str, complaint_text: str) -> str:
    
    base64_image = encode_image(image_path)
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": """You are a helpful customer support agent. 
                Analyze the product image and the customer complaint together.
                Provide a clear, empathetic, and actionable response.
                Include:
                1. Acknowledgment of the issue
                2. What you can see in the image
                3. Recommended solution
                4. Next steps for the customer"""
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Customer complaint: {complaint_text}"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=500
    )
    
    return response.choices[0].message.content