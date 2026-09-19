

from fastapi import FastAPI
from pydantic import BaseModel
from app.agent import investigate as run_investigation


app = FastAPI()


class InvestigationRequest(BaseModel):
    question: str


class InvestigationResponse(BaseModel):
    question: str
    answer: str
    status: str

@app.get("/")
def root():
    return {"message":"Enterprise agent is live"}


@app.post("/investigate",response_model=InvestigationResponse)
def investigate(request: InvestigationRequest):
    result = run_investigation(request.question)


    
    return {
        "question": request.question,
        "answer": result["answer"],
        "status": result["status"]
    }





