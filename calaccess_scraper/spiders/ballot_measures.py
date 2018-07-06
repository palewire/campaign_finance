# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class BallotMeasuresSpider(CrawlSpider):
    name = 'ballot-measures'
    allowed_domains = ['cal-access.sos.ca.gov']
    start_urls = ['http://cal-access.sos.ca.gov/Campaign/Measures//']
    rules = (
        # Automatically follows links found on site (follow=True by default)
        Rule(LinkExtractor(allow=('/Measures')), callback='get_measures'),
        #Rule(LinkExtractor(allow=('(/Detail/*)')), callback='get_committees'),
         
    )

    def parse_item(self, response): # If you override the parse method, the crawl spider will no longer work
        print 'Text on page ' + response.text
    
    def get_measures(self, response): # Get all measures from first page
        measures = response.xpath('//table//a/text()').extract()[21:] # Returns a list of all measures
        links = response.xpath('//table//a/@href').extract()[21:] # Getting the committee funding info too
        print links
        # TODO: Match with related URL to lign up with committee info
        #print measures

    def get_committees(self, response): # If the committe exists, get committee ID, name, and position
        committees = response.xpath('//table//a/text()').extract() # Gets committees in the detail link
        print committees
        print 'Url for committee info: ' + response.url
        # Follow URL, get committee funding info in next URL

    def committee_contribs(self, response): # Get contributions made by committee, found on /Campaign/Committees url
        pass

    # TODO: Export data to CSV, set delay times
