from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings



def launch_spider(url, utility_spider_name):
	settings = get_project_settings()
	settings.set('LOG_STDOUT', False)
	settings.set('LOG_FILE', 'scrapy_logs/scrapy_output.txt')

	process = CrawlerProcess(settings)

	print('Launching spider: ' + utility_spider_name + ' ' + url)

	process.crawl(utility_spider_name, url=url)
	process.start() # the script will block here until the crawling is finished
	