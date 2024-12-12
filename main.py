from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from loguru import logger
from orchestrator import Orchestrator

app = FastAPI()
orchestrator = Orchestrator()


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    response: str


@app.post("/predict", response_model=QueryResponse)
def predict(request: QueryRequest):
    try:
        logger.info(f"Received query: {request.query}")
        response_content = orchestrator.get_personal_assistant_response(
            request.query)
        return QueryResponse(response=response_content)
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
