"""
This file contains all the functions/classes related to WIR extraction for Task 2
"""
from pydantic import BaseModel
from typing import List, BinaryIO

from task2.constants import WIR_EXTRACT_NAME
from task2.prompts import WIR_EXTRACT_SYSTEM_PROMPT, WIR_EXTRACT_USER_PROMPT
from logger import loggerT2
from constants import GPT_Model
from utilities.document_text_parser import DocumentTextExtractor, OCRMode
from utilities.ai_generator import OpenAITextGenerator, OpenAI_Text_Config
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
        self.ai_generator = OpenAITextGenerator(
            config=OpenAI_Text_Config(model=GPT_Model.GPT_4_1.value)
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
    
    async def _ai_parse_wir_text(self, WIR_extracted_text: str) -> WIRExtractData:
        response = await self.ai_generator.async_generate_response(
            system_prompt=WIR_EXTRACT_SYSTEM_PROMPT,
            user_prompt=WIR_EXTRACT_USER_PROMPT.format(
                WIR_extracted_text=WIR_extracted_text
            ),
            response_format=WIRExtractData,
            project_name=WIR_EXTRACT_NAME
        )
        return response["response"]
    
    async def parse_wir_document(self, file: BinaryIO) -> WIRExtractData:
        try:
            self._validate_file_type(file)
            extracted_text = await self._extract_text_from_doc(file)
            
            wir_data =  await self._ai_parse_wir_text(
                WIR_extracted_text=extracted_text
            )

            return wir_data

        except Exception as e:
            loggerT2.error(f"Error parsing WIR document: {e}")
            raise e