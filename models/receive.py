
from pydantic import BaseModel, Field
from typing import List, Optional


class Profile(BaseModel):
    name: str


class Text(BaseModel):
    body: str


class Message(BaseModel):
    from_: str = Field(..., alias="from")
    id: str
    timestamp: str
    text: Text
    type: str


class Metadata(BaseModel):
    display_phone_number: str
    phone_number_id: str


class Contact(BaseModel):
    profile: Profile
    wa_id: str


class Value(BaseModel):
    messaging_product: str
    metadata: Metadata
    contacts: List[Contact]
    messages: List[Message]


class Change(BaseModel):
    value: Value
    field: str


class Entry(BaseModel):
    id: str
    changes: List[Change]


class WhatsappIncomingData(BaseModel):
    object: str
    entry: List[Entry]


# Parsing the JSON
json_data = {
    "object": "whatsapp_business_account",
    "entry": [
        {
            "id": "100283353032215",
            "changes": [
                {
                    "value": {
                        "messaging_product": "whatsapp",
                        "metadata": {
                            "display_phone_number": "66974171461",
                            "phone_number_id": "108011825584270"
                        },
                        "contacts": [
                            {
                                "profile": {
                                    "name": "Sydney"
                                },
                                "wa_id": "6591891331"
                            }
                        ],
                        "messages": [
                            {
                                "from": "6591891331",
                                "id": "wamid.HBgKNjU5MTg5MTMzMRUCABIYFDNBOUMxOTg3Q0YwNDUzQzVBRUY5AA==",
                                "timestamp": "1683312729",
                                "text": {
                                    "body": "hi i am sydney from lobang app. i have a question\n\nhow do i do this\n👍"
                                },
                                "type": "text"
                            }
                        ]
                    },
                    "field": "messages"
                }
            ]
        }
    ]
}

whatsapp_account = WhatsappIncomingData(**json_data)