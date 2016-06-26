import nltk
import json
import words
from nltk.tokenize import word_tokenize


def has_keyword(text):
    for word in words.keywords:
        if word in text.lower():
            return True

    return False


filtered = []

with open("../json/twitter_profiles.json") as infile:
    users = json.load(infile)
    infile.close()

for user in users:
    if has_keyword(user["description"]) and (not user["protected"]):
        filtered.append(user)

with open("../json/twitter_profiles.json", "w") as outfile:
    json.dump(filtered, outfile)
    outfile.close()

print("Users: %s" % len(users))
print("Filtered: %s" % len(filtered))
