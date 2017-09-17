import os
import sys
import time
import logging
import requests
import warnings

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q


google_location_base_url='https://maps.googleapis.com/maps/api/geocode/json'

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

    while True:
        try:
            for id, location in locationless_dwellings(Search(index=index, using=es)):
                if location:
                    es.update(index=index,
                              doc_type=doc_type,
                              id=id,
                              body={"doc": location})
            logging.info('All done for today. Sleeping for 12h.')
            time.sleep(60*60*12)
        except Exception as exp:
            logging.error('Updating location stopped. {}. Resting a bit.'.format(exp))
            time.sleep(60)

def get_location(doc):
    response = requests.get(
        google_location_base_url,
        {
            'address': '{}, {}'.format(doc.get('formalised_address'), 'Dublin, Ireland')
        }
    )
    if not response.status_code == 200:
        raise Exception('Could not find geolocation for address: {}'.format(
            doc.get('formalised_address')
        ))

    results = response.json()['results']

    if len(results) == 0:
        return None

    location = results[0]['geometry']['location']
    return {
        'location': {
            'lat': location.get('lat'),
            'lon': location.get('lng')
        }
    }


def locationless_dwellings(search):
    for id, doc in dwellings(search):
        yield id, get_location(doc)

def dwellings(search):
    s = search.filter(
        'missing', **{
            'field': 'location'
        }
    ).extra(
        from_=0,
        size=10
    )
    if s.count() > 0:
        for id, doc in [(h.get('_id'), h.get('_source')) for h in s.execute().hits.hits]:
            yield id, doc

if __name__ == '__main__':
    warnings.simplefilter('ignore')
    logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO)
    main()