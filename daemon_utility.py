from daemon_service import Daemon

import sys
import time
import datetime

class NotifyDaemon(Daemon):

	
	def set_parameters(self, dispatcher, keywords):
		self.dispatcher = dispatcher
		self.keywords= keywords

		return

	def run(self):
		counter = 1
		while True:
			try:
				self.dispatcher(self.keywords)
				with open('notification.log', 'a') as f:
					f.write('Notification {0}: '.format(str(counter)) + str(datetime.datetime.now()))
				counter += 1
				sys.stdout.flush()
				time.sleep(120)
			except Exception as e:
				with open('error.log', 'w') as f:
					f.write('Got error at {0}: '.format(str(counter)) + str(datetime.datetime.now()))
				counter += 1				