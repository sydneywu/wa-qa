from pydantic import BaseModel

class TextContent(BaseModel):
    body: str

class Message(BaseModel):
    messaging_product: str
    to: str
    text: TextContent

class SendMessageInput(BaseModel):
    mobile: str
    text_message: str

def init_message(mobile: str, text_message: str):
    message = Message(
        messaging_product="whatsapp",
        to=mobile,
        text=TextContent(body=text_message)
    )

    return message