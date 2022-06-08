from tika import parser # pip install tika
import json
import spacy
import re

from utils.Solitan import Solitan

pdf_file = r'assets/Vladimir_Anaimanovich_2022-06-02T12_28_56.954Z.pdf'

# Clean the PDF's text from empty lines and reconstruct splited words
cv = parser.from_file(pdf_file)['content']
cv = re.sub('\n+', '\n', cv)
cv = re.sub('-\n+', '', cv)
cv = re.sub("^[a-zA-Z0-9]*$", '', cv)

# Split the document in the different sections
sections = ['Personal Info', 'Strengths', 'Work history', 'Education', 'Certificates', 'Projects', 'Skills', 'Web presence', 'Languages', 'Hobbies & passions']
cv_in_sections = dict()
for i in range(0, len(sections) - 1):
    cv_splitted = cv.split(sections[i + 1] + '\n')
    cv_in_sections[sections[i]] = cv_splitted[0]
    cv = cv_splitted[1]

print(cv_in_sections)