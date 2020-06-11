import os
from flask import Flask, request, redirect, make_response, redirect, url_for
from flask_restplus import Api, Resource, fields
from random import randint
from twilio_api import get_twilio_criteria, twilio_responder, twilio_sender
from werkzeug.middleware.proxy_fix import ProxyFix


flask_app = Flask(__name__)
flask_app.wsgi_app = ProxyFix(flask_app.wsgi_app)
app = Api(app=flask_app)




sms_name_space = app.namespace('', description='SMS APIs')




"""
This is the details route. Enter the endpoint to get your details.
You can change the client_number to your number if it's registered on the current account
"""
@sms_name_space.route("/details")
class Login(Resource):
    def get(self):
        """All this does is return JSON for you to use as headers"""
        criteria = get_twilio_criteria()
        # All this does is return JSON for you to use as headers
        return {"save these as headers, you can substitute the values with yours": criteria}


"""
This is the incoming SMS endpoint, it listens for your SMS and replies accordingly if your number is registered.
This endpoint is best left untouched if you're not developing
"""


@sms_name_space.route("/sms")
class IncomingSms(Resource):
    def post(self):
        """Send a dynamic reply to an incoming text message"""
        # Get the message the user sent our number
        body = request.values.get("Body", None)
        if not body:
            return {"info": "This endpoint is to be accessed by sending an SMS to the Twilio number with a registered number"}, 403

        # Determine the right reply for this message
        if body.lower() in ("hello", "hi"):
            message = "Hi from Team-Titans! Send 'CHECK BALANCE' or 'CB' to see your balance. \nSend 'BYE' for a goodbye."

        elif body.lower() in ("check balance", 'CB'):
            message = f"Your balance is {randint(1000,99999)}"

        elif body.lower() == 'bye':
            message = "Goodbye"

        elif body:
            message = "Invalid message, Type 'HELLO' or 'HI' for a tip"

        # Call the Twilio Responder passing the message to it
        twiml = twilio_responder(message)
        response = make_response(str(twiml))
        response.headers["Content-Type"] = "application/xml"

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

@sms_name_space.route("/send", endpoint="send")
class OutgoingSms(Resource):
    @sms_name_space.expect(send_data, parser)
    def post(self):
        """Checking the request method to proceed if POST"""
        response = twilio_sender(request)
        return response

    def get(self):
        """return JSON with criteria to fill"""
        return {"Fill out the text body and client number if empty and submit as JSON": dict(sender=request.headers.get('sender'),
                                                                                             reciever=request.headers.get("receiver"),
                                                                                             text="")
                }
