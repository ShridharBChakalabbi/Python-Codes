from twilio.rest import Client

# the following line needs your Twilio Account SID and Auth Token
client = Client("AC1fc441077205651b5ac9b2263acc09c9", "ef398e0801c9b67100a5b97452f9a117")

# change the "from_" number to your Twilio number and the "to" number
# to the phone number you signed up for Twilio with, or upgrade your
# account to send SMS to any phone number
client.messages.create(to="+919148192989", 
                       from_="+18035251165", 
                       body="Hello from Python!")


# Download the helper library from https://www.twilio.com/docs/python/install
#==============================================================================
# from twilio.rest import Client
# 
# 
# # Your Account Sid and Auth Token from twilio.com/console
# account_sid = 'AC1fc441077205651b5ac9b2263acc09c9'
# auth_token = 'ef398e0801c9b67100a5b97452f9a117'
# client = Client(account_sid, auth_token)
# 
# message = client.messages \
#     .create(
#          body='This is the ship that made the Kessel Run in fourteen parsecs?',
#          from_='+18035251165',
#          to='+919148192989'
#      )
# 
# print(message.sid)
# 
# import os
# from twilio.rest import Client
#  
#  
# account_sid = os.environ.get('AC1fc441077205651b5ac9b2263acc09c9')
# auth_token = os.environ.get('ef398e0801c9b67100a5b97452f9a117')
#  
# client = Client(account_sid, auth_token)
#  
# client.messages.create(from_=os.environ.get('+18035251165'),
#                       to=os.environ.get('+919148192989'),
#                       body='You just sent an SMS from Python using Twilio!')
# 
#==============================================================================
