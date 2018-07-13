# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from calaccess_scraper.items import CommitteeLoader
import re
from w3lib.html import remove_tags

class CommitteesSpider(CrawlSpider):
    name = 'committees'
    allowed_domains = ['cal-access.sos.ca.gov']
    start_urls = ['http://cal-access.sos.ca.gov/Campaign/Committees']
    rules = (
        Rule(LinkExtractor(allow=(r'(\/Detail).*')), callback='get_committees'),
    )

    def get_committees(self, response): # TODO: Check for errors
        summary = map(remove_tags, (response.xpath('//table//td[@width="50%"]').extract()))
        status = summary[1]

        if (len(summary) > 2):
            reporting_period = summary[5]
            curr_contribs = summary[7]
            year_contribs = summary[9]
        if (len(summary) > 11):
            curr_expend = summary[11]
            year_expend = summary[13]
            ending_cash = summary[15]
        else:
            curr_expend = ''
            year_expend = ''
            ending_cash = ''
        if (len(summary) <= 2):
            reporting_period = ''
            curr_contribs = ''
            year_contribs = ''

        l = CommitteeLoader(response=response)
        l.add_xpath('committee_id', '//span[@id="_ctl3_lblFilerId"]/text()')
        l.add_xpath('committee_name', '//span[@id="lblFilerName"]/text()')
        l.add_value('election_cycle', response.url[-4:])
        l.add_xpath('historical_names', '//table[@id="_ctl3_names"]//td/text()')
        l.add_value('status', status)
        l.add_value('reporting_period', reporting_period)
        l.add_value('current_contributions', curr_contribs)
        l.add_value('year_contributions', year_contribs)
        l.add_value('current_expenditures', curr_expend)
        l.add_value('year_expenditures', year_expend)
        l.add_value('ending_cash', ending_cash)
        return l.load_item()
