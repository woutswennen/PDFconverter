import os, sys
from docxtpl import DocxTemplate
from docx import Document

from utils.StringTransform import objectArrayToSTring


def argenta(template_path, output_path, solitan):
    doc = DocxTemplate(template_path)
    doc.render(toDict(solitan))
    doc.save(output_path)


def toDict(solitan):
    dict = solitan.__dict__.copy()
    dict['education'] = objectArrayToSTring(dict['education'])
    dict['certifications'] = objectArrayToSTring(dict['certifications'])
    dict['tech_skills'] = objectArrayToSTring(dict['tech_skills'])
    return dict