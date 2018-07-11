#-*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from calaccess_scraper.items import ElectionLoader, MeasureLoader, CommitteeLoader
import re
from w3lib.html import remove_tags

class BallotMeasuresSpider(CrawlSpider):
    name = 'ballot-measures'
    allowed_domains = ['cal-access.sos.ca.gov']
    start_urls = ['http://cal-access.sos.ca.gov/Campaign/Measures//']
    rules = (
        #Automatically follows links found on site (follow=True by default)
        #Rule(LinkExtractor(allow=[r'(\/Measures\/list\.aspx\?session=).']), callback='get_elections'), # only getting 2017 and 2015
        Rule(LinkExtractor(allow=(r'(\/Detail).*')), callback='get_measures'),
    )

    def parse_item(self, response): # If you override the parse method, the crawl spider will no longer work
        print 'Text on page ' + response.text
    
    def get_elections(self, response): # Get all measures from first page
        measures = response.xpath('//table//a/text()').extract()[21:] # Returns a list of all measures and committees
        links = response.xpath('//table//a/@href').extract()[21:] 
        d = {}
        for i in range(0,len(measures)):
            d[measures[i]] = links[i]
        
        elections = response.xpath('//table//caption//span/text()').extract()
        no_measures = response.xpath('//table//font[@color = "White"]/text()').extract()
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

    def get_measures(self, response): # If the committe exists, get committee ID, name, and position
        committee_names = response.xpath('//table//a[@class = "sublink2"]/text()').extract()
        id_pos = response.xpath('//table//span[@class="txt7"]/text()').extract()
        positions = id_pos[1::2]
        committee_ids = id_pos[0::2]
        support = []
        oppose = []

        for i in range(0,len(positions)):
            if positions[i] == 'OPPOSE':
                oppose.append({'committee_id' : committee_ids[i], 'committee_name' : committee_names[i]})
            elif positions[i] == 'SUPPORT':
                support.append({'committee_id' : committee_ids[i], 'committee_name' : committee_names[i]})
        
        l = MeasureLoader(response=response)
        l.add_xpath('measure_name', '//span[@id="measureName"]/text()')
        l.add_value('measure_id', re.search("id=(.*)\&", response.url).group(1))
        l.add_value('supporting_committees', support)
        l.add_value('opposing_committees', oppose)
        return l.load_item()

    def get_committees(self, response): # Get contributions made by committee, found on /Campaign/Committees url
        summary = remove_tags(response.xpath('//table//td[@width="50%"]').extract())
        
        l = CommitteeLoader(response=response)
        l.add_xpath('committee_id', '//span[@id="_ctl3_lblFilerId"]/text()')
        l.add_xpath('committee_name', '//span[@id="lblFilerName"]/text()')
        l.add_value('election_cycle', response.url[-4:])
        l.add_xpath('historical_names', '//table[@id="_ctl3_names"]//td/text()')
        l.add_value('status', summary[1])
        l.add_value('reporting_period', summary[5])
        l.add_value('current_contributions', summary[7])
        l.add_value('year_contributions', summary[9])
        l.add_value('current_expenditures', summary[11])
        l.add_value('year_expenditures', summary[13])
        l.add_value('ending_cash', sumary[15])
        return l.load_item()

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

        l = ContributionsReceivedLoader(response=response)
        l.add_value('committee_id', re.search("(?<=id=)(.*)(?=&session)", response.url).group(1))
        l.add_xpath('committee_name', '//span[@id="lblFilerName"]/text()')
        l.add_value('contributors', contributors)
        l.add_value('election_year', re.search("(?<=session=)(.*)(?=&view)", response.url).group(1))
        return l.load_item()

    def get_contribs_made(self, response):
        table = map(remove_tags, response.xpath('//table[@id="_ctl3_contributions"]//tr[@bgcolor="#FDEFD3"]//td').extract())    
        dates = tables[0::6]

        l = ContributionsMadeLoader(response=response)
        l.add_value('committee_id', re.search("(?<=id=)(.*)(?=&session)", response.url).group(1))
        l.add_xpath('committee_name', '//span[@id="lblFilerName"]/text()')
        return l.load_item()

    def get_expenditures(self, response):
        pass

    def get_late_funding(self, response):
        pass

    def get_electronic_filings(self, response):
        pass
