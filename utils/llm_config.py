import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()

def get_llm(model_name="gemini-pro", temperature=0.3):
    """
    Returns a configured Gemini LLM instance.
    Raises a clear error if API key is missing.
    """
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY not found. "
            "Please set it in your .env file or Streamlit Secrets."
        )

    return ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=api_key,
        temperature=temperature,
        convert_system_message_to_human=True
    )
