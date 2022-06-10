# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import streamlit as st
import pandas as pd
import time
import datetime
from st_aggrid import AgGrid, GridUpdateMode, DataReturnMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

import fillTemplate


def main():

    menu = ["Upload", "Edit", "Download", "Upload template"]
    choice = st.sidebar.selectbox("Upload", menu)



    if choice == "Upload":
        st.subheader("Upload a cv")





    elif choice == "Edit":
        create_form()









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
        st.subheader("Upload template")


def create_form():

    with st.form("form1"):

        st.title("Edit information")

        solitan = {}

        addPersonal(solitan)

        addProfRef(solitan)

        addEducation(solitan)

        addLanguages(solitan)

        addProfExper(solitan)

        addSkills(solitan)



        if st.form_submit_button("Download"):
            fillTemplate.argenta((solitan))




def addPersonal(solitan):
    st.subheader("Personal information")
    col1, col2 = st.columns(2)
    with col1:
        # row1
        solitan['lastname'] = st.text_input("Lastname")
        # row2
        solitan['birthdate'] = st.date_input("Birthdate", datetime.date(2000, 1, 1))
        # row3
        gender_choice = ['Male', 'Female']
        solitan['gender'] = st.selectbox("Gender", gender_choice)

    with col2:
        # row1
        solitan['firstname'] = st.text_input("Firstname")
        # row2
        solitan['nationality'] = st.text_input("Nationality")
        # row3
        occupation_choice = ['Fulltime', 'Freelance']
        solitan['work_occupation'] = st.selectbox("Occupation", occupation_choice)

    solitan['fitness'] = st.text_input("Why is the candidate a good fit?")


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
    gd.configure_auto_height(True)
    gridoptions = gd.build()
    grid_response = AgGrid(df, gridOptions=gridoptions, data_return_mode= DataReturnMode.FILTERED_AND_SORTED)
    df = grid_response['data']
    response_array = df.values.tolist()
    solitan['references'] = response_array

def addEducation(solitan):
    st.subheader("Education")
    solitan['educaiton'] = st.text_area("Education")

    st.subheader("Certification")
    solitan['certification'] = st.text_area("Certification")

def addLanguages(solitan):
    lang = {'french':{}, 'dutch':{}, 'englsih':{}}
    st.subheader("Languages")
    scale = ['native', 'fluent', 'good', 'basic']
    fra, dut, eng = st.columns(3)
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

    solitan['languages'] = lang

def addProfExper(solitan):
    st.subheader('Professional Experience')
    dict2 = [
        {
            'company': 'Solita',
            'client': 'Argenta',
            'period': '6/2020-3/2021',
            'role': 'integration architect',
            'task': 'mulesoft development',
            'tools': 'mulesoft',
            'environment': 'software ag',
            'methodology': 'agile'
        },
        {
            'company': 'Solita',
            'client': 'Proximus',
            'period': '3/2021-9/2021',
            'role': 'integration architect',
            'task': 'data engineer',
            'tools': 'postgresql',
            'environment': 'postgresql',
            'methodology': 'agile'
        }
    ]

    df2 = pd.DataFrame.from_dict(dict2)
    # st.dataframe(data=df)

    gd2 = GridOptionsBuilder.from_dataframe(df2)
    gd2.configure_default_column(editable=True)
    gd2.configure_auto_height(True)
    gridoptions2 = gd2.build()
    grid_response = AgGrid(df2, gridOptions=gridoptions2,
                   update_mode=GridUpdateMode.SELECTION_CHANGED)
    df = grid_response['data']
    response_array = df.values.tolist()
    print(response_array)
    print(type(response_array))
    solitan['experience'] = response_array

def addSkills(solitan):
    solitan['man_skills'] = st.text_area('Management Skills')

    solitan['tech_skills'] = st.text_area('Technical Skills')

    solitan['other_skills'] = st.text_area('Others')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
   main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/




