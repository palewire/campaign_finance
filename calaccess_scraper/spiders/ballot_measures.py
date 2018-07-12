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

        l = LateIndependentExpenditures(response=response)
        l.add_xpath('committee_name', '//span[@id="lblFilerName"]/text()')
        l.add_value('committee_id', re.search("(?<=id=)(.*)(?=&session)", response.url).group(1))
        l.add_value('election_year', re.search("(?<=session=)(.*)(?=&view)", response.url).group(1))
        l.add_value('lateExpenditures', expenditures)
        return l.load_item()

