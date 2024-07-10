# https://www.pg4e.com/code/elasticmail.py

import requests
import re
import datecompat
import time
import json
import copy
from elasticsearch import Elasticsearch
from elasticsearch import RequestsHttpConnection

# Elasticsearch credentials
es = Elasticsearch(
    ['www.pg4e.com'],
    http_auth=('pg4e_83c4a0efb5', '2410_fb5d92ae'),
    url_prefix='elasticsearch',
    scheme='https',
    port=443,
    connection_class=RequestsHttpConnection,
)

# Index name
indexname = 'pg4e_83c4a0efb5'

# Start fresh
res = es.indices.delete(index=indexname, ignore=[400, 404])
print("Dropped index")
print(res)

res = es.indices.create(index=indexname)
print("Created the index...")
print(res)

baseurl = 'http://mbox.dr-chuck.net/sakai.devel/'

many = 0
count = 0
fail = 0
start = 0
while True:
    if many < 1:
        sval = input('How many messages:')
        if len(sval) < 1:
            break
        many = int(sval)

    start = start + 1
    many = many - 1
    url = baseurl + str(start) + '/' + str(start + 1)

    text = 'None'
    try:
        # Open with a timeout of 30 seconds
        response = requests.get(url)
        text = response.text
        status = response.status_code
        if status != 200:
            print('Error code=', status, url)
            break
    except KeyboardInterrupt:
        print('')
        print('Program interrupted by user...')
        break
    except Exception as e:
        print('Unable to retrieve or parse page', url)
        print('Error', e)
        fail = fail + 1
        if fail > 5:
            break
        continue

    print(url, len(text))
    count = count + 1

    if not text.startswith('From '):
        print(text)
        print('Did not find From ')
        fail = fail + 1
        if fail > 5:
            break
        continue

    pos = text.find('\n\n')
    if pos > 0:
        hdr = text[:pos]
        body = text[pos + 2:]
    else:
        print(text)
        print('Could not find break between headers and body')
        fail = fail + 1
        if fail > 5:
            break
        continue

    # Accept with or without < >
    email = None
    x = re.findall(r'\nFrom: .* <(\S+@\S+)>\n', hdr)
    if len(x) == 1:
        email = x[0]
        email = email.strip().lower()
        email = email.replace('<', '')
    else:
        x = re.findall(r'\nFrom: (\S+@\S+)\n', hdr)
        if len(x) == 1:
            email = x[0]
            email = email.strip().lower()
            email = email.replace('<', '')

    # Hack the date
    sent_at = None
    y = re.findall(r'\nDate: .*, (.*)\n', hdr)
    if len(y) == 1:
        tdate = y[0]
        tdate = tdate[:26]
        try:
            sent_at = datecompat.parsemaildate(tdate)
        except:
            print(text)
            print('Parse fail', tdate)
            fail = fail + 1
            if fail > 5:
                break
            continue

    # Make the headers into a dictionary
    hdrlines = hdr.split('\n')
    hdrdict = dict()
    for line in hdrlines:
        y = re.findall(r'([^ :]*): (.*)$', line)
        if len(y) != 1:
            continue
        tup = y[0]
        if len(tup) != 2:
            continue
        key = tup[0].lower()
        value = tup[1].lower()
        hdrdict[key] = value

    # Override the date field
    hdrdict['date'] = sent_at

    # Reset the fail counter
    fail = 0
    doc = {'offset': start, 'sender': email, 'headers': hdrdict, 'body': body}
    res = es.index(index=indexname, id=str(start), body=doc)
    print('   ', start, email, sent_at)

    print('Added document...')
    print(res['result'])

    if count % 100 == 0:
        time.sleep(1)
