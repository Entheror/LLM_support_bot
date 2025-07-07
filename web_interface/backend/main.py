from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
import logging
from database.db import init_db, SessionLocal, Chat, Message  

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

init_db()  

class MessageRequest(BaseModel):
    chat_id: int
    text: str

class MessageStatusRequest(BaseModel):
    message_id: int
    status: str
    chat_id: Optional[int] = None
    text: Optional[str] = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/messages/new")
async def get_new_messages(db: Session = Depends(get_db)):
    logger.debug("Received request for /messages/new")
    try:
        messages = db.query(Message).filter(Message.status == "new").all()
        result = [
            {"id": m.id, "owner": m.owner, "chat_id": m.chat_id, "text": m.text, "status": m.status}
            for m in messages
        ]
        logger.debug(f"Returning messages: {result}")
        return result
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/messages/generate")
async def generate_message(request: MessageRequest, db: Session = Depends(get_db)):
    logger.debug(f"Received POST /messages/generate with chat_id: {request.chat_id}, text: {request.text}")
    try:
        chat = db.query(Chat).filter(Chat.id == request.chat_id).first()
        if not chat:
            logger.error(f"Chat with id {request.chat_id} not found")
            raise HTTPException(status_code=422, detail=f"Chat with id {request.chat_id} not found")
        message = Message(
            chat_id=request.chat_id,
            text=request.text,
            status="pending",
            owner="bot",
            parent_id=None
        )
        db.add(message)
        db.commit()
        logger.debug("Message added to database")
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/messages/status")
async def update_status(request: MessageStatusRequest, db: Session = Depends(get_db)):
    logger.debug(f"POST /messages/status with: {request}")
    try:
        message = db.query(Message).filter(Message.id == request.message_id).first()
        if not message:
            logger.warning(f"Message not found: {request.message_id}")
            raise HTTPException(status_code=404, detail="Message not found")

        if request.status == "edited":
            if request.text is not None:
                message.text = request.text
            if request.chat_id is not None:
                message.chat_id = request.chat_id

        message.status = request.status
        db.commit()
        logger.debug("Message status updated")

        return {"status": "success"}
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/responses/pending")
async def get_pending_responses(db: Session = Depends(get_db)):
    logger.debug("Received request for /responses/pending")
    try:
        messages = db.query(Message).filter(Message.status.in_(["pending", "edited"])).all()
        result = [
            {"id": m.id, "owner": m.owner, "chat_id": m.chat_id, "text": m.text, "status": m.status}
            for m in messages
        ]
        logger.debug(f"Returning pending responses: {result}")
        return result
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")