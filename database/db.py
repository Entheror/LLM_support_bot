from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

DATABASE_URL = "sqlite:////app/database/support.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    token = Column(String)
    token_updated_at = Column(String) 
    token_ttl = Column(Integer)
    created_at = Column(String)

class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(String)

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    owner = Column(String(7))
    parent_id = Column(Integer, ForeignKey("messages.id"), nullable=True)
    chat_id = Column(Integer, ForeignKey("chats.id"))
    status = Column(String(8))
    text = Column(String)

def init_db():
    logger.debug("Initializing database")
    try:
        Base.metadata.create_all(bind=engine)
        logger.debug("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise