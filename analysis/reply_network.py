# Create a twitter mention network
#
# Go through each tweet and determine the author
# of the tweet. Associate the author of the tweet
# with users mentioned in the tweet. Create weighted
# relations based on the number of mentions from
# target to source.

from pymongo import MongoClient
from csv import writer
from time import time

start = time() # to calculate runtime

NODE_FILE = "nodes_3.csv"
EDGE_FILE = "edges_3.csv"
_DATABASE = "media-monitor"
_HOST = "faraday.local"

db = MongoClient("mongodb://%s:27017" % _HOST)[_DATABASE]
tweets = [t for t in db.tweets.find().limit(10000)]
nodes = set()
edges = set()

def get_id(name):
    # accepts screen_name and returns
    # index of the node
    for node in nodes:
        if node[1] == name:
            return node[0]

# collect nodes
for tweet in tweets:
    source = tweet["user"]["id_str"]
    target = tweet["in_reply_to_user_id_str"]

    if target is not None:
        nodes.add((source, source))
        nodes.add((target, target))
        edges.add((source, target))

# write nodes
with open(NODE_FILE, 'w') as f:
    w = writer(f)
    w.writerow(["id", "label"])
    w.writerows(nodes)

# write edges
with open(EDGE_FILE, 'w') as f:
    w = writer(f)
    w.writerow(["source", "target"])
    w.writerows(edges)

print("Runtime: %s" % (time() - start))
