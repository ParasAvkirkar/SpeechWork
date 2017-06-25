from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from SpeechWork.spiders.spider_launcher import launch_spider
from speech_utilities import speak_sentences

import pickle
import os

# Currently deprecated, as a new input sanitiser is written, which returns a keyword list 
# containing word whose definition is needed
def get_word(text_spoke):
	is_dictionary_tag_found = False
	for word in text_spoke.split():
		if is_dictionary_tag_found:
			print('word: ' + word)
			return str(word)
		if 'dict' in word:
			is_dictionary_tag_found = True



def find_meaning(keywords):
	word = keywords[0]
	get_request_url = 'http://www.dictionary.com/browse/' + word + '?s=ts'
	print('Word found: ' + word + ' Url: ' + get_request_url)

	if not os.path.isfile('meanings/' + word + '.pickle'):
		launch_spider(utility_spider_name='dictionary.com', url=get_request_url)

	meaning_strings = []
	with open('meanings/' + word + '.pickle', 'rb') as f:
		meaning_strings = pickle.load(f)

	# print(meaning_strings)
	speak_sentences(meaning_strings, max_sentences_to_be_spoken=3)
	
	return 'Hope you got the answer!'