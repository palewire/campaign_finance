from unittest import TextTestResult
from twisted.trial import unittest
from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.contracts import ContractsManager
from scrapy.contracts.default import (
    UrlContract,
    ReturnsContract,
    ScrapesContract,
)

class TestItem(scrapy.Item):
    spider_name = scrapy.Field()
    url = scrapy.Field()

class ContractsManagerTest(unittest.TestCase):
    contracts = [UrlContract, ReturnsContract, ScrapesContract]
