class Solitan:
    def __init__(self):
        self.name = ""
        self.lastname = ""
        self.rol = ""
        self.gender = ""
        self.birthday = ""
        self.nationality = ""
        self.work_occupation = ""
        self.fitness = "" #TODO: This i'm not sure should be part of the Solitan object
        self.info = ""
        self.strengths = ""
        self.references = ""
        self.certifications = ""

        self.workExperience = []
        self.education = []
        self.projects = []
        self.languages = []
        self.other_skills = []
        self.man_skills = []
        self.tech_skills = []

    def __str__(self):
        return f"""
        Name = {self.name}
        Rol = {self.rol}
        Info = {self.info}
        Strengths = {self.strengths}
        Work workExperience = {self.workExperience}
        Education =  {self.education}
        Projects = {self.projects}"""


class WorkExperience:
    def __init__(self):
        self.start_date = ""
        self.end_date = ""
        self.job_title = ""
        self.company = ""
        self.client = ""
        self.job_description = ""

    def __repr__(self):
        return f"""
        Job Title = {self.job_title}
        Company = {self.company}
        Start date = {self.start_date}
        End date = {self.end_date}
        Job Description = {self.job_description}"""


class Education:
    def __init__(self):
        self.end_date = ""
        self.title = ""
        self.institution = ""
        self.education_description = ""

    def __repr__(self):
        return f"""
        Title = {self.title}
        Institution= {self.institution}
        End date = {self.end_date}
        Education Description = {self.education_description}"""


class Project:
    def __init__(self):
        self.start_date = ""
        self.end_date = ""
        self.client = ""
        self.project_title = ""
        self.project_description = ""

    def __repr__(self):
        return f"""
        Title = {self.project_title}
        Client = {self.client}
        Start date = {self.start_date}
        End date = {self.end_date}
        Project Description = {self.project_description}"""
