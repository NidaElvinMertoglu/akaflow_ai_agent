from fastapi import FastAPI
from pydantic import BaseModel
from ai_agent.agent_service import ask_agent

app = FastAPI(title="AkaFlow AI Agent Platformu")

class QueryModel(BaseModel):
    question: str

@app.post("/api/v1/agent/ask")
async def handle_query(payload: QueryModel):
    answer = ask_agent(payload.question)
    return {"response": answer}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)