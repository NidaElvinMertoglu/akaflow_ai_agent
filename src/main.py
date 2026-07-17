from fastapi import FastAPI
from pydantic import BaseModel
from ai_agent.agent_service import ask_agent
from prediction_engine import get_student_prediction # Yeni import

app = FastAPI(title="AkaFlow AI Agent Platformu")

class QueryModel(BaseModel):
    question: str

class PredictionModel(BaseModel):
    student_id: int

# Mevcut AI Agent endpoint'i
@app.post("/api/v1/agent/ask")
async def handle_query(payload: QueryModel):
    # Agent burada senin verilerine erişmek için "get_student_prediction"
    # fonksiyonunu bir tool olarak kullanacak şekilde yapılandırılmalı.
    answer = ask_agent(payload.question)
    return {"response": answer}

# Yeni ML Tahmin endpoint'i
@app.post("/api/v1/predict")
async def handle_prediction(payload: PredictionModel):
    result = get_student_prediction(payload.student_id)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)