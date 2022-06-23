# This is a sample Python script.
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import os
import random
from _csv import writer
from ast import literal_eval

import streamlit as st
import pandas as pd
import datetime
from st_aggrid import AgGrid, GridUpdateMode, DataReturnMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

from utils.Output import addExTable
import utils.fillTemplate as fill
from utils.CVTransformer import CVTransformer
from utils.Solitan import Solitan
from utils.Output import addExTable


@st.cache(allow_output_mutation=True)
def create_CVTransformer():
    return CVTransformer()


cvTransformer = create_CVTransformer()


def main(cvTransformer=cvTransformer):
    menu = ["Upload", "Edit", "Download", "Upload template"]
    choice = st.sidebar.selectbox("Upload", menu)

    if choice == "Upload":
        st.subheader("Upload the solita cv")
        cv_data = st.file_uploader("Upload Solita CV", type=["pdf"])
        if cv_data is not None:
            st.subheader("Extracting data...")
            cvTransformer.prepare_and_extract(cv_data)
            st.write(cvTransformer.solitan)


    elif choice == "Edit":
        solitan = cvTransformer.solitan
        create_form(solitan)
        st.write(solitan)  # TODO: to delete when complited
        # with st.form(key="form1"):
        #     firstname = st.text_input("Firstname")
        #     submit = st.form_submit_button("Submit")
        #     with st.sidebar:
        #         with st.spinner("loading"):
        #             time.sleep(5)
        #         st.success("Done")


    elif choice == "Download":
        st.subheader("Download the new pdf")


    elif choice == "Upload template":

        st.title("idk")
        uploadedfiles = st.file_uploader("upload file")

        save_uploadedfile(uploadedfiles)

        st.subheader("All templates")
        for file in os.listdir('assets/templates'):
            st.write(file)
            st.button("remove", on_click=removeTemplateFile(file), key=str(random.random()))


def save_uploadedfile(uploadedfile):
    with open(os.path.join("assets/templates", uploadedfile.name), "wb") as f:
        print(uploadedfile.getbuffer())
        f.write(uploadedfile.getbuffer())
        return st.success("Saved File:{} to assets/templates".format(uploadedfile.name))


def removeTemplateFile(filename):
    os.remove('assets/templates/' + filename)


def create_form(solitan):
    with st.form("form1"):
        st.title("Edit information")

        addPersonal(solitan)

        addProfRef(solitan)

        addEducation(solitan)

        addLanguages(solitan)

        addProfExper(solitan)

        addSkills(solitan)

        input_path = 'assets/templates/cv_template.docx'
        inbetween_path = 'assets/templates/semi_filled_template.docx'
        output_path = 'assets/templates/filled_template.docx'

        if st.form_submit_button("Render"):
            addExTable(input_path, inbetween_path, solitan)
            fill.argenta(inbetween_path, output_path, solitan)


    result_doc = open(output_path, 'rb')
    filename = solitan.name + '_' + solitan.lastname + '_cv.docx'
    st.download_button('Download', result_doc, file_name=filename, on_click=final(solitan))
    result_doc.close()


def final(solitan):

    # list of all the project's tools thats going to render in the word doc
    all_tools = []
    for project in solitan.projects:
        for tool in literal_eval(project.tools):
            all_tools.append(tool)

    #tools that where found by the matcher
    found_tools = cvTransformer.last_found_tools


    # add the tools that where added bij the user and are not already in the listing software file
    with open('data/ds_job_listing_software.csv', 'a', newline='') as f_object:
        writer_object = writer(f_object)
        for tool in all_tools:
            if tool not in found_tools:
                list_data = [tool]
                writer_object.writerow(list_data)
        f_object.close()




def addPersonal(solitan):
    st.subheader("Personal information")
    col1, col2 = st.columns(2)
    with col1:
        # row1
        solitan.lastname = st.text_input("Lastname", value=solitan.lastname)
        # row2
        solitan.birthdate = st.date_input("Birthdate", datetime.date(2000, 1, 1))
        # row3
        gender_choice = ['Male', 'Female']
        solitan.gender = st.selectbox("Gender", gender_choice)

    with col2:
        # row1
        solitan.firstname = st.text_input("Firstname", value=solitan.name)
        # row2
        solitan.nationality = st.text_input("Nationality", value=solitan.nationality)
        # row3
        occupation_choice = ['Fulltime', 'Freelance']
        solitan.work_occupation = st.selectbox("Occupation", occupation_choice)

    solitan.fitness = st.text_input("Why is the candidate a good fit?")


def addProfRef(solitan):
    st.subheader("Proffesional References")
    dict = [
        {
            'company': 'Solita',
            'contact_name': 'Jos',
            'profecional_relationship': 'IDK',
            'contact': '+32493706578'
        },
        {
            'company': 'B-post',
            'contact_name': 'Freddie',
            'profecional_relationship': 'IDK2',
            'contact': 'wout.swennen@gmail.com'
        }
    ]

    df = pd.DataFrame.from_dict(dict)
    # st.dataframe(data=df)

    gd = GridOptionsBuilder.from_dataframe(df)
    gd.configure_default_column(editable=True)
    gd.configure_auto_height(False)
    gridoptions = gd.build()
    grid_response = AgGrid(df, gridOptions=gridoptions, data_return_mode=DataReturnMode.FILTERED_AND_SORTED)
    df = grid_response['data']
    response_array = df.values.tolist()
    solitan.references = response_array

    if st.form_submit_button("print grid_response profref"):
        print(df)



