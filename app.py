from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="Wish.com Redis Clone", version="1.0.0")

@app.get("/ping")
async def ping():
    """Health check endpoint"""
    message = ping()
    return {"message": message} 