from pydantic import BaseModel


class UserModel(BaseModel):
    name: str


class ChatRequest(BaseModel):
    user_id: str
    question: str

