# This is a sample Python script.
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import os
import random

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
from streamlit import caching

@st.cache(allow_output_mutation=True)
def create_solitan_profile():
    return Solitan()


menu = ["Upload", "Edit", "Download", "Upload template"]
choice = st.sidebar.selectbox("Upload", menu)

solitan = create_solitan_profile()

def save_uploadedfile(uploadedfile):
    with open(os.path.join("assets/Templates", uploadedfile.name), "wb") as f:
        print(uploadedfile.getbuffer())
        f.write(uploadedfile.getbuffer())
        return st.success("Saved File:{} to assets/Templates".format(uploadedfile.name))

def removeTemplateFile(filename):
    os.remove('assets/Templates/' + filename)




def create_form(solitan):
    with st.form("form1"):
        st.title("Edit information")

        addPersonal(solitan)

        addProfRef(solitan)

        addEducation(solitan)

        addLanguages(solitan)

        addProfExper(solitan)

        addSkills(solitan)

        if st.form_submit_button("Download"):

            input_path = 'assets/Templates/cv_template.docx'
            inbetween_path = 'assets/semi_filled_template.docx'
            output_path = 'assets/filled_template.docx'

            addExTable(input_path, inbetween_path, solitan)
            fill.argenta(inbetween_path, output_path, solitan)


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
                           update_mode=GridUpdateMode.SELECTION_CHANGED)
    df = grid_response['data']
    for index, row in df2.iterrows():
        solitan.education[index].title = row['title']
        solitan.education[index].end_date = row['end_date']
        solitan.education[index].institution = row['institution']
        solitan.education[index].education_description = row['education_description']

    st.subheader("Certification")
    df3 = pd.DataFrame(
        [[c.start_date, c.end_date, c.cert_title, c.technology] for c in solitan.certifications],
        columns=['start_date', 'end_date', 'cert_title', 'technology'])
    # st.dataframe(data=df)
    print(df3)

    gd3 = GridOptionsBuilder.from_dataframe(df3)
    gd3.configure_default_column(editable=True)
    gd3.configure_auto_height(False)
    gridoptions3 = gd3.build()
    grid_response3 = AgGrid(df3, gridOptions=gridoptions3,
                            update_mode=GridUpdateMode.SELECTION_CHANGED)
    df = grid_response3['data']
    for index, row in df3.iterrows():
        solitan.certifications[index].start_date = row['start_date']
        solitan.certifications[index].end_date = row['end_date']
        solitan.certifications[index].cert_title = row['cert_title']
        solitan.certifications[index].technology = row['technology']


def addLanguages(solitan):
    lang = {'french': {}, 'dutch': {}, 'englsih': {}}
    lang = {'french': {}, 'dutch': {}, 'englsih': {}}
    st.subheader("Languages")
    scale = ['native', 'fluent', 'good', 'basic']
    fra, dut, eng = st.columns(3)
    # TODO: I think this should iterate into the languages of the solitan
    with fra:
        lang['french']['spoken'] = st.selectbox('French spoken', scale)
        lang['french']['spoken'] = st.selectbox('Dutch spoken', scale)
        lang['french']['spoken'] = st.selectbox('English spoken', scale)
    with dut:
        lang['french']['spoken'] = st.selectbox('French writen', scale)
        lang['french']['spoken'] = st.selectbox('Dutch writen', scale)
        lang['french']['spoken'] = st.selectbox('English writen', scale)
    with eng:
        lang['french']['spoken'] = st.selectbox('French comprehension', scale)
        lang['french']['spoken'] = st.selectbox('Dutch comprehension', scale)
        lang['french']['spoken'] = st.selectbox('English comprehension', scale)

    solitan.languages = lang


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
                           update_mode=GridUpdateMode.SELECTION_CHANGED)
    df = grid_response['data']
    for index, row in df2.iterrows():
        solitan.workExperience[index].start_date = row['start_date']
        solitan.workExperience[index].end_date = row['end_date']
        solitan.workExperience[index].job_title = row['job_title']
        solitan.workExperience[index].company = row['company']
        solitan.workExperience[index].job_description = row['job_description']
        # TODO
        solitan.workExperience[index].client = "client"

    st.subheader('Projects')
    df4 = pd.DataFrame(
        [[p.start_date, p.end_date, p.client, p.role, p.tasks] for p in solitan.projects],
        columns=['start_date', 'end_date', 'client', 'role', 'tasks'])
    # st.dataframe(data=df)

    gd4 = GridOptionsBuilder.from_dataframe(df4)
    gd4.configure_default_column(editable=True)
    gd4.configure_auto_height(False)
    gridoptions4 = gd4.build()
    grid_response4 = AgGrid(df4, gridOptions=gridoptions4, update_mode=GridUpdateMode.SELECTION_CHANGED)

    df4 = grid_response4['data']
    for index, row in df4.iterrows():
        solitan.projects[index].start_date = row['start_date']
        solitan.projects[index].end_date = row['end_date']
        solitan.projects[index].role = row['role']
        solitan.projects[index].client = row['client']
        solitan.projects[index].tasks = row['tasks']


def addSkills(solitan):
    solitan.man_skills = st.text_area('Management Skills', value=solitan.man_skills)
    st.write('Technical Skills')
    df = pd.DataFrame(
        [[s.skill, s.level, s.year_exp] for s in solitan.tech_skills],
        columns=['skill','level','years_experience'])
    # st.dataframe(data=df)

    gd = GridOptionsBuilder.from_dataframe(df)
    gd.configure_default_column(editable=True)
    gd.configure_auto_height(False)
    gridoptions = gd.build()
    grid_response = AgGrid(df, gridOptions=gridoptions,
                           update_mode=GridUpdateMode.SELECTION_CHANGED)
    df = grid_response['data']
    for index, row in df.iterrows():
        solitan.tech_skills[index].skill = row['skill']
        solitan.tech_skills[index].level = row['level']
        solitan.tech_skills[index].year_exp = row['years_experience']

    solitan.other_skills = st.text_area('Others', value=solitan.other_skills)


if choice == "Upload":
    st.subheader("Upload the solita cv")
    cv_data = st.file_uploader("Upload Solita CV", type=["pdf"])
    if cv_data is not None:
        st.legacy_caching.clear_cache()
        solitan = create_solitan_profile()
        st.subheader("Extracting data...")
        cvTransformer = CVTransformer(cv_data, solitan)
        solitan = cvTransformer.prepare_and_extract()
        st.write(solitan)

elif choice == "Edit":
    create_form(solitan)

elif choice == "Download":
    st.subheader("Download the new pdf")

elif choice == "Upload template":
    st.title("idk")
    uploadedfiles = st.file_uploader("upload file")

    save_uploadedfile(uploadedfiles)

    st.subheader("All templates")
    for file in os.listdir('assets/Templates'):
        st.write(file)
        st.button("remove", on_click=removeTemplateFile(file), key=str(random.random()))