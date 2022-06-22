from spacy.matcher import PhraseMatcher
import spacy
import csv
import pandas as pd
import streamlit as st

nlp = spacy.load('en_core_web_sm')
#Load vocab into matcher and don't look at capital or not
matcher = PhraseMatcher(nlp.vocab, attr='LOWER')
#need this to see what tools matcher found
last_found_tools = []


def add_small():
    #open small csv and add tools to list
    smallList = []
    with open('../ds_job_listing_software.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            smallList.append(row[0])

    #create patterns of small list
    phrase_patterns_small_list = [nlp(text) for text in smallList]
    #add small list
    matcher.add('data science', None, *phrase_patterns_small_list)

#takes very long
def add_big():
    #read big list
    df = pd.read_excel('Technology Skills.xlsx')
    #create patterns of big list
    phrase_patterns_big_list = [nlp(text) for text in df.Example]


    #add small and big list patterns to the matcher

    matcher.add('software', None, *phrase_patterns_big_list)




def init_matcher():
    add_small()
    add_big()

#load in the matcher for the first time
init_matcher()

def getProjectTools(description):

    project_description = nlp(description)

    #found matches has the places of where there where matches found
    found_matches = matcher(project_description)
    found_tools = []

    #for every match search the word and add it to found tools if not already in there

    for match_id, start, end in found_matches:
        string_id = nlp.vocab.strings[match_id]
        span = project_description[start:end]
        if span.text.upper() not in (tool.upper() for tool in found_tools):
            found_tools.append(span.text)

    last_found_tools = found_tools
    return found_tools

def reload_small():
    matcher.remove('data science')
    add_small()

def reload_big():
    matcher.remove('software')
    add_small()