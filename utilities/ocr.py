import os
import asyncio
from abc import ABC, abstractmethod
from io import BytesIO

from google.cloud import vision as google_vision
