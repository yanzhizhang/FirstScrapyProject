import scrapy


class PapersFile(scrapy.Item):
    author = scrapy.Field()
    href = scrapy.Field()


class CvprSpider(scrapy.Spider):
    name = "CVPR2017"

    def start_requests(self):
        urls = [
            'http://openaccess.thecvf.com/CVPR2017.py'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        page = response.url.split("/")[-2]

        filename = 'body-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

        filename = 'cspr-%s.html' % page


        authors = response.css("div.bibref").extract()
        hrefs = response.xpath('//a[contains(@href, "papers")]').extract()

        # for a in response.xpath('//a[contains(@href, "papers")]'):
        #     link = a.extract()
        #     if link.endswith('.pdf'):
        #         link = urlparse.urljoin(base_url, link)
        #         yield Request(link, callback=self.save_pdf)

        for item in zip(authors, hrefs):
            new_item = PapersFile()
            new_item['author'] = item[0]
            new_item['href'] = item[1]

            yield new_item
