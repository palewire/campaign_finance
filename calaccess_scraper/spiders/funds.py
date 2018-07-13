# -*- coding: utf-8 -*-
import scrapy
from calaccess_scraper.items import ContributionsReceivedLoader
import re
from w3lib.html import remove_tags

class FundsSpider(scrapy.Spider):
    name = 'funds'
    allowed_domains = ['cal-access.sos.ca.gov']
    start_urls = ['http://cal-access.sos.ca.gov/Campaign/Committees/']

    def parse(self, response): 
        m = {'dont_redirect' : True, 'handle_httpstatus_list' : [302]}
        hrefs = response.xpath('//a/@href').extract()
        hrefs = [link for link in hrefs if re.search('(Detail)', link)]
        
        if response.url == self.start_urls[0]:
            for h in hrefs:
                yield scrapy.Request(self.start_urls[0]+h, callback=self.parse)
        else:
            test = [s for s in hrefs if re.search('(.*)view=received', s)]
            for h in test:
                yield scrapy.Request('http://'+self.allowed_domains[0]+'/'+h, meta=m, callback=self.get_contribs_received) 

    def get_contribs_received(self, response):
        table = map(remove_tags, response.xpath('//table[@bordercolor="#3149aa"]//tr[@bgcolor="#fdefd3"]//td').extract())
        #table = filter(None, table) # get table of all contributors
        #table = filter(lambda c: u'\xa0' not in c, n)
        contributors = []
        contributor_names = table[0::12]
        payments = table[1::12]
        cities = table[2::12]
        states = table[3::12]
        ids = table[4::12]
        employers = table[5::12]
        occupations = table[6::12]
        amounts = table[7::12]
        trans_dates = table[9::12]
        field_dates = table[10::12]
        trans_no = table[11::12]

        for i in range (0, len(contributor_names)):
            contributors.append({'name' : contributor_names[i], 'payment_type' : payments[i], 'city' : cities[i], 'state' : states[i], 'contributor_id' : ids[i], 'employer' : employers[i], 'occupation' : occupations[i], 'amount' : amounts[i], 'trans_date' : trans_dates[i], 'field_date' : field_dates[i], 'trans_no' : trans_no[i]})
        if "view=received" in response.url:
            l = ContributionsReceivedLoader(response=response)
            l.add_value('committee_id', re.search("(?<=id=)(.*)(?=&session)", response.url).group(1))
            l.add_xpath('committee_name', '//span[@id="lblFilerName"]/text()')
            l.add_value('contributors', contributors)
            l.add_value('election_year', re.search("(?<=session=)(.*)(?=&view)", response.url).group(1))
            return l.load_item()