def addEducation(solitan):
    st.subheader("Education")
    df2 = pd.DataFrame([[e.title, e.end_date, e.institution, e.education_description] for e in solitan.education],
                       columns=['title', 'end_date', 'institution', 'education_description'])
    # st.dataframe(data=df)

    gd2 = GridOptionsBuilder.from_dataframe(df2)
    gd2.configure_default_column(editable=True)
    gd2.configure_auto_height(False)
    gridoptions2 = gd2.build()
    grid_response = AgGrid(df2, gridOptions=gridoptions2,
                           data_return_mode=DataReturnMode.FILTERED_AND_SORTED)
    df = grid_response['data']
    for index, row in df.iterrows():
        solitan.education[index].title = row['title']
        solitan.education[index].end_date = row['end_date']
        solitan.education[index].institution = row['institution']
        solitan.education[index].education_description = row['education_description']


    st.subheader("Certification")
    df3 = pd.DataFrame(
        [[c.start_date, c.end_date, c.cert_title, c.technology] for c in solitan.certifications],
        columns=['start_date', 'end_date', 'cert_title', 'technology'])
    # st.dataframe(data=df)

    gd3 = GridOptionsBuilder.from_dataframe(df3)
    gd3.configure_default_column(editable=True)
    gd3.configure_auto_height(False)
    gridoptions3 = gd3.build()
    grid_response3 = AgGrid(df3, gridOptions=gridoptions3,
                            data_return_mode=DataReturnMode.FILTERED_AND_SORTED)
    df = grid_response3['data']
    for index, row in df3.iterrows():
        solitan.certifications[index].start_date = row['start_date']
        solitan.certifications[index].end_date = row['end_date']
        solitan.certifications[index].cert_title = row['cert_title']
        solitan.certifications[index].technology = row['technology']


def addLanguages(solitan):
    st.subheader("Languages")
    scale = ['native', 'fluent', 'good', 'basic']
    spoken, written, compre = st.columns(3)
    # TODO: I think this should iterate into the languages of the solitan
    with spoken:
        solitan.french_spoken = st.selectbox('French spoken', scale)
        solitan.dutch_spoken = st.selectbox('Dutch spoken', scale)
        solitan.english_spoken = st.selectbox('English spoken', scale)
    with written:
        solitan.french_written = st.selectbox('French writen', scale)
        solitan.dutch_written = st.selectbox('Dutch writen', scale)
        solitan.english_written = st.selectbox('English writen', scale)
    with compre:
        solitan.french_comprehension = st.selectbox('French comprehension', scale)
        solitan.dutch_comprehension = st.selectbox('Dutch comprehension', scale)
        solitan.english_comprehension = st.selectbox('English comprehension', scale)


def addProfExper(solitan):
    st.subheader('Professional Experience')
    df2 = pd.DataFrame(
        [[w.start_date, w.end_date, w.job_title, w.company, w.job_description] for w in solitan.workExperience],
        columns=['start_date', 'end_date', 'job_title', 'company', 'job_description'])
    # st.dataframe(data=df)

    gd2 = GridOptionsBuilder.from_dataframe(df2)
    gd2.configure_default_column(editable=True)
    gd2.configure_auto_height(False)
    gridoptions2 = gd2.build()
    grid_response = AgGrid(df2, gridOptions=gridoptions2,
                           data_return_mode=DataReturnMode.FILTERED_AND_SORTED)
    df = grid_response['data']
    for index, row in df.iterrows():
        solitan.workExperience[index].start_date = row['start_date']
        solitan.workExperience[index].end_date = row['end_date']
        solitan.workExperience[index].job_title = row['job_title']
        solitan.workExperience[index].company = row['company']
        solitan.workExperience[index].job_description = row['job_description']
        # TODO
        solitan.workExperience[index].client = "client"

    st.subheader('Projects')
    df4 = pd.DataFrame(
        [[p.start_date, p.end_date, p.client, p.role, p.tasks, p.methodologies, p.tools] for p in solitan.projects],
        columns=['start_date', 'end_date', 'client', 'role', 'tasks', 'methodologies', 'tools'])
    # st.dataframe(data=df)

    gd4 = GridOptionsBuilder.from_dataframe(df4)
    gd4.configure_default_column(editable=True)
    gd4.configure_auto_height(False)
    gridoptions4 = gd4.build()
    grid_response4 = AgGrid(df4, gridOptions=gridoptions4, data_return_mode=DataReturnMode.FILTERED_AND_SORTED)

    df4 = grid_response4['data']
    for index, row in df4.iterrows():
        solitan.projects[index].start_date = row['start_date']
        solitan.projects[index].end_date = row['end_date']
        solitan.projects[index].role = row['role']
        solitan.projects[index].client = row['client']
        solitan.projects[index].tasks = row['tasks']
        solitan.projects[index].tools = row['tools']


def addSkills(solitan):
    solitan.man_skills = st.text_area('Management Skills', value=solitan.man_skills)
    st.write('Technical Skills')
    df = pd.DataFrame(
        [[s.skill, s.level, s.year_exp] for s in solitan.tech_skills],
        columns=['skill', 'level', 'years_experience'])
    # st.dataframe(data=df)

    gd = GridOptionsBuilder.from_dataframe(df)
    gd.configure_default_column(editable=True)
    gd.configure_auto_height(False)
    gridoptions = gd.build()
    grid_response = AgGrid(df, gridOptions=gridoptions,
                           data_return_mode=DataReturnMode.FILTERED_AND_SORTED)
    df = grid_response['data']
    for index, row in df.iterrows():
        solitan.tech_skills[index].skill = row['skill']
        solitan.tech_skills[index].level = row['level']
        solitan.tech_skills[index].year_exp = row['years_experience']

    solitan.other_skills = st.text_area('Others', value=solitan.other_skills)


if __name__ == '__main__':
    main()
