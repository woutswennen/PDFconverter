

class Solitan:
    def __init__(self):
        self.name = ""
        self.rol = ""
        self.info = ""
        self.strengths = ""
        self.workExperience = []

    def __str__(self):
        return f"""
        Name = {self.name}
        Rol = {self.rol}
        Info = {self.info}
        Strengths = {self.strengths}
        Work workExperience = {self.workExperience}"""


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

