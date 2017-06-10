import pyaudio
import speech_recognition as sr
from notes_command import take_note
from wiki_command import search_wiki


def map_text_to_command(text_spoke):
	s = 'Command not recognised. Please speak again' 
	if 'take' in text_spoke and 'note' in text_spoke:
		is_success = take_note(text_spoke)
		s = 'Note taken' if is_success else 'Failure while taking note'
	elif 'wiki' in text_spoke:
		is_success = search_wiki(text_spoke)
		s = 'Wiki search made. Please be patient for the page to load!' if is_success else 'Failure in search'
	return s


def get_microphone_source():
	pass


def listen(device_index, timeout=10, phrase_time_limit=10):
	r = sr.Recognizer()
	try:
		with sr.Microphone(device_index=device_index) as source:
			print('Listening now. Speak within {0} seconds'.format(timeout + phrase_time_limit - 5))
			audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

		print('Listening finished')
		try:
			text_spoke = str(r.recognize_google(audio))
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