



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
    for json in array:
        for key in json:
            result += json[key]
            result += ' '
        result += '\n'

    return result

def educationObjectToString(array):
    result = ""
    for educationJson in array:
        # result += educationJson['title'] + ' ' + educationJson['institution'] + ': ' + educationJson['education_description'] + ' in ' + educationJson['end_date'] + '\n'
        print(educationJson)
    return result