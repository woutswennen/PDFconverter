from docxtpl import DocxTemplate

from utils.StringTransform import objectArrayToSTring, educationObjectToString, certObjectToString, techSkillObjectToString


def argenta(template_path, output_path, solitan):
    doc = DocxTemplate(template_path)
    #the toDict transformation will transform the dict to match the output format we want in the filled template
    formattedSolitan = toDict(solitan)
    doc.render(formattedSolitan)
    doc.save(output_path)


def toDict(solitan):
    dict = solitan.copy()
    dict['certifications'] = certObjectToString(dict['certifications'])
    dict['tech_skills'] = techSkillObjectToString(dict['tech_skills'])
    dict['education'] = educationObjectToString(dict['education'])
    #TODO addLanguagesToDict(dict)
    return dict

def addLanguagesToDict(dict):
    languages_dict = dict['languages']

    dutch_obj = languages_dict['Dutch']
    dict['dutch_spoken'] = dutch_obj.spoken_level
    dict['dutch_written'] = dutch_obj.written_level
    dict['dutch_comprehension'] = dutch_obj.comprehension_level

    english_obj = languages_dict['English']
    dict['english_spoken'] = english_obj.spoken_level
    dict['english_written'] = english_obj.written_level
    dict['english_comprehension'] = english_obj.comprehension_level


    french_obj = languages_dict['French']
    dict['french_spoken'] = french_obj.spoken_level
    dict['french_written'] = french_obj.written_level
    dict['french_comprehension'] = french_obj.comprehension_level
