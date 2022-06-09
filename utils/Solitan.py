
class Solitan:
    def __init__(self):
        self.name = ""
        self.rol = ""
        self.info = ""
        self.strengths = ""
        self.workExperience = []
        self.education = []

    def __str__(self):
        return f"""
        Name = {self.name}
        Rol = {self.rol}
        Info = {self.info}
        Strengths = {self.strengths}
        Work workExperience = {self.workExperience}
        Education {self.education}"""


class WorkExperience:
    def __init__(self):
        self.start_date = ""
        self.end_date = ""
        self.job_title = ""
        self.company = ""
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
