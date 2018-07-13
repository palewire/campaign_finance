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
    election_year = scrapy.Field() # get from URL

class ContributionsReceivedLoader(ItemLoader):
    default_item_class = ContributionsReceived
    committeeId_in = Compose(to_int)
    committeeName_in = MapCompose(clean)
    contributor_in = MapCompose() # TODO: Clean up dicts
    electionYear_in = MapCompose(clean)

class ContributionsMade(scrapy.Item):
    committee_id = scrapy.Field()
    committee_name = scrapy.Field()
    contributions = scrapy.Field()
    election_year = scrapy.Field()

class ContributionsMadeLoader(ItemLoader):
    default_item_class = ContributionsMade
    committeeId_in = Compose(to_int)
    committeeName_in = MapCompose(clean)
    contributions = MapCompose() # TODO: Clean values in dicts
    electionYear_in = MapCompose(clean)

class ExpendituresMade(scrapy.Item):
    election_year = scrapy.Field()
    committee_id = scrapy.Field()
    committee_name = scrapy.Field()
    expenditure = scrapy.Field()

class ExpenditureLoader(ItemLoader):
    default_item_class = ExpendituresMade
    electionYear_in = Compose(to_int)
    committeeId_in = Compose(to_int)
    committeeName_in = MapCompose(clean)
    expenditure_in = MapCompose(clean)

class LateFunding(scrapy.Item):
    committee_name = scrapy.Field()
    committee_id = scrapy.Field()
    election_year = scrapy.Field()
    funding_type = scrapy.Field() # LateContributionsMade, LateExpendituresPlus5000
    contributions = scrapy.Field()

class LateFundingLoader(ItemLoader):
    default_item_class = LateFunding
    committeeName_in = MapCompose(clean)
    committeeId_in = Compose(to_int)
    electionYear_in = MapCompose(clean)
    fundingType_in = MapCompose(clean)
    contributions_in = MapCompose() # TODO: Clean up values in the dictionaries

class LateIndependentExpenditures(scrapy.Item):
    committee_name = scrapy.Field()
    committee_id = scrapy.Field()
    election_year = scrapy.Field()
    lateExpenditures = scrapy.Field()

class LateIndependentExpendituresLoader(ItemLoader):
    default_item_class = LateIndependentExpenditures
    committeeName_in = Compose(clean)
    committeeId_in = Compose(to_int)
    electionYear_in = Compose(to_int)
    lateExpenditures_in = MapCompose(clean) # TODO: Clean up amount
