# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass, field
from typing import Optional
from scrapy.item import Item, Field

#import scrapy


@dataclass
class ScrapebackendItem:
    # define the fields for your item here like:
    name: str = field(default='none')
    city: str = field(default='none')
    address: Optional[str] = field(default='none')
    zipcode: Optional[int] = field(default=-1)
    zc_extension: Optional[int] = field(default=-1)
    five_star: Optional[int] = field(default=0)
    four_star: Optional[int] = field(default=0)
    three_star: Optional[int] = field(default=0)
    two_star: Optional[int] = field(default=0)
    one_star: Optional[int] = field(default=0)
    # pass


@dataclass
class YelpBackendItem:
    name: str = field(default='none')
    city: str = field(default='none')
    address: Optional[str] = field(default='none')
    rating: Optional[float] = field(default='-1')
    rating_count: Optional[int] = field(default='0')
