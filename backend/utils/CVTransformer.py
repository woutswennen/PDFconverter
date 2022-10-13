from operator import contains
import re
import spacy
from spacy.matcher import Matcher, PhraseMatcher
from utils.Solitan import Solitan, WorkExperience, Education, Project, Certification, Skill, Language
from tika import parser
import pandas as pd
import csv

from utils.StringTransform import addItemsToString, addItemToString


class CVTransformer:
    def __init__(self):
        self.cv_in_sections = dict()
        self.cv = None
        self.solitan = Solitan()
        self.nlp = spacy.load("en_core_web_lg")
        self.nlp.get_pipe("ner").labels
        # these will be the all the tools found without the client changing them in the UI
        self.last_found_tools = []

        self.matcher_dates = Matcher(self.nlp.vocab)
        self.matcher_lower = Matcher(self.nlp.vocab)
        self.matcher_duration = Matcher(self.nlp.vocab)
        self.matcher_year = Matcher(self.nlp.vocab)

        pattern1 = [{"TEXT": {"REGEX": '^[0-9]{1,2}/[0-9]{4}—[0-9]{1,2}/[0-9]{4}$'}}]
        pattern2 = [{"TEXT": {"REGEX": '^[0-9]{1,2}/[0-9]{4}'}},
                    {"TEXT": {"REGEX": '—$'}}]
        pattern3 = [{"TEXT": {"REGEX": '^[0-9]{1,2}/[0-9]{4}$'}},
                    {"TEXT": {"REGEX": '—'}},
                    {"LOWER": 'present'}]
        pattern4 = [{"TEXT": {"REGEX": '^[0-9]{4}$'}}]
        pattern5 = [{"TEXT": {"REGEX": '[0-9]*'}},
                    {"LOWER": 'year'}]

        pattern_lower = [{"TEXT": {"REGEX": '[A-Z]*[a-z]+'}}]

        self.matcher_dates.add('Date', [pattern1, pattern2, pattern3])
        self.matcher_year.add('YEAR', [pattern4])
        self.matcher_lower.add('Lower case text', [pattern_lower])
        self.matcher_duration.add('DURATION', [pattern5])

        self.matcher = PhraseMatcher(self.nlp.vocab, attr='LOWER')
        self.add_small()
        # self.add_big() TODO
        print("important to add later")

    def prepare_and_extract(self, cv):
        self.solitan = Solitan()
        self.solitan.clear()
        self.cv = parser.from_file(cv)['content']
        self.cv = re.sub('-\n+|\ue210', '', self.cv)
        self.cv = re.sub("^[a-zA-Z0-9]*$", '', self.cv)
        self.cv = re.sub('\n+', '\n', self.cv)

        # Split the document in the different sections
        self.get_sections()
        self.get_personal_info()
        self.get_work_experience()
        self.get_education()
        self.get_projects()
        self.get_certificates()
        self.get_skills()
        self.get_languages()
        return self.solitan

    def get_sections(self):
        phrase_matcher = PhraseMatcher(self.nlp.vocab)

        sections = [self.nlp(title) for title in
                    ['Personal Info', 'Strengths', 'Work history', 'Education', 'Certificates', 'Projects', 'Skills',
                     'Web presence', 'Languages', 'Hobbies & passions']]

        doc = self.nlp(self.cv)
        print(doc)
        phrase_matcher.add("SECTION", None, *sections)
        matches = phrase_matcher(doc)
        if len(matches) > 0:
            for i in range(0, len(matches) - 1):
                match_id, start, end = matches[i]
                match_id_next, start_next, end_next = matches[i + 1]
                self.cv_in_sections[doc[start:end].text] = doc[end:start_next].text
            self.cv_in_sections[doc[start_next:end_next].text] = doc[end_next::].text

    def get_personal_info(self):
        cv_in_lines = self.cv.splitlines()
        for i in range(0, len(cv_in_lines)):
            doc = self.nlp(cv_in_lines[i])
            if self.solitan.name != "":
                break
            for ent in doc.ents:
                if ent.label_ == "PERSON" or ent.label_ == "ORG":
                    name = cv_in_lines[i].split(' ', 1)
                    if len(name) > 1:
                        self.solitan.name, self.solitan.lastname = name
                        if len(cv_in_lines) > i + 1:
                            self.solitan.rol = cv_in_lines[i + 1]
                    else:
                        self.solitan.name = name[0]
                    break

    def get_work_experience(self):
        try:
            doc = self.nlp(self.cv_in_sections['Work history'])
            matches = self.matcher_dates(doc)
            if len(matches) > 0:
                date_matches = filter_matches_by_longest_string(matches)
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
                    workExperience.role, workExperience.company = span_jobdescription.pop(0).strip("— .").split(
                        ',')

                    workExperience.job_description = " ".join(span_jobdescription)
                    self.solitan.workExperience.append(workExperience)
        except KeyError:
            print('No Work Experience found!')

    def get_education(self):
        try:
            self.solitan.education = list()
            doc = self.nlp(self.cv_in_sections['Education'])
            certifications = []
            matches = self.matcher_year(doc)
            if len(matches) > 0:
                date_matches = filter_matches_by_longest_string(matches)
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
                    certifications.append(education)

            self.solitan.education = certifications
        except KeyError:
            print('No Education found!')

    def get_projects(self):
        try:
            doc = self.nlp(self.cv_in_sections['Projects'])
            matches = self.matcher_dates(doc)
            self.last_found_tools = []
            if len(matches) > 0:
                date_matches = filter_matches_by_longest_string(matches)
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
                    
                    span_project_header = span_project_description.pop(0)
                    if not ',' in span_project_header:
                        span_project_header = span_project_header + ' ' + span_project_description.pop(0)
                    project.role, project.client = span_project_header.strip(' —.').split(',', 1)
                    project.tasks = " ".join(span_project_description)
                    # check methodologies in tasks
                    if 'scrum' in project.tasks.lower():
                        project.methodologies = addItemToString(project.methodologies, 'Scrum')
                    if 'devops' in project.tasks.lower():
                        project.methodologies = addItemToString(project.methodologies, 'DevOps')
                    if 'agile' in project.tasks.lower():
                        project.methodologies = addItemToString(project.methodologies, 'Agile')
                    if 'waterfall' in project.tasks.lower():
                        project.methodologies = addItemToString(project.methodologies, 'Waterfall')

                    project_tools = self.getProjectTools(project.tasks)
                    self.last_found_tools += project_tools
                    # #check tools in tasks
                    project.tools = addItemsToString(project.tools, project_tools)
                    # add new project object to projects list
                    self.solitan.projects.append(project)
        except KeyError:
            print('No Projects found!')

    def get_certificates(self):
        try:
            doc = self.nlp(self.cv_in_sections['Certificates'])
            matches = self.matcher_dates(doc)
            if len(matches) > 0:
                date_matches = filter_matches_by_longest_string(matches)
                for i in range(0, len(date_matches)):
                    certification = Certification()
                    match_id, start, end = date_matches[i]
                    span_date = doc[start:end].text.split('—')
                    if len(span_date) > 1:
                        certification.start_date, certification.end_date = span_date  # The matched span
                    else:
                        certification.start_date = span_date[0]
                    if i < len(date_matches) - 1:
                        span_description = doc[end:date_matches[i + 1][1]].text
                    else:
                        span_description = doc[end::].text
                        
                    span_cert_title, certification.reference = span_description.split('\n', 1)
                    
                    if ',' in span_cert_title:
                        certification.cert_title, certification.technology = span_cert_title.split(',')[:2]
                    else:
                        certification.cert_title = span_cert_title
                        
                    self.solitan.certifications.append(certification)
        except KeyError:
            print('No Certifications found!')

    def get_skills(self):
        try:
            doc = self.nlp(self.cv_in_sections['Skills'])

            matches = self.matcher_duration(self.nlp(" ".join([token.lemma_ for token in doc])))

            for i in range(0, len(matches)):
                match_id, start, end = matches[i]
                if i > 1:
                    span_date = doc[start: end].text
                    span_tech = doc[matches[i - 1][2] + 1:start - 1]
                    span_level = doc[start - 1]
                else:
                    span_date = doc[start: end].text
                    span_tech = doc[0:start - 1]
                    span_level = doc[start - 1]

                skill = Skill()
                skill.skill = str(span_tech)
                skill.level = str(span_level)
                skill.year_exp = str(span_date)
                self.solitan.tech_skills.append(skill)
        except KeyError:
            print('No Skills found!')
        try:
            man_skills_array = self.cv_in_sections['Strengths'].splitlines()
            man_skills_array = [skill for skill in man_skills_array if skill != '']
            self.solitan.man_skills = addItemsToString(self.solitan.man_skills, man_skills_array)
        except KeyError:
            print('No Strengths found!')


    def get_languages(self):
        try:
            doc = self.nlp(self.cv_in_sections['Languages'].strip('\n'))
            for line in doc.text.splitlines():
                try:
                    span_language, span_level = line.split(' ', 1)
                    language = Language(span_level)
                    self.solitan.languages[span_language] = language.__dict__
                except ValueError:
                    print('No Languages more found!')
        except KeyError:
            print('No Languages found!')

    def getProjectTools(self, description):
        project_description = self.nlp(description)

        # found matches has the places of where there where matches found
        found_matches = self.matcher(project_description)
        found_tools = []

        # for every match search the word and add it to found tools if not already in there

        for match_id, start, end in found_matches:
            string_id = self.nlp.vocab.strings[match_id]
            span = project_description[start:end]
            if span.text.upper() not in (tool.upper() for tool in found_tools):
                found_tools.append(span.text)

        return found_tools

    def reload_small(self):
        self.matcher.remove('data science')
        self.add_small()

    def reload_big(self):
        self.matcher.remove('software')
        self.add_small()

    def add_small(self):
        # open small csv and add tools to list
        smallList = []
        with open('./data/ds_job_listing_software.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                smallList.append(row[0])

        # create patterns of small list
        phrase_patterns_small_list = [self.nlp(text) for text in smallList]
        # add small list
        self.matcher.add('data science', None, *phrase_patterns_small_list)

    # takes very long
    def add_big(self):
        # read big list
        df = pd.read_excel('./data/Technology Skills.xlsx')
        # create patterns of big list
        phrase_patterns_big_list = [self.nlp(text) for text in df.Example]

        # add small and big list patterns to the matcher

        self.matcher.add('software', None, *phrase_patterns_big_list)


def filter_matches_by_longest_string(matches):
    filtered_matches = []
    for i in range(0, len(matches) - 1):
        match_id, start, end = matches[i]
        if not start >= matches[i + 1][1] and end <= matches[i + 1][2]:
            filtered_matches.append(matches[i])
    filtered_matches.append(matches[-1])
    return filtered_matches
