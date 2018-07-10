#-*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from calaccess_scraper.items import ElectionLoader

class BallotMeasuresSpider(CrawlSpider):
    name = 'ballot-measures'
    allowed_domains = ['cal-access.sos.ca.gov']
    start_urls = ['http://cal-access.sos.ca.gov/Campaign/Measures//']
    rules = (
        # Automatically follows links found on site (follow=True by default)
        Rule(LinkExtractor(allow=[r'(\/Measures\/list\.aspx\?session=.)']), callback='get_elections'), # only getting 2017 and 2015
        #Rule(LinkExtractor(allow=('(/Detail/*)')), callback='get_committees'),
         
    )

    # TODO: Get dates of elections for the measures

    def parse_item(self, response): # If you override the parse method, the crawl spider will no longer work
        print 'Text on page ' + response.text
    
    def get_elections(self, response): # Get all measures from first page
        measures = response.xpath('//table//a/text()').extract()[21:] # Returns a list of all measures and committees
        links = response.xpath('//table//a/@href').extract()[21:] # Getting the committee funding info too
        
        d = {}
        for i in range(0,len(measures)):
            d[measures[i]] = links[i]
        
        elections = response.xpath('//table//caption//span/text()').extract()
        no_measures = response.xpath('//table//font[@color = "White"]/text()').extract() # TODO: Chop off measures at the end
        no_measures = list(map(lambda x: int(''.join(x)), list(map(lambda n: [c for c in n if c.isdigit()], no_measures))))

        for i in range(0,len(elections)):
            l = ElectionLoader(response=response)
            l.add_value('election', elections[i])
            l.add_value('no_measures', no_measures[i])
            if i == 0:
                l.add_value('measures', measures[i:no_measures[i]])
            else:
                l.add_value('measures', measures[sum(no_measures[:i])+1 : no_measures[i]+sum(no_measures[:i])+1]) 
            yield l.load_item()


        # TODO: Path should be Campaign/Measures/Detail or simply /Misc 
        # TODO: Each ballot measure can have several names

    
    def get_committees(self, response): # If the committe exists, get committee ID, name, and position
        committee_names = response.xpath('measure_name', '//span[@id="measureName"]/text()').extract()
        #committees = response.xpath('//table//a/text()').extract() # Gets committees in the detail link
        # print 'Url for committee supporting the measure: ' + response.url
        # Each committee can have several names

    def committee_contribs(self, response): # Get contributions made by committee, found on /Campaign/Committees url
        pass

    # TODO: Export data to CSV, set delay times
