from typing import Optional

from google.cloud import vision
from google.oauth2 import service_account

from config import GOOGLE_CREDENTIALS_JSON_FILEPATH
from logger import loggerUtils as logger

try:
    GCP_CREDENTIALS = service_account.Credentials.from_service_account_file(
        GOOGLE_CREDENTIALS_JSON_FILEPATH
    )
except Exception as e:
    logger.warning(
        f"GCP credentials could not be loaded from {GOOGLE_CREDENTIALS_JSON_FILEPATH}: {e}"
    )
    GCP_CREDENTIALS = None

def get_gcp_vision_client() -> Optional[vision.ImageAnnotatorClient]:
    if GCP_CREDENTIALS:
        return vision.ImageAnnotatorClient(credentials=GCP_CREDENTIALS)
    else:
        logger.error("GCP credentials are not available.")
        return None