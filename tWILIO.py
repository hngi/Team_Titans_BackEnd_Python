from twilio.rest import Client


# My Account Sid and Auth Token from twilio.com/console
account_sid = 'ACc75351ad26839498cb52f10141689b32'
auth_token = '6882e64bc73b56370ea798c3380f4e7a'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Hello User",
                     from_='+15017122661',
                     to='+2348143142973'
                 )
#Sends message to user
print(message.sid)
