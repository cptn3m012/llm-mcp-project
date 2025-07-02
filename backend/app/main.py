from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import logging

from app.services.agents import query_agent

# -------- Configuration ------------
load_dotenv()
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="LLM + MCP Demo")


@app.get("/health")
async def health():
    """Simple health check endpoint."""
    return {"status": "ok"}


class QueryRequest(BaseModel):
    query: str


@app.post("/query")
async def query(req: QueryRequest):
    """
    Receives a user query -> delegates to the LangChain agent ->
    returns the generated response.
    """
    try:
        answer = query_agent(req.query)
        return {"response": answer}
    except Exception as exc:
        logging.exception("Agent error: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))
