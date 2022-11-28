from event import Event, EventDecoder, EventEncoder
import json


filename='test.json'
event = Event("Test", 70)
with open(filename, 'w') as jsonfile:
    json.dump(event, jsonfile, cls=EventEncoder)
with open(filename, 'r') as jsonfile:
    event1 = json.load(jsonfile, cls=EventDecoder)
assert event1 == event