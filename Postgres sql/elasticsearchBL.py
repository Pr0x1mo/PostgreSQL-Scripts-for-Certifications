from elasticsearch import Elasticsearch
from elasticsearch import RequestsHttpConnection
import time
import copy
import uuid
import json
import hashlib
import requests

# Elasticsearch credentials
es_host = "www.pg4e.com"
es_scheme = "https"
es_prefix = "elasticsearch"
es_port = 443
es_user = "pg4e_83c4a0efb5"
es_pass = "2410_fb5d92ae"

# Download the book
url = "https://www.pg4e.com/gutenberg/cache/epub/20203/pg20203.txt"
response = requests.get(url)
book_text = response.text

# Save the book text to a file
bookfile = "pg20203.txt"
with open(bookfile, "w", encoding="utf-8") as f:
    f.write(book_text)

# Make sure we can open the file
fhand = open(bookfile, encoding="utf-8")

# Create Elasticsearch client
es = Elasticsearch(
    [es_host],
    http_auth=(es_user, es_pass),
    url_prefix=es_prefix,
    scheme=es_scheme,
    port=es_port,
    connection_class=RequestsHttpConnection,
)

# Set index name equal to Elasticsearch username
indexname = es_user

# Start fresh
res = es.indices.delete(index=indexname, ignore=[400, 404])
print("Dropped index", indexname)
print(res)

res = es.indices.create(index=indexname)
print("Created the index...")
print(res)

para = ''
chars = 0
count = 0
pcount = 0
for line in fhand:
    count = count + 1
    line = line.strip()
    chars = chars + len(line)
    if line == '' and para == '' : continue
    if line == '' :
        pcount = pcount + 1
        doc = {
            'offset' : pcount,
            'content': para
        }

        # Use the paragraph count as primary key
        # pkey = pcount

        # Use a GUID for the primary key
        # pkey = uuid.uuid4()

        # Compute a SHA256 of the entire document as the primary key.
        # Because the pkey is based on the document contents
        # the "index" is in effect INSERT ON CONFLICT UPDATE unless
        # the document contents change
        m = hashlib.sha256()
        m.update(json.dumps(doc).encode())
        pkey = m.hexdigest()

        res = es.index(index=indexname, id=pkey, body=doc)

        print('Added document', pkey)
        # print(res['result'])

        if pcount % 100 == 0 :
            print(pcount, 'loaded...')
            time.sleep(1)

        para = ''
        continue

    para = para + ' ' + line

# Tell it to recompute the index
res = es.indices.refresh(index=indexname)
print("Index refreshed", indexname)
print(res)

print(' ')
print('Loaded',pcount,'paragraphs',count,'lines',chars,'characters')
