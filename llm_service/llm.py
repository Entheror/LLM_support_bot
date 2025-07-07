from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.concurrency import run_in_threadpool
import ollama
import logging

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

class Request(BaseModel):
    text: str
    chat_id: str

@app.post("/generate")
async def generate_response(request: Request):
    logger.debug(f"Received POST /generate with text: {request.text}, chat_id: {request.chat_id}")
    try:
        def generate():
            try:
                logger.debug("Calling ollama.generate with model: tinyllama")
                response = ollama.generate(
                    model="tinyllama",
                    prompt=f"Ответь на сообщение пользователя: {request.text}",
                    options={"encoding": "utf-8"}  
                )
                logger.debug(f"Ollama response: {response}")
                return response
            except Exception as e:
                logger.error(f"Ollama error: {str(e)}")
                raise
        response = await run_in_threadpool(generate)
        response_text = str(response['response']).encode('utf-8').decode('utf-8')
        logger.debug(f"LLM response: {response_text}")
        return {"response": response_text}
    except Exception as e:
        logger.error(f"Error in generate_response: {str(e)}")
        raise HTTPException(status_code=500, detail=f"LLM error: {str(e)}")

@app.get("/")
async def root():
    return {"message": "LLM service is running"}