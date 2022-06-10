import re
import spacy

from utils.Solitan import Solitan, WorkExperience, Education, Project
from spacy.matcher import Matcher
from tika import parser


class CVTransformer:
    def __init__(self, cv, solitan):
        self.cv_in_sections = None
        self.cv = cv
        self.solitan = solitan
        self.nlp = spacy.load("en_core_web_lg")
        self.nlp.get_pipe("ner").labels

        self.matcher_dates = Matcher(self.nlp.vocab)
        self.matcher_lower = Matcher(self.nlp.vocab)

        pattern = [{"TEXT": {"REGEX": '[0-9]{4}'}}]
        pattern_lower = [{"TEXT": {"REGEX": '[A-Z]*[a-z]+'}}]

        self.matcher_dates.add('Date', [pattern])
        self.matcher_lower.add('Lower case text', [pattern_lower])

    def prepare_and_extract(self):

        self.cv = parser.from_file(self.cv)['content']
        self.cv = re.sub('\n+', '\n', self.cv)
        self.cv = re.sub('-\n+', '', self.cv)
        self.cv = re.sub("^[a-zA-Z0-9]*$", '', self.cv)

        # Split the document in the different sections
        self.get_sections()
        self.get_personal_info()
        self.get_work_experience()
        print(type(self.solitan.education))
        print(type(self.solitan.workExperience))
        self.get_education()
        self.get_projects()

        return self.solitan

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
        doc = self.nlp(self.cv_in_sections['Work history'])
        date_matches = self.matcher_dates(doc)
        for i in range(0, len(date_matches)):
            workExperience = WorkExperience()
            match_id, start, end = date_matches[i]
            span_date = doc[start:end].text.split('—')
            if len(span_date) > 1:
                workExperience.start_date, workExperience.end_date = span_date  # The matched span
            else:
                workExperience.start_date = span_date[0]
            if i < len(date_matches) - 1:
                span_jobdescription = doc[end:date_matches[i + 1][1]].text.splitlines()
            else:
                span_jobdescription = doc[end::].text.splitlines()
            workExperience.job_title, workExperience.company = span_jobdescription.pop(0).strip("— .").split(',')

            workExperience.job_description = " ".join(span_jobdescription)
            self.solitan.workExperience.append(workExperience)

    def get_education(self):
        doc = self.nlp(self.cv_in_sections['Education'])
        date_matches = self.matcher_dates(doc)
        for i in range(0, len(date_matches)):
            match_id, start, end = date_matches[i]
            education = Education()
            education.end_date = doc[start:end].text  # The matched span
            if i < len(date_matches) - 1:
                span_education_description = re.sub('\n', ' ', doc[end:date_matches[i + 1][1]].text)
            else:
                span_education_description = re.sub('\n', ' ', doc[end::].text)

            education_doc = self.nlp(span_education_description)
            lower_matches = self.matcher_lower(education_doc)
            if len(lower_matches) > 1:
                span_title = education_doc[:lower_matches[0][1]].text
                education.education_description = education_doc[lower_matches[0][1]::].text
            else:
                span_title = span_education_description
            education.title, education.institution = span_title.strip("— .").split(',')
            self.solitan.education.append(education)

    def get_projects(self):
        doc = self.nlp(self.cv_in_sections['Projects'])
        date_matches = self.matcher_dates(doc)
        for i in range(0, len(date_matches)):
            project = Project()
            match_id, start, end = date_matches[i]
            span_date = doc[start:end].text.split('—')
            if len(span_date) > 1:
                project.start_date, project.end_date = span_date  # The matched span
            else:
                project.start_date = span_date[0]

            if i < len(date_matches) - 1:
                span_project_description = doc[end:date_matches[i + 1][1]].text.splitlines()
            else:
                span_project_description = doc[end::].text.splitlines()
            project.project_title, project.client = span_project_description.pop(0).strip(' —.').split(',', 1)
            project.project_description = " ".join(span_project_description)
            self.solitan.projects.append(project)
