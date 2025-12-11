import uuid
import uvicorn
import whisper
import shutil
import os
from agent import agent
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import HumanMessage
from pydantic import BaseModel


app = FastAPI()

# config cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

audio_model = whisper.load_model("small")

class ChatRequest(BaseModel):
    message: str
    thread_id: str = None

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    # save file as a temporary file 
    temp_filename = f"temp_{uuid.uuid4()}.webm"
    
    try:
        with open(temp_filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # using the model to transcribe
        result = audio_model.transcribe(temp_filename, fp16=False)
        text = result["text"].strip()
        
        return {"text": text}
        
    except Exception as e:
        return {"error": str(e)}
        
    finally:
        # Nettoyage : on supprime le fichier temp
        if os.path.exists(temp_filename):
            os.remove(temp_filename)


@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    # thread for conversation memory
    thread_id = request.thread_id or str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    # streaming generator
    async def generate_stream():
        inputs = {"messages": [HumanMessage(content=request.message)]}
        try:
            # get tokens from agent
            async for event in agent.astream_events(inputs, config=config, version="v1"):
                kind = event["event"]
                
                # send response chunks
                if kind == "on_chat_model_stream":
                    content = event["data"]["chunk"].content
                    if content:
                        yield content
                        
        except Exception as e:
            yield f"Backend error: {str(e)}"

    # return streaming response
    return StreamingResponse(generate_stream(), media_type="text/plain")

if __name__ == "__main__":
    print("api lancé sur http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)