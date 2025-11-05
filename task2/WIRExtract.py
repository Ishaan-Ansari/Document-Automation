"""
This file contains all the functions/classes related to BOQ extraction for Task 2
"""
from pydantic import BaseModel
from typing import List, BinaryIO

from task2.constants import WIR_EXTRACT_NAME
from logger import loggerT2
from utilities.document_text_parser import DocumentTextExtractor, OCRMode
from utilities.exceptions import UnsupportedFileTypeError

class WIRExtractData(BaseModel):
    Project: str
    WIR_No: str
    Date: str
    Activity: str
    Contractor: str
    Handwritten_Remark: str

class WIRExtractParser:
    def __init__(self):
        self.document_text_extractor = DocumentTextExtractor(
            ocr_mode=OCRMode.ONLINE
        )
    
    def _validate_file_type(self, file: BinaryIO):
        """
        For now all file types supported by the Document Text Extractor are supported.
        """
        pass

    async def _extract_text_from_doc(self, file: BinaryIO) -> str:
        file.seek(0)
        extracted_text = self.document_text_extractor.extract_text(file)
        return extracted_text
    
    async def parse_wir_document(self, file: BinaryIO) -> WIRExtractData:
        try:
            self._validate_file_type(file)
            extracted_text = await self._extract_text_from_doc(file)
            return extracted_text
        except Exception as e:
            loggerT2.error(f"Error parsing WIR document: {e}")
            raise e