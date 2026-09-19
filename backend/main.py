from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import run_sales_agent
from llm_gateway import public_provider_status

app = FastAPI(title="Furniture AI Sales Agent", version="1.3.3")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=False,
    allow_methods=["*"], allow_headers=["*"],
)

class SalesRequest(BaseModel):
    inquiry: str
    language: str = "zh"
    provider: Optional[str] = None

@app.get("/health")
def health(provider: Optional[str] = None):
    return {
        "status": "ok",
        "service": "sales-agent",
        "version": "1.3.3",
        "llm": public_provider_status(provider),
    }

@app.post("/api/sales-agent")
def sales_agent(req: SalesRequest):
    return run_sales_agent(req.inquiry, req.language, req.provider)
