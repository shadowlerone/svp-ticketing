from flask import Flask, render_template, redirect, send_file
from json import load, dump
from io import StringIO, BytesIO
import qrcode

from event import Event, EventEncoder, EventDecoder


app = Flask(__name__)

@app.route("/")
def hello_world():
	return "<p>Hello, World!</p>"

@app.route("/<eventName>/verify/<int:ticketNumber>")
def verify(eventName, ticketNumber):
	event = readJson(eventName)
	valid = event.verify(ticketNumber)
	return render_template("verify.html", valid=valid)

@app.route("/<eventName>/generate_tickets/")
def generateTickets(eventName):
	e = readJson(eventName)
	return render_template("ticket.html", eventName=eventName, tickets=e.attendees)

def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

@app.route("/<eventName>/qrcode/<int:ticketNumber>/")
def generate_qrcode(eventName, ticketNumber):
	img = qrcode.make(f"http://svplacathédrale.ca/{eventName}/verify/{ticketNumber}")
	return serve_pil_image(img)


@app.route("/create_event/<eventName>/<int:attendees>")
def create_event(eventName,attendees):
	e = Event(eventName, attendees)
	with open(f"{eventName}.json", "w") as fp:
		dump(e, fp, cls=EventEncoder)
	return redirect(f"/{eventName}/generate_tickets")

def readJson(eventName):
	with open(f"{eventName}.json") as fp:
		return load(fp, cls=EventDecoder)
		
def writeJson(eventName, ticketNumber):
	event = readJson(eventName)
	event.append(ticketNumber)
	with open(f"{eventName}.json", "w") as fp:
		return dump(event, fp, cls=EventEncoder)