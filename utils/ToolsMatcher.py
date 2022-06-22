from spacy.matcher import PhraseMatcher
import spacy
import csv
import pandas as pd


class ToolsMatcher:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        # Load vocab into matcher and don't look at capital or not



