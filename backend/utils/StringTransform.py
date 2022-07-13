



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
        result += educationJson['end_date'] + ' - ' + educationJson['title'] + ' ' + educationJson['institution'] + ': ' + educationJson['education_description'] + '\n'
    return result

def certObjectToString(array):
    result = ""
    for certJson in array:
        result += certJson['end_date'] + ' - ' + certJson['cert_title'] + ' ' + certJson['technology'] + '\n'
        if(certJson['reference'] != ''):
            result += certJson['reference'] + '\n'
    return result

def techSkillObjectToString(array):
    result = ""
    for skillJson in array:
        result += skillJson['skill'] + ', Niveau: ' + skillJson['level'] + ', Experience: ' + skillJson['year_exp'] + '\n'

    return result