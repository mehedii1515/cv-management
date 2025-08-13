from dotenv import load_dotenv
import os


GPT_MODEL = "gpt-3.5-turbo"

DATA_FOLDER = "Sample CVs\\"

OUTPUT_FOLDER = "Output\\"

PROMPT_FILE = "prompt.yml"




def InitialiseAPI():
    load_dotenv()  # Load variables from .env
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("Missing OpenAI API key. Please check your .env file.")
    
    return api_key