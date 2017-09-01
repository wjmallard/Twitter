#!/usr/bin/env python3

from twython import Twython
import json
import time

TIMESTAMP = time.strftime('%Y-%m-%d - %H:%M %Z')
FILENAME = 'Followers - ' + TIMESTAMP + '.log'

with open('auth.json') as fd:
    auth = json.load(fd)

twitter = Twython(auth['API_Key'],
                  auth['API_Secret'],
                  auth['Access_Token'],
                  auth['Access_Token_Secret'])
user_id = auth['username']

with open('followers.json') as fd:
    old_followers = json.load(fd)

cur_followers = []

cursor = -1
while cursor:
    followers = twitter.get_followers_ids(user_id=user_id, cursor=cursor)
    cursor = followers['next_cursor']
    cur_followers += followers['ids']

with open('followers.json', 'w') as fd:
    json.dump(cur_followers, fd)

lost_followers = list(set(old_followers) - set(cur_followers))
gained_followers = list(set(cur_followers) - set(old_followers))

if old_followers != cur_followers:

    if lost_followers:
        lost_follower_info = twitter.lookup_user(user_id=lost_followers)
        lost_follower_names = [user['screen_name'] for user in lost_follower_info]
    else:
        lost_follower_names = ['[none]']

    if gained_followers:
        gained_follower_info = twitter.lookup_user(user_id=gained_followers)
        gained_follower_names = [user['screen_name'] for user in gained_follower_info]
    else:
        gained_follower_names = ['[none]']
    
    last_tweet = twitter.get_user_timeline(user_id=user_id, count=1)[0]['text']

    with open(FILENAME, 'w') as fd:
        print(TIMESTAMP, file=fd)
        print('Lost:', '.'.join(lost_follower_names), file=fd)
        print('Gained:', '.'.join(gained_follower_names), file=fd)
        print('Last tweet:', last_tweet, file=fd)
