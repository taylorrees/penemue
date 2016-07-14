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

NODE_FILE = "nodes_2.csv"
EDGE_FILE = "edges_2.csv"
_DATABASE = "media-monitor"
_HOST = "faraday.local"

db = MongoClient("mongodb://%s:27017" % _HOST)[_DATABASE]
tweets = [t for t in db.tweets.find().limit(100000)]
nodes = set()
edges = set()
wedges = [] # weighted edges

def get_id(name):
    # accepts screen_name and returns
    # index of the node
    for node in nodes:
        if node[1] == name:
            return node[0]

for tweet in tweets:
    mentions = tweet["entities"]["user_mentions"]
    source = tweet["user"]["screen_name"]
    nodes.add(source)

    for mention in mentions:
        target = mention["screen_name"]
        nodes.add(target)

        if (source, target) not in edges:
            # add edge for reference
            edges.add((source, target))
            # create weighted edge
            wedges.append([source, target, 1])

        else:
            # add to weight of edge
            for edge in wedges:
                if edge[0] == source and edge[1] == target:
                    edge[2] = edge[2] + 1
                    break

# create a list of [id, screen_name] pairs
nodes = [(float(n[0]), n[1]) for n in enumerate(nodes)]

for edge in wedges:
        edge[0] = get_id(edge[0])
        edge[1] = get_id(edge[1])

with open(NODE_FILE, 'w') as f:
    w = writer(f)
    w.writerow(["id", "label"])
    w.writerows(nodes)

with open(EDGE_FILE, 'w') as f:
    w = writer(f)
    w.writerow(["source", "target", "weight"])
    w.writerows(wedges)

print("Runtime: %s" % (time() - start))
