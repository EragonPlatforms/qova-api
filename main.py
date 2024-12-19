import os
from uuid import uuid4

import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from typing_extensions import Annotated

from models import UserModel, ChatRequest
from utils import retrieve_rag_query

load_dotenv()

app = FastAPI()


LLM_MODEL_NAME = "llama-3.1-8b-instant"


def get_llm():
    return ChatGroq(model_name=LLM_MODEL_NAME, temperature=0.5, api_key=os.getenv('GROQ_API_KEY'))


@app.get("/")
def index():
    return {"message": "welcome to Online Safety Bot API"}


@app.post("/user")
async def welcome_user(user: UserModel):
    return {"user_id": uuid4(), "name": user.name}


@app.post("/chat")
async def chat(chat_request: ChatRequest, llm: Annotated[ChatGroq, Depends(get_llm)]):
    try:
        messages = retrieve_rag_query(chat_request.question)
        response = llm.invoke(messages, )
        return {"content": response.content}
    except:
        raise HTTPException(status_code=404, detail="Error getting response")


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, reload=True)