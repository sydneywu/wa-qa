from fastapi import FastAPI, Request, Query
import json
import requests
import os
from dotenv import load_dotenv

from models.send import SendMessageInput, init_message
from models.receive import WhatsappIncomingData
from qa import ask_llm

load_dotenv()


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Simple WhatsApp Webhook tester. There is no front-end, see server.py for implementation!"}

@app.get('/webhook')

async def verify_webhook(
    hub_mode: str = Query(..., alias="hub.mode"),
    hub_verify_token: str = Query(..., alias="hub.verify_token"),
    hub_challenge: str = Query(..., alias="hub.challenge")  
):
    print(hub_mode)
    print(hub_verify_token)
    print(hub_challenge)

    verify_token = os.getenv('WA_VERIFY_TOKEN')

    if (
        hub_mode == 'subscribe' and
        hub_verify_token == verify_token
    ):
        
        return int(hub_challenge)
    else:
        return {"status": "error"}

@app.post("/webhook")
async def handle_webhook(request: Request):
    json_data = await request.json()
    print(f"Incoming webhook: {json_data}")
    print("xxyxxyxxyxxy")
    incomingData = WhatsappIncomingData(**json_data)
    key_data = incomingData.entry[0].changes[0].value
    mobile = key_data.contacts[0].wa_id
    message_content = key_data.messages[0].text.body

    print(mobile)
    print(message_content)
    
    send_message_input = SendMessageInput(mobile=mobile, text_message=message_content)
    send_response = await send_qa(send_message_input)
    return {"status": "success"}


@app.post("/test_send")
async def send_qa(request: SendMessageInput):
    llm_answer = ask_llm(request.text_message)

    message = init_message(request.mobile, llm_answer)
    json_data = message.json()
    url = os.getenv('WA_MESSAGE_URL')

    wa_token = os.getenv('WA_TOKEN')

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + wa_token
    }
    
    response = requests.post(url, data = json_data, headers = headers)
    print(response)
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)