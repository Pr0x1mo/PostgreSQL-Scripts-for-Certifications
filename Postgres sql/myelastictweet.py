from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch import RequestsHttpConnection

# Hardcoded credentials
secrets = {
    'host': 'www.pg4e.com',
    'scheme': 'https',
    'prefix': 'elasticsearch',
    'port': 443,
    'user': 'pg4e_83c4a0efb5',
    'pass': '2410_fb5d92ae'
}

es = Elasticsearch(
    [secrets['host']],
    http_auth=(secrets['user'], secrets['pass']),
    url_prefix=secrets['prefix'],
    scheme=secrets['scheme'],
    port=secrets['port'],
    connection_class=RequestsHttpConnection,
)
indexname = secrets['user']

# Start fresh
res = es.indices.delete(index=indexname, ignore=[400, 404])
print("Dropped index")
print(res)

res = es.indices.create(index=indexname)
print("Created the index...")
print(res)

tweets = [
    "and then the compiler puts the resulting machine language into a file",
    "If you have a Windows system often these executable machine language",
    "programs have a suffix of exe or dll which stand for executable",
    "and dynamic link library respectively In Linux and Macintosh there",
    "is no suffix that uniquely marks a file as executable"
]

# Loop through the tweets and index them
for i, tweet in enumerate(tweets):
    doc = {
        'author': 'author_name',  # Replace with actual author if needed
        'type': 'tweet',
        'text': tweet,
        'timestamp': datetime.now(),
    }
    res = es.index(index=indexname, id=f'tweet_{i}', body=doc)
    print(f'Added document {i}...')
    print(res['result'])

# Refresh the index
res = es.indices.refresh(index=indexname)
print("Index refreshed")
print(res)

# Search for a term to verify
x = {
    "query": {
        "bool": {
            "must": {
                "match": {
                    "text": "executable"
                }
            },
            "filter": {
                "match": {
                    "type": "tweet"
                }
            }
        }
    }
}

res = es.search(index=indexname, body=x)
print('Search results...')
print(res)
print()
print("Got %d Hits:" % len(res['hits']['hits']))
for hit in res['hits']['hits']:
    s = hit['_source']
    print(f"{s['timestamp']} {s['author']}: {s['text']}")
