from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
#from utility_spiders.utility_spiders.spiders.spider_launcher import launch_spider
from SpeechWork.spiders.spider_launcher import launch_spider


def get_word(text_spoke):
	is_dictionary_tag_found = False
	for word in text_spoke.split():
		if is_dictionary_tag_found:
			print('word: ' + word)
			return str(word)
		if 'dict' in word:
			is_dictionary_tag_found = True

def find_meaning(text_spoke):
	try:
		word = get_word(text_spoke)
		get_request_url = 'http://www.dictionary.com/browse/' + word + '?s=ts'
		print('Word found: ' + word + ' Url: ' + get_request_url)
		launch_spider(utility_spider_name='dictionary.com', url=get_request_url)

		return True
	except Exception as e:
		print(str(e))
		return False