import os
import base64
import asyncio
from abc import ABC, abstractmethod
from io import BytesIO

from google.cloud import vision as google_vision

from logger import loggerUtils as logger
from .gcp_utils import get_gcp_vision_client

class OCRDetector(ABC):
    @abstractmethod
    def detect_image_text(self, image: BytesIO):
        pass

    @abstractmethod
    async def detect_image_text_async(self, image: BytesIO):
        pass

    @abstractmethod
    async def detect_multiple_images_text_async(self, images: list[BytesIO]):
        pass

class GoogleVisionOCRDetector:
    def __init__(self):
        self.client = get_gcp_vision_client()
        if not self.client:
            raise Exception("Google Vision API client could not be initialized.")
        
    def get_vision_image(self, image: BytesIO) -> google_vision.Image:
        image_base64 = base64.b64encode(image.getvalue()).decode("utf-8")
        return google_vision.Image(content=image_base64)
    
    def detect_text_annotation_from_response(
            self, response: google_vision.AnnotateImageResponse
    ) -> str:
        if response.error.message:
            logger.error(f"Google Vision API error: {response.error.message}")
            raise Exception(f"Google Vision API error: {response.error.message}")
        
        text_annotations = response.text_annotations
        if text_annotations:
            return text_annotations[0].description
        return ""
    
    def detect_text(self, image: BytesIO)-> str:
        """Detects text in an image using Google Vision API."""
        image = self.get_vision_image(image)
        response = self.client.text_detection(image=image)

        return self.detect_text_annotation_from_response(response)
    
    async def detect_image_text_async(self, image: BytesIO):
        """Asynchronously detects text in an image"""
        image = self.get_vision_image(image)
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(None, lambda: self.client.text_detection(image=image))
        return self.detect_text_annotation_from_response(response)
    
    async def detect_multiple_images_text_async(self, images: list[BytesIO]):
        """Asynchronously detects text in multiple images"""
        tasks = [self.detect_image_text_async(image) for image in images]
        results = await asyncio.gather(*tasks)
        return results