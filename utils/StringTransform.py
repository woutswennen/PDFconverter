



def addItemToString(string, item):
    if string == "":
        string += item
    else:
        string += ', ' + item
    return string

def addItemsToString(string, items):
    for item in items:
        string = addItemToString(string, item)
    return string

def objectArrayToSTring(array):
    result = ""
    for object in array:
        result += str(object)
        result += '\n'
    return result