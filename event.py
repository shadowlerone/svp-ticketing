from json import JSONDecoder, JSONEncoder
class Event(object):
	def __init__(self, name, attendees):
		self.name = name
		self.attendees = attendees
		self.present = []

	def __eq__(self, other):
		return self.name == other.name and self.attendees == other.attendees and self.present == other.present

	def verify(self, ticketNumber):
		if ticketNumber in range(self.attendees):
			if ticketNumber not in self.present:
				return True
		return False

	def add_attendee(self, ticketNumber):
		if ticketNumber not in self.present:
			self.present.append(ticketNumber)

class EventEncoder(JSONEncoder):
	def default(self, obj):
		return {
			"name": obj.name,
			"attendees": obj.attendees,
			"present": obj.present
		}

class EventDecoder(JSONDecoder):
	def __init__(self, *args, **kwargs):
		super().__init__(object_hook=self.object_hook, *args, **kwargs)

	def object_hook(self, dct):
		e = Event(dct['name'], dct['attendees'])
		e.present = dct['present']
		return e