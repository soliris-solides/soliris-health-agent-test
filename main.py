import os
from dotenv import load_dotenv
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

import csv
import io
from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import Dict, List
from auth.login import router
from auth.login import verify_token
import tiktoken
app = FastAPI()

app.include_router(router)


encoding = tiktoken.encoding_for_model("gpt-4")

def count_tokens(text: str) -> int:
    return len(encoding.encode(text))

MAX_TOKENS = 512

supervisor_cache: Dict[str, object] = {} # será melhorado futuramente, para implementação futura de cash de respostas
messages_csv: Dict[str, List[object]] = {}

class Interaction(BaseModel):
    #openai_key: str
    #thread_id: str
    content: str
    
@app.get("/")
def connected():
    return True

@app.post("/")
def handle_interaction(interaction: Interaction, thread_id: str = Depends(verify_token)):
    
    if count_tokens(interaction.content) > MAX_TOKENS:
        return [{"content": "⚠️ Sua mensagem é muito longa. Por favor, envie até 512 tokens (cerca de 350 palavras)."}]
    
    try:
        if thread_id not in supervisor_cache:
            from graph import supervisor
            supervisor_cache[thread_id] = supervisor
            messages_csv[thread_id] = []

        supervisor = supervisor_cache[thread_id]

        config = {"configurable": {"thread_id": thread_id}}
        
        messages_csv[thread_id].append(
            {
                "role": "user",
                "content": interaction.content
            }
        )

        resp = supervisor.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": interaction.content
                    }
                ]
            },
            config
        )
        
        messages_csv[thread_id].append(
            {
                "role": "assistant",
                "content": resp['messages'][-1].content
            }
        )

        return resp['messages']
    except Exception as e:
        import traceback
        traceback_str = traceback.format_exc()
        print("Erro no POST /:", traceback_str)
        return JSONResponse(content={"error": str(e), "trace": traceback_str}, status_code=500)

@app.post('/end_conection')
def end_conection(thread_id: str = Depends(verify_token)):
    if thread_id in supervisor_cache:
        supervisor_cache.pop(thread_id, None)
        messages_csv.pop(thread_id, None)
        return JSONResponse(content={"message": "Sessão finalizada com sucesso."}, status_code=200)
    else:
        return JSONResponse(content={"message": "Essa sessão não existe."}, status_code=404)
    

@app.get("/history")
def download_csv(thread_id: str = Depends(verify_token)):
    if thread_id not in supervisor_cache:
        return JSONResponse(content={"message": "Essa sessão não existe."} ,status_code=404)

    # Cria CSV em memória
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["role", "content"])
    writer.writeheader()
    for message in messages_csv[thread_id]:
        writer.writerow(message)

    output.seek(0)  # Volta para o início do buffer
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={thread_id}.csv"}
    )
