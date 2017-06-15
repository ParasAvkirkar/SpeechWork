

# Currently age and female properties are not available
# They are just added as skeleton
# When a workaround or provision for such properties will be available,
# then at that time this function will modified to get voice property of that
# Currently only by accent voice proprety is returned
def get_voice_property(engine, age=30, gender='female', accent='english-us'):
	voices = engine.getProperty('voices')
	for voice in voices:
		if accent in str(voice.name):
			return voice

	raise ValueError('Demanded accent does not matched')
