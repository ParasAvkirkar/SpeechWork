import pyaudio
import speech_recognition as sr
import sys, os
import datetime

from command_notes import take_note
from command_wiki import search_wiki
from command_meaning import find_meaning
from command_cricket import get_score_live
from text_utilities import sanitize_input

def map_text_to_command(text_spoke):
	s = 'Command not recognised. Please speak again'
	try:
		
		dispatcher, new_key_words_list = sanitize_input(text_spoke)
		s = dispatcher(keywords = new_key_words_list)
		s = '' if s is None else s
	except ValueError as v:
		print(str(v))
		s = 'Failure while performing task'
	except Exception as e:
		print(str(e))
		s = 'Failure while performing task'
		exc_type, exc_obj, exc_tb = sys.exc_info()
		print('Exception at line '+ str(exc_tb.tb_lineno))
		print('Time: {0} File: {1} Line: {2} User: {3} '.format(datetime.datetime.now(), os.path.basename(__file__),
                                                                                          exc_tb.tb_lineno))

	return s


def get_microphone_source():
	pass


def listen(device_index, timeout=10, phrase_time_limit=10):
	r = sr.Recognizer()
	try:
		with sr.Microphone(device_index=device_index) as source:
			print('Listening now. Speak within {0} seconds'.format(timeout))
			# print(str(source))
			audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

		print('Listening finished')
		try:
			text_spoke = str(r.recognize_google(audio))
			# text_spoke = 'cricket pakistan versus england'
			text_spoke = text_spoke.lower()

			print("You said: " + text_spoke)	
			s = map_text_to_command(text_spoke)
			print(s)			
			
		except LookupError:
			print("Could not understand audio")
		
	except Exception as e:
		print(str(e))
		# pass
	

if __name__ == '__main__':
	# index = pyaudio.PyAudio().get_device_count() - 1
	# print(str(index))
	listen(device_index=3)