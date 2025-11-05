from datetime import datetime
from fastapi import FastAPI, HTTPException
from pathlib import Path
from typing import Any
import json

app = FastAPI()

@app.get("/utcp")
async def utcp_invoke():
    file_path = Path("api_manual.json")
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    try:
        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON")
    return data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=3000, reload=True)