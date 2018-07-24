# -*- coding: utf-8 -*-
import scrapy
from calaccess_scraper.items import CandidatesLoader
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re

class CandidatesSpider(CrawlSpider):
    name = 'candidates'
    allowed_domains = ['cal-access.sos.ca.gov']
    start_urls = ['http://cal-access.sos.ca.gov/Campaign/Candidates/']
    rules = (
        Rule(LinkExtractor(allow=(r'(\/Detail).*')), callback='get_candidates'),
    )

    def get_candidates(self, response):
        lim = response.xpath('//table[@id="_ctl3_limits"]//text()').extract()
        spending_limits = { "election" : lim[6], "spending_limits" : lim[7]}

        races = []
        r = response.xpath('//table//td[@class="txt7"]//text()').extract()
        office = r[0::2]
        election = r[1::2]
        result = response.xpath('//table//td[@class="hdr13"]//text()').extract()
        for i in range(0,len(result)):
            curr = races.append({ "office" : office[i], "election" : election[i], "result" : result[i]})

        committees = []
        title_ids = response.xpath('//table//td[@colspan="2"]//text()').extract()[98:]
        title_ids = [x for x in title_ids if "Form 460/461/450" not in x]
        c_names = [x for x in title_ids if "ID#" not in x]
        c_ids = [x for x in title_ids if "ID#" in x]
        committee_info = response.xpath('//table//td[@width="50%"]//text()').extract()
        last_index = 0 # index to keep track of committee name
        for i in range(0,len(c_names)):
            if last_index < len(committee_info) - 3:
                if committee_info[last_index+2] != "CURRENT STATUS": # if [current_status + 2] != "current_status", there's more info
                    c_names[i]
                    c_ids[i]
                    info = committee_info[last_index:16] # Add 16 to get all values

                    if info:
                        committees.append( { "committee_id" : c_ids[i], "committee_name" : c_names[i], "current_status" : info[1], \
                        "last_report_date" : info[3], "reporting_period" : info[5], "curr_contributions" : info[7], "total_contribs" : info[9], \
                        "curr_expenditures" : info[11], "total_expenditures" : info[13], "ending_cash" : info[15]} )
                    else:
                        committees.append( { "committee_id" : c_ids[i], "committee_name" : c_names[i] } )
                    last_index += 16 # reset index
                else: # Committee has not filed form 460/461/450
                    committees.append( { "committee_id" : c_ids[i], "committee_name" : c_names[i], "current_status" : committee_info[last_index+2]} )
                    last_index += 3
            if last_index - len(committee_info) == 3: # Get last item
                committees.append( { "committee_id" : c_ids[i], "committee_name" : c_names[i], "current_status" : committee_info[-1]} )

        l = CandidatesLoader(response=response)
        l.add_value('candidate_id', re.search("(?<=id=)(.*)", response.url).group(1))
        l.add_xpath('candidate_name', '//span[@id="lblFilerName"]/text()')
        l.add_xpath('party', '//span[@class="hdr15"]/text()')
        l.add_value('spending_limits', spending_limits)
        l.add_value('races', races)
        l.add_value('committees', committees)
        return l.load_item()
