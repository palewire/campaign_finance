# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Compose, MapCompose, TakeFirst
from w3lib.html import remove_tags

# Helper functions for preprocessing
def clean(s):
    if isinstance(s, list):
        s = s[0]
    s = s.replace('-','').replace('.','').replace(';','').replace('(','').replace(')','')
    s = ''.join([i if ord(i) < 128 else '' for i in s]).rstrip()
    return s.decode('utf-8').lower()

def to_int(s):
    if isinstance(s, list):
        s = s[0]
    return int(s)

def clean_dict(d):
    clean_dict = {}
    for k,v in d.items():
        new_val = ''.join([i if ord(i) < 128 else '' for i in v]).rstrip() # remove non-ascii characters
        # Using replace throws an error for some reason, use list comprehension instead
        new_val = new_val.decode('utf-8').lower()
        clean_dict[k] = new_val
    return clean_dict

# Ballot Measure Items and Loaders
class Election(scrapy.Item):
    election = scrapy.Field()
    no_measures = scrapy.Field()
    measures = scrapy.Field(serializer=str)

class ElectionLoader(ItemLoader):
    default_item_class = Election
    election_in = MapCompose(clean)
    election_out = TakeFirst()
    no_measures_in = Compose(to_int)
    no_measures_out = TakeFirst()
    measures_in = MapCompose(clean)

class Measure(scrapy.Item):
    measure_name = scrapy.Field(input_processor=Compose(clean),output_processor=TakeFirst())
    measure_id = scrapy.Field(input_processor=Compose(to_int),output_processor=TakeFirst()) # Measure id is in the URL
    supporting_committees = scrapy.Field(input_processor=MapCompose(clean_dict))
    opposing_committees = scrapy.Field(input_processor=MapCompose(clean_dict))

class MeasureLoader(ItemLoader):
    default_item_class = Measure

class Committee(scrapy.Item):
    committee_id = scrapy.Field(input_processor=Compose(to_int),output_processor=TakeFirst())
    committee_name = scrapy.Field(input_processor=Compose(clean),output_processor=TakeFirst())
    election_cycle = scrapy.Field(input_processor=MapCompose(to_int),output_processor=TakeFirst())
    historical_names = scrapy.Field(input_processor=MapCompose(clean),serializer=str)
    status = scrapy.Field(input_processor=Compose(clean),output_processor=TakeFirst())
    reporting_period = scrapy.Field(output_processor=TakeFirst())
    current_contributions = scrapy.Field(output_processor=TakeFirst())
    year_contributions = scrapy.Field(output_processor=TakeFirst())
    current_expenditures = scrapy.Field(output_processor=TakeFirst())
    year_expenditures = scrapy.Field(output_processor=TakeFirst())
    ending_cash = scrapy.Field(output_processor=TakeFirst())

class CommitteeLoader(ItemLoader):
    default_item_class = Committee

class ContributionsReceived(scrapy.Item):
    committee_id = scrapy.Field(input_processor=Compose(to_int),output_processor=TakeFirst())
    committee_name = scrapy.Field(input_processor=Compose(clean),output_processor=TakeFirst())
    contributors = scrapy.Field(input_processor=MapCompose(clean_dict))
    election_year = scrapy.Field(input_processor=Compose(to_int),output_processor=TakeFirst())

class ContributionsReceivedLoader(ItemLoader):
    default_item_class = ContributionsReceived

class ContributionsMade(scrapy.Item):
    committee_id = scrapy.Field(input_processor=Compose(to_int),output_processor=TakeFirst())
    committee_name = scrapy.Field(input_processor=MapCompose(clean),output_processor=TakeFirst())
    contributions = scrapy.Field(input_processor=MapCompose(clean_dict))
    election_year = scrapy.Field(input_processor=Compose(to_int),output_processor=TakeFirst())

class ContributionsMadeLoader(ItemLoader):
    default_item_class = ContributionsMade

class ExpendituresMade(scrapy.Item):
    committee_id = scrapy.Field(input_processor=Compose(to_int),output_processor=TakeFirst())
    committee_name = scrapy.Field(input_processor=MapCompose(clean),output_processor=TakeFirst())
    expenditure = scrapy.Field(input_processor=MapCompose(clean_dict))
    election_year = scrapy.Field(input_processor=Compose(to_int),output_processor=TakeFirst())

class ExpenditureLoader(ItemLoader):
    default_item_class = ExpendituresMade

class LateFunding(scrapy.Item):
    committee_id = scrapy.Field(input_processor=Compose(to_int),output_processor=TakeFirst())
    committee_name = scrapy.Field(input_processor=MapCompose(clean),output_processor=TakeFirst())
    funding_type = scrapy.Field(input_processor=Compose(clean),output_processor=TakeFirst()) # LateContributionsMade, LateExpendituresPlus5000
    contributions = scrapy.Field(input_processor=MapCompose(clean_dict))
    election_year = scrapy.Field(input_processor=Compose(to_int),output_processor=TakeFirst())

class LateFundingLoader(ItemLoader):
    default_item_class = LateFunding

class LateIndependentExpenditures(scrapy.Item):
    committee_name = scrapy.Field(input_processor=MapCompose(clean),output_processor=TakeFirst())
    committee_id = scrapy.Field(input_processor=Compose(to_int),output_processor=TakeFirst())
    lateExpenditures = scrapy.Field(input_processor=MapCompose(clean_dict))
    election_year = scrapy.Field(input_processor=Compose(to_int),output_processor=TakeFirst())

class LateIndependentExpendituresLoader(ItemLoader):
    default_item_class = LateIndependentExpenditures

class Candidates(scrapy.Item):
    candidate_id = scrapy.Field(input_processor=Compose(to_int),output_processor=TakeFirst())
    candidate_name = scrapy.Field(input_processor=Compose(clean),output_processor=TakeFirst())
    party = scrapy.Field(input_processor=Compose(clean),output_processor=TakeFirst())
    spending_limits = scrapy.Field(input_processor=MapCompose(clean_dict))
    races = scrapy.Field(input_processor=MapCompose(clean_dict))
    committees = scrapy.Field(input_processor=MapCompose(clean_dict))

class CandidatesLoader(ItemLoader):
    default_item_class = Candidates
