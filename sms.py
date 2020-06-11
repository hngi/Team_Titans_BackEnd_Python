import os
from flask import Flask, request, redirect, make_response, redirect, url_for
from flask_restplus import Api, Resource, fields
from random import randint
from twilio_api import get_twilio_criteria, twilio_responder, twilio_sender
from werkzeug.middleware.proxy_fix import ProxyFix
import os


flask_app = Flask(__name__)
flask_app.wsgi_app = ProxyFix(flask_app.wsgi_app)
app = Api(app=flask_app)
os_get = os.environ.get

sms_name_space = app.namespace('', description='SMS APIs')


"""
This is the details route. Enter the endpoint to get your details.
You can change the client_number to your number if it's registered on the current account
"""
@sms_name_space.route("/details")
@sms_name_space.route("/details/<v1>")
@sms_name_space.route("/details/<v1>/<configure>")
class Login(Resource):
    def get(self, v1=None, configure=None):
        if v1 == "v1" and configure == None:
            return {"doc": "This endpoint is for to receive details being used for the API.",
                    "GET": "This method returns a list of details you can set as headers on a client app"}
        elif (v1 or configure) and (v1 != "v1" or configure!="configure"):
            return {"error": "Wrong endpoint"}, 404
        """All this does is return JSON for you to use as headers"""
        criteria = get_twilio_criteria()
        # All this does is return JSON for you to use as headers
        return {"save these as headers, you can substitute the values with yours": criteria}


"""
This is the incoming SMS endpoint, it listens for your SMS and replies accordingly if your number is registered.
This endpoint is best left untouched if you're not developing
"""

@sms_name_space.route("/sms")
@sms_name_space.route("/sms/<v1>")
@sms_name_space.route("/sms/<v1>/<configure>")
class IncomingSms(Resource):
    def post(self, v1=None, configure=None):
        if v1 == "v1" and configure == None:
            return {"doc": "This endpoint is for programmatically replying to SMS's from registered numbers",
                    "POST": f"Send an SMS to {os_get('SENDER')} to get a reply"}
        elif (v1 or configure) and (v1 != "v1" or configure!="configure"):
            return {"error": "Wrong endpoint"}, 404
        
        """Send a dynamic reply to an incoming text message"""
        # Get the message the user sent our number
        body = request.values.get("Body", None)
        if not body:
            return {"info": "This endpoint is for listening for an incoming sms.\n Send an SMS with a verified number to get a reply"}

        # Determine the right reply for this message
        if body.lower() in ("hello", "hi"):
            message = "Hi from Team-Titans! Send 'CHECK BALANCE' or 'CB' to see your balance. \nSend 'BYE' or for a goodbye."

        elif body.lower() in ("check balance", 'cb'):
            message = f"Your balance is {randint(1000,99999)}"

        elif body.lower() in 'bye':
            message = "Goodbye"

        elif body:
            message = "Invalid message, Type 'HELLO' or 'HI' for a tip"

        # Call the Twilio Responder passing the message to it
        twiml = twilio_responder(message)
        response = make_response(str(twiml))
        response.headers["Content-type"] = "application/xml" 
        return response


"""
This endpoint is for sending an SMS to your number using your client app.
Using the headers already set from the "/details" endpoint, all you have to do is send a JSON containing the text body and the client number if you wish to change that
It results in an SMS to the client number if registered with the current account
"""

send_data = sms_name_space.model("Json data to send when calling the send endpoint",
                              {
                                  "sender":
                                  fields.String(
                                      description="Sender", required=True),
                                  "receiver":
                                  fields.String(
                                      description="Receiver", required=True),
                                  "text":
                                  fields.String(
                                      description="text", required=True)
                              }
                              )
#parser to add required headers to the request
parser = sms_name_space.parser()
parser.add_argument('account_sid', location='headers')
parser.add_argument('receiver', location='headers')
parser.add_argument('sender', location='headers')
parser.add_argument('auth_token', location='headers')

@sms_name_space.route("/send")
@sms_name_space.route("/send/<v1>")
@sms_name_space.route("/send/<v1>/<configure>", endpoint="send")
class OutgoingSms(Resource):
    @sms_name_space.expect(send_data, parser)
    def post(self, v1=None, configure=None):
        if v1 == "v1" and configure == None:
            return {"doc": "This endpoint is to send an sms to a registered number.",
                    "GET": "Receive the JSON fields to send",
                    "POST": "Send an SMS by sending the JSON fields"
                    }
        elif (v1 or configure) and (v1 != "v1" or configure!="configure"):
            return {"error": "Wrong endpoint"}, 404
        """Checking the request method to proceed if POST"""
        response = twilio_sender(request)
        return response

    def get(self, v1=None, configure=None):
        if (v1 == "v1") and (configure == None):
            return {"doc": "This endpoint is to send an sms to a registered number.",
                    "GET": "Receive the JSON fields to send, sender and receiver keys are optional and can be cleared or left as default, text is required",
                    "POST": "Send an SMS by sending the JSON fields"}
        elif (v1 or configure) and (v1 != "v1" or configure!="configure"):
            return {"error": "Wrong endpoint"}, 404
        """return JSON with criteria to fill"""
        return {"Fill out the text body and client number if empty and submit as JSON": dict(sender=request.headers.get('sender', os_get("SENDER")),
                                                                                             reciever=request.headers.get("receiver", os_get("RECEIVER")),
                                                                                             text="")
                }
if __name__ == "__main__":
    flask_app.run()