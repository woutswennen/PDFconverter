from tika import parser # pip install tika
import json
import spacy
import re

from utils.CVTransformer import CVTransformer
from utils.Solitan import Solitan
import os

# assign directory
directory = 'assets'

# iterate over files in
# that directory
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f) and f.endswith('.pdf'):
        # Clean the PDF's text from empty lines and reconstruct splitted words
        cv = parser.from_file(f)['content']
        cv = re.sub('\n+', '\n', cv)
        cv = re.sub('-\n+', '', cv)
        cv = re.sub("^[a-zA-Z0-9]*$", '', cv)

        # Split the document in the different sections
        solitan = Solitan()
        cvTransformer = CVTransformer(cv, solitan)
        cvTransformer.get_sections()
        cvTransformer.get_personal_info()
        cvTransformer.get_work_experience()
        cvTransformer.get_education()
        cvTransformer.get_projects()

        print(cvTransformer.solitan)
        print(f)

