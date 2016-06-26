import json
import pymongo

def update():
    """
    Remove all current users in the database and
    replace with new users.
    """

    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['MediaMonitor']

    print('Update Users')

    with open('../json/twitter_profiles.json') as infile:
        users = json.load(infile)
        print('\tUsers in file: %s' % len(users))
        if len(users) > 5000:
            print("Max users: 5000")
            print("Limiting to 5000 users")
            users = users[:5000]

    db.users.remove({})

    print('\tRemoving users...')
    print('\tUsers: %s' % db.users.count())
    print('\tInserting users...')

    db.users.insert_many(users)

    print('\tUsers: %s' % db.users.count())

update()
