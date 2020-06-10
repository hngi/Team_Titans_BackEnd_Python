from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os

def get_twilio_criteria():
    account_sid = os.environ.get("ACCOUNT_SID")
    auth_token = os.environ.get("AUTH_TOKEN")
    sender = os.environ.get("SENDER")
    receiver = os.environ.get("RECEIVER")

    return dict(account_sid=account_sid,
                auth_token=auth_token,
                sender=sender,
                receiver=receiver)

def twilio_sender(request):
    json = request.get_json()
    get = request.headers.get

    #A list of criteria so the endpoint doesn't return a 500 response should the client have missed a criteria
    #os_get = os.environ.get
    criteria = dict(
                auth_token = get("auth_token"), 
                account_sid = get("account_sid"), 
                sender = json.get("sender") or get("sender"),  
                receiver = json.get("receiver") or get("receiver"),
                text = json.get("text")
    )

    if not all(criteria.values()):
        #return a JSON containing the error message if criteria are missing
        return dict(error="Incomplete Criteria",
                    criteria = criteria), 400

    #set all the variables to be used in the Twilio request
    auth_token = criteria["auth_token"]
    account_sid = criteria["account_sid"]
    twilio_number = criteria["sender"]
    client_number = criteria["receiver"]
    text = criteria["text"]

    print(request.headers)

    #Creating the Client Object to send the SMS
    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
                    body= text,
                    from_= twilio_number,
                    to= client_number
                )
    except:
        return dict(error = "Invalid credentials or expired token"), 401

    #Sending the SMS
    print(message.sid)
    return dict(message= f"SMS sent!",
                 details= {
                     "from": twilio_number,
                     "body": text,
                     "to": client_number
                 }), 200


def twilio_responder(message):
    # Start our TwiML response
    resp = MessagingResponse()

    #Pass the message into the TwiML response
    resp.message("message")

    #return the response
    return str(resp)