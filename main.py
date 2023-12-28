import os
from dataclasses import dataclass
from fastapi import FastAPI, Response, Form, Depends
from twilio.rest import Client
from gen_ai_services import DialogFlowReply

# Initialize FastAPI app
app = FastAPI()

# Load environment variables
account_sid = os.environ.get("accountSID")  # Twilio account SID
auth_token = os.environ.get("authToken")  # Twilio auth token
language_code = os.environ.get("languageCode")  # Language code (ISO format)


# Define data model
@dataclass
class TwilioForm:
    Body: str = Form(...)
    From: str = Form(...)
    To: str = Form(...)


@app.post("/twilio-dialogflowcx")
async def twilio_dialogflowcx(form: TwilioForm = Depends()):
    """Handles incoming WhatsApp messages, send them to Dialogflow CX and
    replies to the user with the agent's response.

    Args:
       form: TwilioForm object containing the received message data.

    Returns:
       Response object indicating success or failure of the operation.

    Raises:
       Exception: If an error occurs during Twilio message sending.
    """
    received_msg = form.Body
    user_number = form.From
    twilio_number = form.To

    # Create Twilio and call Dialogflow agent
    twilio_client = Client(account_sid, auth_token)
    dialogflow_cx = DialogFlowReply(session_id=user_number)
    response = dialogflow_cx.send_request(
        message=received_msg, language_code=language_code
    )
    if len(response) == 0:
        return Response(status_code=400, content="No message returned.")
    for message in response:
        if message.text:
            agent_response = message.text.text[0]
            # Send message through Twilio API
            try:
                twilio_client.messages.create(
                    to=user_number,
                    from_=twilio_number,
                    body=f"{agent_response}",
                )
            except Exception as error:
                print(error)
                return Response(status_code=500, content=error)
    return Response(status_code=200, content="Message Sent!")
