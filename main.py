from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents='Why is the meaning of life 42?'
)
print(response.text)
