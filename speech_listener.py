import pyaudio
import speech_recognition as sr
import sys, os
import datetime

from command_notes import take_note
from command_wiki import search_wiki
from command_meaning import find_meaning
from command_cricket import get_score_live

def map_text_to_command(text_spoke):
	s = 'Command not recognised. Please speak again'
	try:
		if 'take' in text_spoke and 'note' in text_spoke:
			take_note(text_spoke)
			s = 'Note taken'
		elif 'wiki' in text_spoke:
			search_wiki(text_spoke)
			s = 'Wiki search made. Please be patient for the page to load!'
		elif 'dictionary' in text_spoke:
			find_meaning(text_spoke) 
			s = 'Hope you got the answer!'
		elif 'cric' in text_spoke:
			get_score_live(text_spoke)
			s = 'Grace is always complementary with sport-skills!'
	except ValueError as v:
		print(str(v))
		s = 'Failure while performing task'
	except Exception as e:
		print(str(e))
		s = 'Failure while performing task'
		# print('Exception at line '+ str(exc_tb.tb_lineno))
		# exc_type, exc_obj, exc_tb = sys.exc_info()
		# print('Time: {0} File: {1} Line: {2} User: {3} '.format(datetime.datetime.now(), os.path.basename(__file__),
  #                                                                                         exc_tb.tb_lineno))

	return s


def get_microphone_source():
	pass


def listen(device_index, timeout=10, phrase_time_limit=10):
	r = sr.Recognizer()
	try:
		with sr.Microphone(device_index=device_index) as source:
			print('Listening now. Speak within {0} seconds'.format(timeout + phrase_time_limit - 5))
			print(str(source))
			audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

		print('Listening finished')
		try:
			text_spoke = str(r.recognize_google(audio))
			# text_spoke = 'cricket pakistan versus england'
			text_spoke = text_spoke.lower()

			print("You said " + text_spoke)	
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