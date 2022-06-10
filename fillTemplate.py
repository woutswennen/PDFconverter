import os,sys
from docxtpl import DocxTemplate
from docx import Document






def argenta(solitan):
    doc = DocxTemplate('cv_template_2.3.docx')
    doc.render(solitan)
    doc.save('filledTemplate.docx')
    filledDoc = Document('cv_template_2.3.docx')



    for ref in solitan['references']:
        pass

    refTable = filledDoc.tables[3]

    for row in refTable.rows:
        for sell in row.cells:
            sell.text = "xd"

    # row = refTable.add_row().cells
    # row2 = refTable.add_row().cells
    # row3 = refTable.add_row().cells
    # row4 = refTable.add_row().cells
    filledDoc.save('renderedTest.docx')