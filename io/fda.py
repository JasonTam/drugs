__author__ = 'Josh D'

import requests
import json
import os

API_KEY = '3HUprADupJWJCWLW1D7e37Z2Nh6noXrYaTYJ2zMY'
fda_adverse_endpoint = 'https://api.fda.gov/drug/event.json?'
cur_dir = os.path.dirname(__file__)
data_path = os.path.join(cur_dir, '../data/')
json_path = os.path.join(data_path, 'json')


def get_adverse_report(recievedatestart, recievedateend, limit, skip):
    apikey = 'api_key=' + API_KEY
    suffix = '&search=receivedate:[' + recievedatestart + '+TO+' + recievedateend + ']&limit=' + str(
        limit) + '&skip=' + str(skip)
    print fda_adverse_endpoint + apikey + suffix
    r = requests.get(fda_adverse_endpoint + apikey + suffix)
    meta = r.json().get("meta").get("results")

    with open(json_path + recievedatestart + '_' + recievedateend + '_' + str(limit + skip) + '_' + str(
            meta.get("total")) + '.json', 'w') as outfile:
        json.dump(r.json(), outfile)

    return meta.get("total")


def get_adverse_reports(recievedatestart, recievedateend):
    total = get_adverse_report(recievedatestart, recievedateend, 100, 0)
    skip = 100
    while skip < total:
        get_adverse_report(recievedatestart, recievedateend, 100, skip)
        skip += 100


if __name__ == '__main__':
    get_adverse_reports('20140101', '20140108')