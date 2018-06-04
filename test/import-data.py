#!/usr/bin/env python3

import urllib.request
import json
import sys
import time

import elo

api_id=sys.argv[1]

URL = 'https://%s.execute-api.ap-southeast-2.amazonaws.com/dev/match' % api_id

if __name__ == '__main__':
    data = elo.doubles
    total = len(data)
    for i in range(len(data)):
        game = data[i]
        match = {
            'team1': [game[0], game[1]],
            'team2': [game[3], game[4]],
            'score': [game[2], game[5]]
        }
        print("Posting match #%s/%s" % (i, total))
        urllib.request.urlopen(URL, data=json.dumps(match).encode())
        time.sleep(1)
