import scrapy


class MeaningSpider(scrapy.Spider):
    name = "dictionary.com"

    def __init__(self, **kw):
        super(MeaningSpider, self).__init__(**kw)
        self.urls = [ kw.get('url') ]
        if self.urls[0] is None:
            raise ValueError('Url is not sent or due to some other reason, constructor received it as None')

    def start_requests(self):
        # self.urls = [
        #     'http://www.dictionary.com/browse/calumny?s=ts',
        # ]
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print('Parsing started.................')
        page = response.url.split('/')[-1]
        page = page[:page.index('?')]
        filename = 'meaning-%s.html' % page
        meaning_strings = []
        div_tags_defcontent = response.css('div.def-content')
        # print(str(div_tags_defcontent))
        for div_tag in div_tags_defcontent:
            # content = div_tag.css('span::text').extract_first()
            content = div_tag.css('::text').extract_first()
            print(content)
            meaning_strings.append(content)
        print(str(meaning_strings))
       
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)