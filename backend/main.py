from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import run_sales_agent

app = FastAPI(title="Furniture AI Sales Agent", version="1.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=False,
    allow_methods=["*"], allow_headers=["*"],
)

class SalesRequest(BaseModel):
    inquiry: str
    language: str = "zh"

@app.get("/health")
def health():
    return {"status": "ok", "service": "sales-agent", "version": "1.2.1"}

@app.post("/api/sales-agent")
def sales_agent(req: SalesRequest):
    return run_sales_agent(req.inquiry, req.language)
