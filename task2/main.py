"""
Task 2 - OCR & Handwriting Extraction

- From the scanned WIR, extract both typed details (Project, WIR No., Date, Activity, Contractor) and the handwritten remark.
- Present the extracted data in a structured JSON or table format.
"""

import json
import os
from io import BytesIO
from task2.WIRExtract import WIRExtractParser
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, File, UploadFile, HTTPException

from utilities.exceptions import UnsupportedFileTypeError

app = FastAPI()

@app.post("/task2")
async def process_WIR_document(file: UploadFile = File(...)):
    # import pdb; pdb.set_trace()
    try:
        wir_parser = WIRExtractParser()
        wir_data = await wir_parser.parse_wir_document(file.file)
        return JSONResponse(content=jsonable_encoder(wir_data))
    
    except UnsupportedFileTypeError as e:
        raise HTTPException(status_code=400, detail="Unsupported file type.")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)