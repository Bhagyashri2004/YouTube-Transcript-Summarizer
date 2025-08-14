from dotenv import load_dotenv
import os
from groq import Groq

# Load variables from .env
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is not set in the .env file")

# Create Groq client
client = Groq(api_key=api_key)
