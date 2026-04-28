import os
from dotenv import load_dotenv
load_dotenv()

print("API Key loaded:", bool(os.getenv('GOOGLE_API_KEY')))

try:
    import google.generativeai as genai
    api_key = os.getenv('GOOGLE_API_KEY')
    if api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content("Hello, test message")
        print("Gemini API test successful:", response.text[:50])
    else:
        print("No API key found")
except Exception as e:
    print("Gemini API error:", str(e))