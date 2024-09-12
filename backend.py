import google.generativeai as genai
import os
from dotenv import load_dotenv

def genai_generate_content(context=""):

    load_dotenv()  # Load environment variables from .env file

    api_key = os.getenv("API_KEY")
    prompt = os.getenv("PROMPT")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-1.5-flash")
    result = model.generate_content(
        [context, "\n\n", prompt]
    )
    # print(f"{result.text=}")
    return result.text