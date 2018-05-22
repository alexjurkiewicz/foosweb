import foosweb


def hello(event, context):
    return foosweb.hello(event, context)


def addMatch(event, context):
    return foosweb.addMatch(event, context)


def listPlayers(event, context):
    return foosweb.listPlayers(event, context)
