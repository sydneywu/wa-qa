from fastapi import FastAPI, Request, Query
import json
import requests
import os
from dotenv import load_dotenv

from models.send import SendMessageInput, init_message
from models.receive import WhatsappIncomingData
from qa import ask_llm

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = openai_api_key

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Simple WhatsApp Webhook demo"}

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

    if("entry" not in json_data or "object" not in json_data):
        print("webhhook doesn't have entry/object")
        return {"status": "error"}
    
    change_data = json_data["entry"][0]["changes"][0]["value"]
    if("contacts" not in change_data):
        # This is not a whatsapp message
        print("webhhook doesn't have contact")
        return {"status": "error"}
    
    ### Continue only if it is a whatsapp message
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
    port = os.getenv('PORT')
    uvicorn.run(app, host="0.0.0.0", port=port or 8000)
