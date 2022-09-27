import scrapy

class LinkSpider(scrapy.Spider):
    name = "links"

    def start_requests(self):
        url = "https://en.wikipedia.org/wiki/Category:19th-century_classical_composers"
        yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        mwpages = response.css('div#mw-pages')
        list = []
        for group in mwpages.css('div.mw-category-group'):
            list = list + group.css('a')
        for ahref in list:
            local_url = ahref.attrib['href']
            yield {"link": f"https://en.wikipedia.org{local_url}"}

        next_page = response.xpath("//*[contains(text(), 'next page')]")[0].attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse, dont_filter=True)