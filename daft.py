import re
import os
import sys
import time
import random
import logging
import hashlib
import warnings

from datetime import datetime
from elasticsearch import Elasticsearch
from daftlistings import Daft, RentType


def main():
    host = os.environ.get('ES_HOST')
    index = os.environ.get('INDEX')
    doc_type = os.environ.get('DOC_TYPE')

    if not host:
        sys.exit('Invalid ES_HOST value: {}'.format(host))
    if not index:
        sys.exit('Invalid INDEX value: {}'.format(index))
    if not doc_type:
        sys.exit('Invalid DOC_TYPE value: {}'.format(doc_type))

    es = Elasticsearch([host])
    rent_types = list(RentType)
    while True:
        random.shuffle(rent_types)
        for rent_type in rent_types:
            try:
                for doc, id in documents(rent_type):
                    es.index(index,
                             doc_type,
                             doc,
                             id)
            except Exception as exp:
                logging.error('Unexpected error: {}. Sleeping a while'.format(exp))
                time.sleep(60)
        logging.info('Resting a bit')
        time.sleep(60 * 10)


def to_dict(listing):
    price = listing.get_price()
    price_number = None
    price_month = None

    try:
        price_number = int(re.sub('\D', '', price))
        if 'week' in price.lower():
            price_month = price_number * 4
        else:
            price_month = price_number
    except:
        pass

    return {
        'price': listing.get_price(),
        'price_number': price_number,
        'price_month': price_month,
        'price_change': listing.get_price_change(),
        'viewings': listing.get_upcoming_viewings(),
        'facilities': [l for sl in listing.get_facilities() for l in sl] if listing.get_facilities() else None,
        'features': listing.get_features(),
        'formalised_address': listing.get_formalised_address(),
        'address_line_1': listing.get_address_line_1(),
        'address_line_2': listing.get_address_line_2(),
        'town': listing.get_town(),
        'county': listing.get_county(),
        'listing_image': listing.get_listing_image(),
        'agent': listing.get_agent(),
        'agent_url': listing.get_agent_url(),
        'contact_number': listing.get_contact_number(),
        'daft_link': listing.get_daft_link(),
        'dwelling_type': listing.get_dwelling_type(),
        'posted_since': listing.get_posted_since(),
        'num_bedrooms': listing.get_num_bedrooms(),
        'num_bathrooms': listing.get_num_bathrooms(),
        'area_size': listing.get_area_size(),
        'timestamp': datetime.now()
    }


def documents(rent_type):
    for dwelling in dwellings(rent_type):
        url = dwelling.get('daft_link', '')
        if url:
            yield dwelling, hashlib.sha1(url).hexdigest()


def dwellings(rent_type):
    offset = 0
    daft = Daft()
    daft.set_listing_type(rent_type)
    daft.set_county('Dublin City')
    daft.set_offset(offset)

    listings = True
    while listings:
        listings = daft.get_listings()
        for listing in listings:
            yield to_dict(listing)

        offset += len(listings)
        daft.set_offset(offset)


if __name__ == '__main__':
    warnings.simplefilter('ignore')
    logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO)
    main()
