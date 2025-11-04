import io
from typing import Union, BinaryIO

from PIL import Image
import pdfplumber
import pdf2image
import pytesseract
import filetype

from logger import loggerUtils
from utilities.exceptions import UnsupportedFileTypeError

class OCRMode:
    IN_HOUSE = "in_house"
    ONLINE = "online"

class DocumentTextExtractor:
    SUPPORTED_IMAGE_TYPES = {"image/png", "image/jpeg", "image/jpg", "image/tiff"}
    SUPPORTED_PDF_TYPE = "application/pdf"

    def __init__(self, ocr_mode: str = OCRMode.ONLINE):
        if ocr_mode not in {OCRMode.IN_HOUSE, OCRMode.ONLINE}:
            raise ValueError(
                f"OCR mode must be either '{OCRMode.IN_HOUSE}' or '{OCRMode.ONLINE}'"
            )
        self.ocr_mode = ocr_mode
        self.ocr_detector = pytesseract