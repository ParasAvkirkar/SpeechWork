from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

if __name__ == '__main__':
	process = CrawlerProcess(get_project_settings())

	process.crawl('dictionary.com', url='http://www.dictionary.com/browse/calumny?s=ts')
	process.start() # the script will block here until the crawling is finished
	