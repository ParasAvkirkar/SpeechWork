import pyaudio
import speech_recognition as sr

index = pyaudio.PyAudio().get_device_count() - 1
print(str(index))

r = sr.Recognizer()
timeout = 7
phrase_time_limit = 10
for index, name in enumerate(sr.Microphone.list_microphone_names()):
	#print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
	if index == 3:
		try:
			with sr.Microphone(device_index=index) as source:
				print('Start speaking now. I will wait for you only for {0} seconds'.format(timeout-2))
				audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

			print('Listening finished')
			try:
				print("You said " + r.recognize_google(audio))
			except LookupError:
				print("Could not understand audio")
			
		except Exception as e:
			#print(str(e))
			pass
		