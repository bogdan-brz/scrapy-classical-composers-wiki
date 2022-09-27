import scrapy
import csv

with open('links.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile))

links = []
for link in data:
    links.append(link[0])

links.pop(0)

class TextSpider(scrapy.Spider):
    name = "texts"
    start_urls = links

    def parse(self, response):
        title = response.css('span.mw-page-title-main::text').get()
        p_shards = response.xpath('//p')[0].xpath('.//text()').getall()
        paragraph = "".join(p_shards)
        if len(paragraph) < 10:
            p_shards = response.xpath('//p')[1].xpath('.//text()').getall()
            paragraph = "".join(p_shards)
        paragraph = paragraph.replace('\n', ' ').replace('\r', '').strip()
        yield {'title': title, 'paragraph': paragraph}
