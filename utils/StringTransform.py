



def addItemToString(string, item):
    if string == "":
        string += item
    else:
        string += ', ' + item


def addItemsToString(string, items):
    for item in items:
        addItemToString(string, item)