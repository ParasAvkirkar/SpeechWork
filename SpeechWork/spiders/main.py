from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

if __name__ == '__main__':
	settings = get_project_settings()
	settings.set('LOG_STDOUT', False)
	settings.set('LOG_FILE', 'scrapy_output.txt')

	process = CrawlerProcess(settings)

	print('Launching spider: ' + 'dictionary'  + ' ' + 'http://www.dictionary.com/browse/acknowledgement?s=ts')

	process.crawl('dictionary.com', url='http://www.dictionary.com/browse/acknowledgement?s=ts')
	process.start() # the script will block here until the crawling is finished