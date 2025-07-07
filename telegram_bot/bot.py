import os
import requests
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import logging
from database.db import init_db, SessionLocal, User, Chat, Message  

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.debug("Received /start command")
    await update.message.reply_text("Привет! Отправь мне сообщение.")

async def send_approved_message(chat_id: int, text: str, context: ContextTypes.DEFAULT_TYPE):
    try:
        await context.bot.send_message(chat_id=chat_id, text=text)
        logger.debug(f"Approved message sent to chat_id: {chat_id}")
    except Exception as e:
        logger.error(f"Failed to send approved message to chat_id {chat_id}: {str(e)}")

async def check_approved_messages(context: ContextTypes.DEFAULT_TYPE):
    logger.debug("Checking for approved messages")
    db = SessionLocal()
    try:
        messages = db.query(Message).filter(Message.status == "answered").all()
        for message in messages:
            await send_approved_message(message.chat_id, message.text, context)
            message.status = "sent"  
            db.commit()
            logger.debug(f"Message {message.id} marked as sent")
    except Exception as e:
        logger.error(f"Error checking approved messages: {str(e)}")
    finally:
        db.close()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.debug(f"Received message: {update.message.text} from chat_id: {update.message.chat_id}")
    db = SessionLocal()
    try:
        user = db.query(User).filter_by(id=update.message.from_user.id).first()
        if not user:
            user = User(
                id=update.message.from_user.id,
                token="dummy_token",
                token_updated_at="2025-07-06",
                token_ttl=3600,
                created_at="2025-07-06"
            )
            db.add(user)
            db.commit()

        chat = db.query(Chat).filter_by(id=update.message.chat_id).first()
        if not chat:
            chat = Chat(
                id=update.message.chat_id,
                user_id=update.message.from_user.id,
                created_at="2025-07-06"
            )
            db.add(chat)
            db.commit()

        message = Message(
            owner="user",
            chat_id=update.message.chat_id,
            text=update.message.text,
            status="new",
            parent_id=None
        )
        db.add(message)
        db.commit()
        logger.debug("User message saved to database")

        try:
            llm_response = requests.post(
                "http://llm_service:8000/generate",
                json={
                    "text": update.message.text,
                    "chat_id": str(update.message.chat_id)
                },
                timeout=10
            )
            llm_response.raise_for_status()
            llm_text = llm_response.json().get("response", "Ошибка: пустой ответ от LLM")
            logger.debug(f"LLM response: {llm_text}")

            operator_message = Message(
                owner="bot",
                chat_id=update.message.chat_id,
                text=llm_text,
                status="pending",
                parent_id=message.id
            )
            db.add(operator_message)
            db.commit()
            logger.debug("Bot response saved with pending status")

            await update.message.reply_text("Ваше сообщение принято, оператор скоро ответит.")

        except requests.RequestException as e:
            logger.error(f"LLM service request failed: {e}")
            await update.message.reply_text("Ошибка при генерации ответа. Попробуйте позже.")

    except Exception as e:
        logger.error(f"Error saving message: {str(e)}")
        await update.message.reply_text("Ошибка при сохранении сообщения.")
    finally:
        db.close()

def main():
    logger.debug("Starting bot")
    init_db()  
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.job_queue.run_repeating(check_approved_messages, interval=10, first=10) 
    app.run_polling()

if __name__ == "__main__":
    main()