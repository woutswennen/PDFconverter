import spacy

from utils.Solitan import Solitan, WorkExperience
from spacy.matcher import Matcher


class CVTransformer:
    def __init__(self, cv):
        self.cv_in_sections = None
        self.cv = cv
        self.solitan = Solitan()
        self.nlp = spacy.load("en_core_web_lg")
        self.nlp.get_pipe("ner").labels

    def get_sections(self):
        sections = ['Personal Info', 'Strengths', 'Work history', 'Education', 'Certificates', 'Projects', 'Skills',
                    'Web presence', 'Languages', 'Hobbies & passions']
        self.cv_in_sections = dict()
        cv_copy = self.cv
        for i in range(0, len(sections) - 1):
            cv_splitted = cv_copy.split(sections[i + 1] + '\n')
            self.cv_in_sections[sections[i]] = cv_splitted[0]
            if len(cv_splitted) > 1:
                cv_copy = cv_splitted[1]

    def get_personal_info(self):
        line_with_name = 0
        cv_in_lines = self.cv.splitlines()
        for i in range(0, len(cv_in_lines)):
            doc = self.nlp(cv_in_lines[i])
            if self.solitan.name != "":
                break
            for ent in doc.ents:
                if ent.label_ == "PERSON" or ent.label_ == "ORG":
                    self.solitan.name = cv_in_lines[i]
                    self.solitan.rol = cv_in_lines[i + 1]
                    break

    def get_work_experience(self):
        matcher = Matcher(self.nlp.vocab)
        pattern = [{"TEXT": {"REGEX": '[0-9]{2}/[0-9]{4}'}}]
        matcher.add('Date', [pattern])

        doc = self.nlp(self.cv_in_sections['Work history'])
        date_matches = matcher(doc)
        for i in range(0, len(date_matches)):
            workExperience = WorkExperience()
            match_id, start, end = date_matches[i]
            string_id = self.nlp.vocab.strings[match_id]  # Get string representation
            span_date = doc[start:end].text.split('—')
            if len(span_date) > 1:
                workExperience.start_date, workExperience.end_date = span_date # The matched span
            else:
                workExperience.start_date = span_date[0]
            if i < len(date_matches) - 1:
                span_jobdescription = doc[end:date_matches[i + 1][1]].text.splitlines()
            else:
                span_jobdescription = doc[end::].text.splitlines()
            workExperience.job_title, workExperience.company = span_jobdescription.pop(0).strip("— .").split(',')

            workExperience.job_description = " ".join(span_jobdescription)
            self.solitan.workExperience.append(workExperience)