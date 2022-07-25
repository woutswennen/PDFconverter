from docxtpl import DocxTemplate
from docx import Document
from copy import deepcopy
import math

tableindex_ref = 2
rowindex_ref = 10

tableindex_ex = 4
rowindex_ex = 1

experiences_dict = {}
keys = ['Company', 'Client', 'Period', 'Role', 'Tasks', 'Tools', 'Environment', 'Methodology']



def addExTable(input_path, output_path, solitan):
    doc = Document(input_path)

    index = 0
    for project in solitan['projects']:
        arg_dict = {}
        arg_dict['Company'] = 'Solita'
        arg_dict['Client'] = project['client']
        arg_dict['Period'] = project['start_date'] + ' - ' + project['end_date']
        arg_dict['Role'] = project['role']
        arg_dict['Tasks'] = project['tasks']
        arg_dict['Tools'] = project['tools']
        arg_dict['Environment'] = project['environment']
        arg_dict['Methodology'] = project['methodologies']

        experiences_dict[str(index)] = arg_dict

        index = index + 1



    fillExTable(doc, tableindex_ex, rowindex_ex, experiences_dict)
    doc.save(output_path)




def addExRows(table, row):
    row_count = 0
    while (row_count != 8):
        # add row at bottom of table
        table.add_row()
        new_row = table.rows[-1]
        # possition new row just behind given row
        row._tr.addnext(new_row._tr)
        # give right key to new_row
        new_row.cells[0].text = keys[row_count]
        row = new_row
        row_count += 1

    return new_row


def fillExTable(doc, table_index, start_row_index, data):
    table = doc.tables[table_index]
    experience_count = len(data)

    exper_num = 0
    while (exper_num != len(data)):
        experience = data[str(exper_num)]

        arg_index = 0
        while (arg_index != 8):
            row_index_arg = start_row_index + (8 * exper_num) + arg_index
            row = table.row_cells(row_index_arg)
            if (row[0].text not in keys):
                addExRows(table, table.rows[row_index_arg - 1])
                arg_index -= 1
            else:
                row[1].text = experience[row[0].text]

            #             table.rowsx[row_index_arg].text = experience[table.row_cells(row_index_arg)[0].text]
            arg_index += 1

        exper_num = exper_num + 1











