"""
This file contains all the functions/classes related to BOQ extraction for Task 1
"""

from pydantic import BaseModel
from typing import List, BinaryIO

from task1.constants import BOQ_EXTRACT_NAME
from task1.prompts import *

from logger import loggerT1
from constants import GPT_Model
from utilities.exceptions import UnsupportedFileTypeError
from utilities.document_text_parser import DocumentTextExtractor, OCRMode
from utilities.ai_generator import OpenAITextGenerator, OpenAI_Text_Config

class BOQExtractData(BaseModel):
    Scope: str
    References: str
    Materials: str
    WorkProcedure: str

class MethodStatement(BaseModel):
    MethodStatement: List[BOQExtractData]
    follow_up_instructions: str
    general_notes: str

class BOQExtractParser:
    """This class is used to parse BOQ documents and extract relevant information."""
    def __init__(self):
        self.document_text_extractor = DocumentTextExtractor(
            ocr_mode=OCRMode.ONLINE
        ) 
        self.ai_generator = OpenAITextGenerator(
            config=OpenAI_Text_Config(model=GPT_Model.GPT_4_1_NANO.value)
        )

    def _validate_file_type(self, file: BinaryIO):
        """
        For now all file types supported by the Document Text Extractor are supported.
        """
        pass

    async def _extract_text_from_doc(self, file: BinaryIO) -> str:
        file.seek(0)
        extracted_text = await self.document_text_extractor.extract_text(file)
        return extracted_text
    
    async def _ai_parse_prescription_text(self, BOQ_extracted_text: str) -> MethodStatement:
        response = await self.ai_generator.async_generate_response(
            system_prompt=BOQ_EXTRACT_SYSTEM_PROMPT,
            user_prompt=BOQ_EXTRACT_USER_PROMPT.format(
                BOQ_extracted_text=BOQ_extracted_text
            ),
            response_format=MethodStatement,
            project_name=BOQ_EXTRACT_NAME
        )
        return response["response"]
    
    async def parse_boq_document(self, file: BinaryIO) -> MethodStatement:
        try:
            self._validate_file_type(file)
            
            document_text = await self._extract_text_from_doc(file)

            boq_data = await self._ai_parse_prescription_text(
                BOQ_extracted_text=document_text
            )

            return boq_data
    
        except UnsupportedFileTypeError as e:
            loggerT1.exception(f"Error parsing document: {e}")
            raise e