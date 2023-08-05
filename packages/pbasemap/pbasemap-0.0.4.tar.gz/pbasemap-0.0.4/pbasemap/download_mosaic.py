#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json
import re
import csv
import os
import subprocess
import urllib2
import getpass
import sys
from pprint import pprint
from os.path import expanduser
from urllib2 import Request, urlopen
from os.path import expanduser
from retrying import retry
from planet.api.utils import read_planet_json
from planet.api.auth import find_api_key
os.chdir(os.path.dirname(os.path.realpath(__file__)))
planethome = os.path.dirname(os.path.realpath(__file__))
try:
    PL_API_KEY = find_api_key()
    os.environ['PLANET_API_KEY'] = find_api_key()
except:
    print 'Failed to get Planet Key: Initialize First'
    sys.exit()
SESSION = requests.Session()
SESSION.auth = (PL_API_KEY, '')
CAS_URL = 'https://api.planet.com/basemaps/v1/mosaics/'
headers = {'Content-Type': 'application/json'}


def download(filepath=None, coverage=None):
    with open(os.path.join(planethome, 'ids.csv')) as csvfile:
        reader = csv.DictReader(csvfile)
        i=1
        for row in reader:
            url = CAS_URL \
                + str(row['id']) + '/quads?bbox=' + str(row['maxx']) \
                + '%2C' + str(row['maxy']) + '%2C' + str(row['minx']) \
                + '%2C' + str(row['miny'])
            main = SESSION.get(url)
            try:
                if main.status_code == 200:
                    main = main.json()
                    for stuff in main['items']:
                        if coverage is not None \
                            and int(stuff['percent_covered']) \
                            >= int(coverage):
                            downlink = \
                                CAS_URL \
                                + row['id'] + '/quads/' + stuff['id'] \
                                + '/full?api_key=' + str(PL_API_KEY)

                                        # print(downlink)

                            r = requests.get(downlink,
                                    allow_redirects=False, timeout=0.5)
                            mos = r.headers['location'
                                    ].split('planet-mosaics-prod/'
                                    )[1].split('/')[0]
                            fn = r.headers['location'].split('%')[-2]
                            filename = mos + '_' + fn
                            filelink = urllib2.urlopen(downlink)
                            ov = os.path.join(filepath, filename)
                            if not os.path.exists(ov):
                                try:
                                    print 'Downloading: ' + str(filename) \
                                        + ' with coverage ' \
                                        + str(stuff['percent_covered'])
                                    with open(ov, 'wb') as code:
                                        code.write(filelink.read())
                                except Exception, e:
                                    print e
                            else:
                                print 'asset exists..Skipping ' \
                                    + str(filename)
                        elif coverage == None:
                            print 'No coverage information has been provided downloading all'
                            downlink = \
                                CAS_URL \
                                + row['id'] + '/quads/' + stuff['id'] \
                                + '/full?api_key=' + str(PL_API_KEY)

                                        # print(downlink)

                            r = requests.get(downlink,
                                    allow_redirects=False, timeout=0.5)
                            mos = r.headers['location'
                                    ].split('planet-mosaics-prod/'
                                    )[1].split('/')[0]
                            fn = r.headers['location'].split('%')[-2]
                            filename = mos + '_' + fn
                            filelink = urllib2.urlopen(downlink)
                            ov = os.path.join(filepath, filename)
                            if not os.path.exists(ov):
                                try:
                                    print 'Downloading: ' + str(filename)
                                    with open(ov, 'wb') as code:
                                        code.write(filelink.read())
                                except Exception, e:

                                    print e
                            else:
                                print 'asset exists..Skipping ' \
                                    + str(filename)
            except Exception as e:
                print(e)
            except (KeyboardInterrupt, SystemExit) as e:
                print('Program escaped by User')
                sys.exit()
