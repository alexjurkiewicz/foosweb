import json
import os
import decimal
import time
import itertools

import boto3
import trueskill

MATCH_TABLE_NAME = os.environ["DYNAMODB_MATCH_TABLE"]
PLAYER_TABLE_NAME = os.environ["DYNAMODB_PLAYER_TABLE"]
DYNAMO_KWARGS = {
    # XXX for testing
    # 'region_name': 'localhost',
    # 'endpoint_url': 'http://localhost:8000'
}
CORS_HEADERS = {
    "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Amz-User-Agent",  # noqa: E501
    "Access-Control-Allow-Origin": "*",
}


# Base setup
dynamodb = boto3.resource("dynamodb", **DYNAMO_KWARGS)
_player_table = None
_match_table = None


def get_player_table():
    global _player_table
    if not _player_table:
        _player_table = dynamodb.Table(PLAYER_TABLE_NAME)
    return _player_table


def get_match_table():
    global _match_table
    if not _match_table:
        _match_table = dynamodb.Table(MATCH_TABLE_NAME)
    return _match_table


# This is a workaround for: http://bugs.python.org/issue16535
class DecimalEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)


def hello(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event,
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response


def _get_player_ratings_from_ddb(table, names):
    players = []
    for player in names:
        result = table.get_item(
            table, TableName=PLAYER_TABLE_NAME, Key={"PlayerName": player}
        )

        if "Item" in result:
            players.append(
                trueskill.Rating(
                    float(result["Item"]["mu"]), float(result["Item"]["sigma"])
                )
            )
        else:
            players.append(trueskill.Rating())
    return players


def _save_player_to_ddb(table, player):
    item = {
        "PlayerName": player[0],
        # Yes, Decimal(str(float)) is the best way currently:
        # https://github.com/boto/boto3/issues/665
        "mu": decimal.Decimal(str(player[1].mu)),
        "sigma": decimal.Decimal(str(player[1].sigma)),
    }
    table.put_item(Item=item)


def _save_match_to_ddb(table, match):
    table.put_item(Item=match)


def json_player(p):
    return {
        "name": p[0],
        "mu": decimal.Decimal(str(p[1].mu)),
        "sigma": decimal.Decimal(str(p[1].sigma)),
    }


def addMatch(event, context):
    player_table = get_player_table()
    match_table = get_match_table()

    if "body" not in event:
        raise Exception("No HTTP POST body")
    data = json.loads(event["body"])
    team1_names = data["team1"]
    team2_names = data["team2"]

    old_team1_ratings = _get_player_ratings_from_ddb(player_table, team1_names)
    old_team2_ratings = _get_player_ratings_from_ddb(player_table, team2_names)

    total_score = sum(data["score"])
    win_share = [score / total_score for score in data["score"]]
    ranks = [1 - share for share in win_share]

    new_team1_ratings, new_team2_ratings = trueskill.rate(
        [old_team1_ratings, old_team2_ratings], ranks=ranks
    )

    for player in itertools.chain(
        zip(team1_names, new_team1_ratings), zip(team2_names, new_team2_ratings)
    ):
        _save_player_to_ddb(player_table, player)

    match = {
        "timestamp": decimal.Decimal(str(time.time())),
        "team1_before": [json_player(p) for p in zip(team1_names, old_team1_ratings)],
        "team2_before": [json_player(p) for p in zip(team2_names, old_team2_ratings)],
        "score": data["score"],
        "team1_after": [json_player(p) for p in zip(team1_names, new_team1_ratings)],
        "team2_after": [json_player(p) for p in zip(team2_names, new_team2_ratings)],
    }

    _save_match_to_ddb(match_table, match)

    response = {
        "statusCode": 200,
        "body": json.dumps(match, cls=DecimalEncoder, indent=2, separators=(",", ": ")),
        "headers": CORS_HEADERS,
    }

    return response


def listPlayers(event, context):
    table = get_player_table()

    result = table.scan()

    response = {
        "statusCode": 200,
        "body": json.dumps(
            result["Items"], cls=DecimalEncoder, indent=2, separators=(",", ": ")
        ),
        "headers": CORS_HEADERS,
    }

    return response


def listMatches(event, context):
    table = get_match_table()
    result = table.scan()

    response = {
        "statusCode": 200,
        "body": json.dumps(
            result["Items"], cls=DecimalEncoder, indent=2, separators=(",", ": ")
        ),
        "headers": CORS_HEADERS,
    }

    return response
