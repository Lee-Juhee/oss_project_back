from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import uvicorn

origin = {"http://127.0.0.1:5500", "http://44.207.59.235"}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    name: str
    message: str

class MessageInDB(Message):
    id: int
    timestamp: datetime

guestbook = []
router = APIRouter()

@router.post("/guestbook", response_model=MessageInDB)
async def post_message(message: Message):
    new_message = MessageInDB(**message.dict(), id=len(guestbook), timestamp=datetime.now())
    guestbook.append(new_message)
    return new_message

@router.get("/guestbook")
async def get_messages():
    return JSONResponse(content=[msg.dict() for msg in guestbook])

app.include_router(router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, reload = True)
