#!/usr/bin/env python3

import urllib.request
import json

import data

URL = 'https://sqwn4h3dc6.execute-api.ap-southeast-2.amazonaws.com/dev/match'

if __name__ == '__main__':
    print("Posting %s matches" % len(data.doubles))
    for game in data.doubles:
        match = {
            'team1': [game[0], game[1]],
            'team2': [game[3], game[4]],
            'score': [game[2], game[5]]
        }
        print("Posting match %s" % match)
        urllib.request.urlopen(URL, data=json.dumps(match).encode())
