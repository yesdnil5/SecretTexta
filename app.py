from flask import Flask, request, redirect
import twilio.twiml
from people import peopleDict

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def hello_monkey():
	f = open('testResponse.txt', 'w')
	body = request.values.get('Body', None)
	from_number = request.values.get('From', None)
	if from_number in peopleDict.keys():
		message = "Thank you, " + peopleDict[from_number] + ".  I will ask you for your wishlist soon."
		f.write(peopleDict[from_number] + " :" + body)
	else:
		message = "You are not participating in this Secret Santa."
	resp = twilio.twiml.Response()
	resp.message(message)
	return str(resp)

if __name__ == "__main__":
	app.run(host='0.0.0.0')
