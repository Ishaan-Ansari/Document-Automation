"""
FastAPI Application for Task 1 - Method Statement Automation

- Use the BOQ Extract and Project Details Sheet to generate a draft Method Statement for blockwork & plastering.
- Populate at least the following sections: Scope, References, Materials, Work Procedure.
"""

import json
import os
from io import BytesIO
from task1.BOQExtract import BOQExtractParser
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, File, UploadFile, HTTPException


async def process_boq_document(file: UploadedFile = File(...)):
    try:
        boq_parser = BOQExtractParser()
        boq_data = await boq_parser.parse_boq_document(file.file)
        return JSONResponse(content=jsonable_encoder(boq_data))
    
    except UnsupportedFileTypeError as e:
        raise HTTPException(status_code=400, detail="Unsupported file type.")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)