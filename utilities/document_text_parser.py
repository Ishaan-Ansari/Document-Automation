import io
from typing import Union, BinaryIO

from PIL import Image
import pdfplumber
import pdf2image
import pytesseract
import filetype

from logger import loggerUtils
from utilities.exceptions import UnsupportedFileTypeError
from utilities.ocr import GoogleVisionOCRDetector

try:
    from docx import Document as DocxDocument
except Exception:
    DocxDocument = None  # type: ignore


class OCRMode:
    IN_HOUSE = "in_house"
    ONLINE = "online"

class DocumentTextExtractor:
    SUPPORTED_IMAGE_TYPES = {"image/png", "image/jpeg", "image/jpg", "image/tiff"}
    SUPPORTED_PDF_TYPE = "application/pdf"
    # common MIME types for Word documents
    SUPPORTED_DOC_TYPES = {
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document", # .docx
    "application/msword", # .doc
    }

    def __init__(self, ocr_mode: str = OCRMode.ONLINE):
        if ocr_mode not in {OCRMode.IN_HOUSE, OCRMode.ONLINE}:
            raise ValueError(
                f"OCR mode must be either '{OCRMode.IN_HOUSE}' or '{OCRMode.ONLINE}'"
            )
        self.ocr_mode = ocr_mode
        self.ocr_detector = GoogleVisionOCRDetector() 

    async def extract_text(self, file: Union[BinaryIO, io.BytesIO]) -> str:
        """
        Extract text from a given file.

        Args:
            file: A file-like object containing the image or PDF file.

        Returns:
            str: Extracted text from the file.

        Raises:
            UnsupportedFileTypeError: If the file type is not supported.
            Exception: If any other error occurs during text extraction.
        """
        try:
            kind = filetype.guess(file)

            if kind is None:
                raise UnsupportedFileTypeError("Could not determine the file type.")
            
            mime_type = kind.mime

            loggerUtils.debug(f"Extracting text from file of type: {mime_type}")

            if mime_type == self.SUPPORTED_PDF_TYPE:
                text = await self._extract_from_pdf(file)
            elif mime_type in self.SUPPORTED_IMAGE_TYPES:
                text = await self._extract_from_image(file)
            elif mime_type in self.SUPPORTED_DOC_TYPES:
                text = await self._extract_from_doc(file)
            else:
                raise UnsupportedFileTypeError(f"Unsupported file type: {mime_type}")

            return text

        except Exception as e:
            loggerUtils.exception(f"Error in DocumentTextExtractor.extract_text: {e}")
            raise e

    async def _extract_from_doc(self, file: BinaryIO) -> str:
        """Extract text from a Word document"""
        if DocxDocument is None:
            raise UnsupportedFileTypeError("python-docx library is not installed.")

        file.seek(0)
        document = DocxDocument(file)
        full_text = []

        for para in document.paragraphs:
            full_text.append(para.text)

        return "\n\n".join(full_text)
    
    async def _extract_from_pdf(self, file: BinaryIO) -> str:
        """Extract text from a PDF file"""
        file.seek(0)
        full_text = ""

        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                full_text += page.extract_text() + "\n\n"

        # If the extracted text is not empty return it
        if full_text.strip():
            return full_text

        loggerUtils.debug("PDF text extraction failed, trying OCR")

        # If the extracted text is empty, try OCR
        full_text = await self._extract_text_from_pdf_with_ocr(file)

        return full_text

    async def _extract_text_from_pdf_with_ocr(self, file: BinaryIO) -> str:
        """Extract text from a PDF file using OCR"""
        file.seek(0)
        images = pdf2image.convert_from_bytes(file.read())

        # Save these images as png
        _image_files_png = []
        for image in images:
            _file = io.BytesIO()
            image.save(_file, format="PNG")
            _file.seek(0)
            _image_files_png.append(_file)

        image_texts = await self.ocr_detector.detect_multiple_images_text_async(
            image_files=_image_files_png
        )

        # Close all the files
        for image_file in _image_files_png:
            image_file.close()

        return "\n\n".join(image_texts)

    async def _extract_from_image(self, file: BinaryIO) -> str:
        """Extract text from an in-memory image"""
        if self.ocr_mode == OCRMode.IN_HOUSE:
            text = self._apply_local_ocr(file)

        elif self.ocr_mode == OCRMode.ONLINE:
            text = await self._apply_online_ocr(file)
        else:
            raise ValueError(
                f"OCR mode must be '{OCRMode.IN_HOUSE}' or '{OCRMode.ONLINE}'"
            )

        return text

    def _apply_local_ocr(self, image_file: BinaryIO) -> str:
        """Apply local OCR to a single image file"""
        raise NotImplementedError("Local OCR is not implemented yet")

    async def _apply_online_ocr(self, image_file: BinaryIO) -> str:
        """Apply online OCR to a single image file"""
        image = Image.open(image_file)

        with io.BytesIO() as _file:
            image.save(_file, format="PNG")
            _file.seek(0)
            text = await self.ocr_detector.detect_image_text_async(_file)

        return text        
