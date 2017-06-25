import scrapy
import pickle

class MeaningSpider(scrapy.Spider):
    name = "dictionary.com"

    def __init__(self, **kw):
        super(MeaningSpider, self).__init__(**kw)
        self.url =kw.get('url')

        if self.url is None:
            raise ValueError('Word is empty or due to some other reason, constructor received it as None')

    def start_requests(self):
            yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        print('Parsing started.................')
        word = response.url.split('/')[-1]
        word = word[:word.index('?')]
        filename = '%s-meaning.html' % word

        meaning_strings = []
        div_tags_defcontent = response.css('div.def-content')
        for div_tag in div_tags_defcontent:
            content = div_tag.xpath('(.)//text()').extract()
            temp = []
            for element in content:
                if element.strip() is not '':
                    temp.append(element.strip())
            content = " ".join(temp)
            print(content)
            meaning_strings.append(content)

        # The working directory for scrapy based project is the top most SpeechWork directory
        # hence, unlike normal script the open clause, path starting point is two level
        # above from this current script
        with open('meanings/' + word + '.pickle', 'wb') as f:
            pickle.dump(meaning_strings, f)
            print('Pickle dumped')

        with open('scrapy_logs/html-logs/'+filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)