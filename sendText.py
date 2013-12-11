from twilio.rest import TwilioRestClient
from credentials import account_sid, token
from people import peopleDict

for number in peopleDict:
	client = TwilioRestClient(account_sid, token)
	body1 = "This is Lindsey about Secret Santa!"
	body2 = "Is this " + peopleDict[number] + " and are you participating?"
	message = client.sms.messages.create(body=body1, to=number, from_="+14106964419")
	print message.sid
	message = client.sms.messages.create(body=body2, to=number, from_="+14106964419")
	print message.sid
