from flask import Flask, request, redirect
import twilio.twiml

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def hello_monkey():
	resp = twilio.twiml.Response()
	resp.message("Hello, Mobile Monkey")
	return str(resp)

if __name__ == "__main__":
	app.run(debug=True)
