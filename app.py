# This is a sample Python script.
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
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
def create_solitan_profile():
    return Solitan()


solitan = create_solitan_profile()


def main(solitan=solitan):
    menu = ["Upload", "Edit", "Download", "Upload template"]
    choice = st.sidebar.selectbox("Upload", menu)

    if choice == "Upload":
        st.subheader("Upload the solita cv")
        cv_data = st.file_uploader("Upload Solita CV", type=["pdf"])

        if cv_data is not None:
            st.subheader("Extracting data...")
            # solitan = Solitan()
            cvTransformer = CVTransformer(cv_data, solitan)
            cvTransformer.prepare_and_extract()
            st.write(solitan)


    elif choice == "Edit":
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
        st.subheader("Upload template")


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
            input_path = 'assets/template.docx'
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
        [[p.start_date, p.end_date, p.client, p.project_title, p.project_description] for p in solitan.projects],
        columns=['start_date', 'end_date', 'client', 'project_title', 'project_description'])
    # st.dataframe(data=df)

    gd4 = GridOptionsBuilder.from_dataframe(df4)
    gd4.configure_default_column(editable=True)
    gd4.configure_auto_height(False)
    gridoptions4 = gd4.build()
    grid_response4 = AgGrid(df4, gridOptions=gridoptions4, update_mode=GridUpdateMode.SELECTION_CHANGED)

    df = grid_response4['data']
    for index, row in df4.iterrows():
        solitan.projects[index].start_date = row['start_date']
        solitan.projects[index].end_date = row['end_date']
        solitan.projects[index].project_title = row['project_title']
        solitan.projects[index].clinet = row['client']
        solitan.projects[index].project_description = row['project_description']


def addSkills(solitan):
    solitan.man_skills = st.text_area('Management Skills', value=solitan.man_skills)

    solitan.tech_skills = st.text_area('Technical Skills', value=solitan.tech_skills)

    solitan.other_skills = st.text_area('Others', value=solitan.other_skills)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
