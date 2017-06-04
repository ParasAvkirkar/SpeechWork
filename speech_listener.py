import pyaudio
import speech_recognition as sr

index = pyaudio.PyAudio().get_device_count() - 1
print(str(index))


def map_text(text_spoke):
	pass

def listen():
	r = sr.Recognizer()
	for index, name in enumerate(sr.Microphone.list_microphone_names()):
		#print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
		if index == 3:
			try:
				with sr.Microphone(device_index=index) as source:
					print('Listening')
					audio = r.listen(source, timeout=10, phrase_time_limit=10)

				print('Listening finished')
				try:
					text_spoke = str(r.recognize_google(audio))
					print("You said " + text_spoke)

				except LookupError:
					print("Could not understand audio")
				
			except Exception as e:
				#print(str(e))
				pass
	

if __name__ == '__main__':
	listen()