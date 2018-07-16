# -*- coding: utf-8 -*-
import scrapy
from calaccess_scraper.items import ContributionsReceivedLoader, ContributionsMadeLoader, ExpenditureLoader, LateFundingLoader, LateIndependentExpendituresLoader
import re
from w3lib.html import remove_tags
from calaccess_scraper.errors import errback_httpbin

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
            received = [s for s in hrefs if re.search('(.*)view=received', s)]
            made = [s for s in hrefs if re.search('(.*)view=contributions', s)]
            print received
            exp = [s for s in hrefs if re.search('(.*)view=expenditures', s)]
            late5000 = [s for s in hrefs if re.search('(.*)view=late1', s)]
            late = [s for s in hrefs if re.search('(.*)view=late2', s)]
            late_exp = [s for s in hrefs if re.search('(.*)view=late3', s)]

            for h in received:
                yield scrapy.Request('http://'+self.allowed_domains[0]+'/'+h, meta=m, callback=self.get_contribs_received, errback=errback_httpbin)
            for h in made:
                yield scrapy.Request('http://'+self.allowed_domains[0]+'/'+h, meta=m, callback=self.get_contribs_made, errback=errback_httpbin)
            for h in exp:
                yield scrapy.Request('http://'+self.allowed_domains[0]+'/'+h, meta=m, callback=self.get_expenditures, errback=errback_httpbin)
            for h in late5000:
                yield scrapy.Request('http://'+self.allowed_domains[0]+'/'+h, meta=m, callback=self.get_late_contributions, errback=errback_httpbin)
            for h in late:
                yield scrapy.Request('http://'+self.allowed_domains[0]+'/'+h, meta=m, callback=self.get_late_contributions, errback=errback_httpbin)
            for h in late_exp:
                yield scrapy.Request('http://'+self.allowed_domains[0]+'/'+h, meta=m, callback=self.get_late_expenditures, errback=errback_httpbin)

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

    def get_contribs_made(self, response):
        table = map(remove_tags, response.xpath('//table[@id="_ctl3_contributions"]//td').extract())
        table = table[6:]
        date = table[0::6]
        payee = table[1::6]
        contest = table[2::6]
        position = table[3::6]
        payment_type = table[4::6]
        amount = table[5::6]
        contributors = []

        for i in range(0, len(date)):
            contributors.append({'date' : date[i], 'payee' : payee[i], 'contest' : contest[i], 'position' : position[i], 'payment_type' : payment_type[i], 'amount' : amount[i] })

        l = ContributionsMadeLoader(response=response)
        l.add_value('committee_id', re.search("(?<=id=)(.*)(?=&session)", response.url).group(1))
        l.add_xpath('committee_name', '//span[@id="lblFilerName"]/text()')
        l.add_value('contributions', contributors)
        l.add_value('election_year', re.search("(?<=session=)(.*)(?=&view)", response.url).group(1))
        return l.load_item()

    def get_expenditures(self, response):
        table = map(remove_tags,response.xpath('//table[@id="_ctl3_expenditures"]//td').extract())
        table = table[5:]
        date = table[0::5]
        payee = table[1::5]
        exp_code = table[2::5]
        desc = table[3::5]
        amount = table[4::5]
        expenditures = []

        for i in range(0, len(date)):
            expenditures.append({'date' : date[i], 'payee' : payee[i], 'expenditure_code' : exp_code[i], 'description' : desc[i], 'amount' : amount[i] })

        l = ExpenditureLoader(response=response)
        l.add_value('election_year', re.search("(?<=session=)(.*)(?=&view)", response.url).group(1))
        l.add_value('committee_id', re.search("(?<=id=)(.*)(?=&session)", response.url).group(1))
        l.add_xpath('committee_name', '//span[@id="lblFilerName"]/text()')
        l.add_value('expenditure', expenditures)
        return l.load_item()

    def get_late_contributions(self, response):
        table = map(remove_tags, response.xpath('//table//tr[@bgcolor="#fdefd3"]/td').extract())
        name = table[0::11]
        city = table[1::11]
        state = table[2::11]
        ids = table[3::11]
        employer = table[4::11]
        occupation = table[5::11]
        amount = table[6::11]
        types = table[7::11]
        trans_date = table[8::11]
        filed_date = table[9::11]
        trans_no = table[10::11]
        contributions = []

        for i in range(0, len(name)):
            contributions.append({'name' : name[i], 'city' : city[i], 'state' : state[i], 'contribution_id' : ids[i], 'employer' : employer[i], 'occupation' : occupation[i], 'amount' : amount[i], 'type' : types[i], 'trans_date' : trans_date[i], 'filed_date' : filed_date[i], 'trans_no' : trans_no[i]})

        l = LateFundingLoader(response=response)
        l.add_xpath('committee_name', '//span[@id="lblFilerName"]/text()')
        l.add_value('committee_id', re.search("(?<=id=)(.*)(?=&session)", response.url).group(1))
        l.add_value('election_year', re.search("(?<=session=)(.*)(?=&view)", response.url).group(1))
        l.add_value('funding_type', remove_tags(response.xpath('//span[@class="hdr11"]').extract()[-1]))
        l.add_value('contributions', contributions)
        return l.load_item()

    def get_late_expenditures(self, response):
        table = map(remove_tags,response.xpath('//table//td').extract())
        table = table[46:]
        expenditures = []

        ind = [i for i, x in enumerate(table) if x == 'NAME'] # Find all indices of name
        for i in range(0, len(ind)):
            if i != len(ind) - 1:
                sub_table = table[ind[i] : ind[i+1]] # get all subtables from array
                name = sub_table[3]
                contest = sub_table[4]
                position = sub_table[5]
                amount = sub_table[11::5]
                types = sub_table[12::5]
                trans_date = sub_table[13::5]
                filed_date = sub_table[14::5]
                trans_no = sub_table[15::5]
                expenditures.append({'name' : name, 'contest' : contest, 'position' : position, 'amount' : amount, 'type' : types, 'trans_date' : trans_date, 'filed_date' : filed_date, 'trans_no' : trans_no })

        l = LateIndependentExpendituresLoader(response=response)
        l.add_xpath('committee_name', '//span[@id="lblFilerName"]/text()')
        l.add_value('committee_id', re.search("(?<=id=)(.*)(?=&session)", response.url).group(1))
        l.add_value('election_year', re.search("(?<=session=)(.*)(?=&view)", response.url).group(1))
        l.add_value('lateExpenditures', expenditures)
        return l.load_item()
