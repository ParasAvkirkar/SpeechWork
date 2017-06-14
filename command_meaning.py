from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from SpeechWork.spiders.spider_launcher import launch_spider
from utilities import get_voice_property

import pickle
import pyttsx
import os

def get_word(text_spoke):
	is_dictionary_tag_found = False
	for word in text_spoke.split():
		if is_dictionary_tag_found:
			print('word: ' + word)
			return str(word)
		if 'dict' in word:
			is_dictionary_tag_found = True


# Meaning strings are strings returned by spider
# Only fix number of top defintions would be 'said' by PyTTSx Engine
def say(meaning_strings, top_definitions=3):
	engine = pyttsx.init()
	engine.setProperty('rate', 150)

	i = 1
	voice = get_voice_property(engine, age=10, gender='female')
	engine.setProperty('voice', voice.id)
	for s in meaning_strings:
	    if i > top_definitions:
	    	break
	    
	    print(s)
	    engine.say(s)
	    i += 1    
	engine.runAndWait()

def find_meaning(text_spoke):
	word = get_word(text_spoke)
	get_request_url = 'http://www.dictionary.com/browse/' + word + '?s=ts'
	print('Word found: ' + word + ' Url: ' + get_request_url)

	if not os.path.isfile('meanings/' + word + '.pickle'):
		launch_spider(utility_spider_name='dictionary.com', url=get_request_url)

	meaning_strings = []
	with open('meanings/' + word + '.pickle', 'rb') as f:
		meaning_strings = pickle.load(f)

	# print(meaning_strings)
	say(meaning_strings)