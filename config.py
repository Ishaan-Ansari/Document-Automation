# config.py
import os
from pathlib import Path
from dotenv import load_dotenv

# project root assumed to be one level up from this file or same dir as app.py
ROOT = Path(__file__).resolve().parent

# if .env is in project root, change accordingly
dotenv_path = ROOT / ".env"
if dotenv_path.exists():
    load_dotenv(dotenv_path)

# canonical env names
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_CREDENTIALS_JSON_FILEPATH = os.getenv("GOOGLE_CREDENTIALS_JSON_FILEPATH")

# convenience helper to inspect quickly (optional)
# def debug_env():
#     print("OPENAI_API_KEY set:", bool(OPENAI_API_KEY))
#     print("GOOGLE_CREDENTIALS_JSON_FILEPATH:", GOOGLE_CREDENTIALS_JSON_FILEPATH)



# import os 
# from pathlib import Path
# from dotenv import load_dotenv

# ROOT = Path(__file__).resolve().parent

# # Load environment variables
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") 
# GOOGLE_CREDENTIALS_JSON_FILEPATH = os.getenv("GOOGLE_CREDENTIALS_JSON_FILEPATH")