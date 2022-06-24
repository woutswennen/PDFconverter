class Solitan:
    def __init__(self):
        self.name = ""
        self.lastname = ""
        self.rol = ""
        self.gender = ""
        self.birthday = ""
        self.nationality = ""
        self.work_occupation = ""
        self.fitness = ""
        self.info = ""
        self.strengths = ""
        self.references = ""
        self.availability = ""

        self.certifications = []
        self.workExperience = []
        self.education = []
        self.projects = []
        self.languages = []
        self.other_skills = []
        self.man_skills = []
        self.tech_skills = []

    def __str__(self):
        return f"""
        Name = {self.name}\n
        Lastname = {self.lastname}\n
        Rol = {self.rol}\n
        Info = {self.info}
        Strengths = {self.strengths}\n
        Work workExperience = {self.workExperience}\n
        Education =  {self.education}\n
        Projects = {self.projects}\n
        Certifications = {self.certifications}\n """

    def clear(self):
        self.name = ""
        self.lastname = ""
        self.rol = ""
        self.gender = ""
        self.birthday = ""
        self.nationality = ""
        self.work_occupation = ""
        self.fitness = ""
        self.info = ""
        self.strengths = ""
        self.references = ""
        self.availability = ""

        self.certifications = []
        self.workExperience = []
        self.education = []
        self.projects = []
        self.languages = []
        self.other_skills = []
        self.man_skills = []
        self.tech_skills = []
        print('Solitan to zero')


class WorkExperience:
    def __init__(self):
        self.start_date = ""
        self.end_date = ""
        self.job_title = ""
        self.company = ""
        self.client = ""
        self.job_description = ""

    def __repr__(self):
        return f"""\n
        Job Title = {self.job_title}
        Company = {self.company}
        Start date = {self.start_date}
        End date = {self.end_date}
        Job Description = {self.job_description}\n"""


class Education:
    def __init__(self):
        self.end_date = ""
        self.title = ""
        self.institution = ""
        self.education_description = ""

    def __repr__(self):
        return f"""\n
        Title = {self.title}
        Institution= {self.institution}
        End date = {self.end_date}
        Education Description = {self.education_description}\n"""


class Project:
    def __init__(self):
        self.start_date = ""
        self.end_date = ""
        self.client = ""
        self.role = ""
        self.tasks = ""
        self.tools = []
        self.environment = ""
        self.methodologies = []

    def __repr__(self):
        result = ''
        if self.role is not '':
            result += f'\nRole = {self.role}'
        if self.client is not '':
            result += f'\nClient = {self.client}'
        if self.start_date is not '':
            result += f'\nStart date = {self.start_date}'
        if self.end_date is not '':
            result += f'\nEnd date = {self.end_date}'
        if self.tasks is not '':
            result += f'\nTasks = {self.tasks}'
        if self.methodologies is not '':
            result += f'\nMethodologies = {self.methodologies}'
        if self.tools is not '':
            result += f'\nTools = {self.tools}'
        if self.environment is not '':
            result += f'\nEnvironment = {self.environment}'
        return result


class Certification:
    def __init__(self):
        self.start_date = ""
        self.end_date = ""
        self.cert_title = ""
        self.technology = ""
        self.reference = ""

    def __repr__(self):
        result = '[\n'
        if self.cert_title is not '':
            result += f'\n\tCertification = {self.cert_title}'
        if self.start_date is not '':
            result += f'\n\tStart date = {self.start_date}'
        if self.end_date is not '':
            result += f'\n\tEnd date = {self.end_date}'
        if self.technology is not '':
            result += f'\n\tTechnology = {self.technology}'
        if self.reference is not '':
            result += f'\n\tReference = {self.reference}'
        result += '\n]'
        return result


class Skill:
    def __init__(self):
        skill = ""
        level = ""
        years_exp = ""

    def __repr__(self):
        return f"""\n{self.skill}, {self.level}, {self.year_exp}.\n"""


class Language:
    def __init__(self):
        language = ""
        level = ""

    def __repr__(self):
        return f"""\n{self.language}, {self.level}.\n"""