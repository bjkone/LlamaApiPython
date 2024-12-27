from fastapi import FastAPI, HTTPException
import requests
from pydantic import BaseModel


app = FastAPI()


class Query(BaseModel):
    prompt: str
    model: str = "llama3.2"
    stream: bool = False


@app.post("/generate")
async def generate_text(query: Query):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": query.model, "prompt": query.prompt, "stream": query.stream},
            headers={"Content-Type": "application/json"},
        )
        print(response)
        response.raise_for_status()
        return {"generated_text": response.json()["response"]}
    except requests.RequestException as e:
        raise HTTPException(
            status_code=500, detail=f"Error communicating with Ollama: {str(e)}"
        )


@app.get("/models")
async def list_models():
    try:

        response = requests.get("http://localhost:11434/api/tags")
        response.raise_for_status()
        return {"models": response.json()["models"]}
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching models: {str(e)}")


@app.post("/conversation/start")
async def start_conversation(conv_id: str):
    if conv_id in conversations:
        raise HTTPException(status_code=400, detail="Conversation ID already exists")
    conversations[conv_id] = Conversation(id=conv_id)
    return {"message": f"Conversation {conv_id} started"}


@app.get("/")
def root():
    return {"message": "Welcome to the Ollama and FastAPI Integration!"}
