# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Compose, MapCompose
from w3lib.html import remove_tags

# Helper functions for preprocessing
def clean(s):
    s = s.strip('-')
    s = s.strip('.')
    s = s.strip(',')
    return s.lower()

def to_int(s):
    return int(s)

# Ballot Measure Items and Loaders
class Election(scrapy.Item):
    election = scrapy.Field()
    no_measures = scrapy.Field()
    measures = scrapy.Field(serializer=str)

class ElectionLoader(ItemLoader):
    default_item_class = Election
    election_in = MapCompose(clean)
    no_measures_in = Compose()
    measures_in = MapCompose(clean)

class Measure(scrapy.Item):
    measure_name = scrapy.Field()
    measure_id = scrapy.Field() # Measure id is in the URL
    supporting_committees = scrapy.Field()
    opposing_committees = scrapy.Field()

class MeasureLoader(ItemLoader): # TODO: Fix loaders, not preprocessing text correctly
    default_item_class = Measure
    measureName_in = Compose(clean)
    measureId_in = MapCompose(to_int)
    support_in = MapCompose(remove_tags, clean)
    oppose_in = MapCompose(remove_tags, clean)

class Committee(scrapy.Item):
    committee_id = scrapy.Field()
    committee_name = scrapy.Field()
    election_cycle = scrapy.Field()
    historical_names = scrapy.Field(serializer=str)
    status = scrapy.Field()
    reporting_period = scrapy.Field()
    current_contributions = scrapy.Field()
    year_contributions = scrapy.Field() 
    current_expenditures = scrapy.Field()
    year_expenditures = scrapy.Field()
    ending_cash = scrapy.Field()

class CommitteeLoader(ItemLoader):
    default_item_class = Committee
    committeeId_in = Compose(to_int)
    committeeName_in = MapCompose(clean)
    electionCycle_in = MapCompose(clean)
    historicalNames_in = MapCompose(clean)
    status_in = MapCompose(clean)
    reportingPeriod_in = MapCompose()
    currContribs_in = MapCompose(clean)
    yearContribs_in = MapCompose(clean)
    currExpend_in = MapCompose(clean)
    yearExpend_in = MapCompose(clean)
    endingCash_in = MapCompose(clean)

class ContributionsReceived(scrapy.Item):
    committee_id = scrapy.Field()
    committee_name = scrapy.Field()
    contributors = scrapy.Field()
    payment_type = scrapy.Field()
    city = scrapy.Field()
    state_zip = scrapy.Field()
    amount = scrapy.Field()
    trans_date = scrapy.Field()
    filed_date = scrapy.Field()
    employer = scrapy.Field()
    occupation = scrapy.Field()
    id_number = scrapy.Field()
    election_cycle = scrapy.Field()
    trans_no = scrapy.Field()

class ContributionsReceivedLoader(ItemLoader):
    default_item_class = ContributionsReceived
    committeeId_in = Compose(to_int)
    committeeName_in = MapCompose(clean)
    contributor_in = MapCompose(clean)
    paymentType_in = MapCompose(clean)
    city_in = MapCompose(clean)
    stateZip_in = MapCompose(clean)
    amount_in = MapCompose(clean)
    transDate_in = MapCompose(clean)
    filedDate_in = MapCompose(clean)
    employer_in = MapCompose(clean)
    occupation_in = MapCompose(clean)
    id_no_in = MapCompose(clean)
    electionCycle_in = MapCompose(clean)
    trans_no_in = MapCompose(clean)

class ContributionsMade(scrapy.Item):
    committee_name = scrapy.Field()
    date = scrapy.Field()
    payee = scrapy.Field()
    contest = scrapy.Field()
    position = scrapy.Field()
    payment_type = scrapy.Field()
    amount = scrapy.Field()
    election_cycle = scrapy.Field()

class ContributionsMadeLoader(ItemLoader):
    default_item_class = ContributionsMade
    committeeName_in = MapCompose(clean)
    date_in = MapCompose(clean)
    payee_in = MapCompose(clean)
    contest_in = MapCompose(clean)
    position_in = MapCompose(clean)
    paymentType_in = MapCompose(clean)
    amount_in = MapCompose(clean)
    electionCycle_in = MapCompose(clean)

class ExpendituresMade(scrapy.Item):
    date = scrapy.Field()
    payee = scrapy.Field()
    expenditure_code = scrapy.Field()
    description = scrapy.Field()
    amount = scrapy.Field()
    election_cycle = scrapy.Field()
    committee_name = scrapy.Field()

class ExpenditureLoader(ItemLoader):
    default_item_class = ExpendituresMade
    date_in = MapCompose(clean)
    payee_in = MapCompose(clean)
    expenditureCode_in = MapCompose(clean)
    description_in = MapCompose(clean)
    amount_in = MapCompose(clean)
    electionCycle_in = MapCompose(clean)
    committeeName_in = MapCompose(clean)

class LateFunding(scrapy.Item):
    committee_name = scrapy.Field()
    contributor_name = scrapy.Field()
    city = scrapy.Field()
    state_zip = scrapy.Field()
    id_number = scrapy.Field()
    employer = scrapy.Field()
    occupation = scrapy.Field()
    amount = scrapy.Field()
    expenditure_type = scrapy.Field()
    trans_date = scrapy.Field()
    filed_date = scrapy.Field()
    trans_no = scrapy.Field()
    election_cycle = scrapy.Field()
    funding_type = scrapy.Field() # LateContributionsMade, LateExpendituresMade, LateExpendituresPlus5000

class LateFundingLoader(ItemLoader):
    default_item_class = LateFunding
    committeeName_in = MapCompose(clean)
    contributorName_in = MapCompose(clean)
    cityName_in = MapCompose(clean)
    stateZip_in = MapCompose(clean)
    id_no_in = MapCompose(clean)
    employer_in = MapCompose(clean)
    occupation_in = MapCompose(clean)
    amount_in = MapCompose(clean)
    expenditureType_in = MapCompose(clean)
    transDate_in = MapCompose(clean)
    filedDate_in = MapCompose(clean)
    trans_no_in = MapCompose(clean)
    electionCycle_in = MapCompose(clean)
    fundingType_in = MapCompose(clean)

class ElectronicFilings(scrapy.Item):
    committee_name = scrapy.Field()
    election_cycle = scrapy.Field()
    filing_period = scrapy.Field()
    filed_on = scrapy.Field()
    filing_no = scrapy.Field()
    filing_type = scrapy.Field()

class ElectronicFilingsLoader(ItemLoader):
    default_item_class = ElectronicFilings
    committeeName_in = MapCompose(clean)
    electionCycle_in = MapCompose(clean)
    filingPeriod_in = MapCompose(clean)
    filedOn_in = MapCompose(clean)
    filing_no_in = MapCompose(clean)
    filingType_in = MapCompose(clean)
