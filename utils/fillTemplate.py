import os,sys
from docxtpl import DocxTemplate
from docx import Document






def argenta(template_path, output_path, solitan):
    doc = DocxTemplate(template_path)
    doc.render(solitan.__dict__)
    doc.save(output_path)


