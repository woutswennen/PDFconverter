# uses https://discuss.streamlit.io/t/heres-a-download-function-that-works-for-dataframes-and-txt/4052
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import base64
import os
import json
import pickle

def download_button(
    object_to_download, download_filename, button_text, pickle_it=False
):
    if pickle_it:
        try:
            object_to_download = pickle.dumps(object_to_download)
        except pickle.PicklingError as e:
            st.write(e)
            return None

    else:
        if isinstance(object_to_download, bytes):
            pass

        elif isinstance(object_to_download, pd.DataFrame):
            object_to_download = object_to_download.to_csv(index=False)

        # Try JSON encode for everything else
        else:
            object_to_download = json.dumps(object_to_download)

    try:
        # some strings <-> bytes conversions necessary here
        b64 = base64.b64encode(object_to_download.encode()).decode()

    except AttributeError as e:
        b64 = base64.b64encode(object_to_download).decode()

    dl_link = f"""
        <html>
        <head>
        <title>Start Auto Download file</title>
        <script src="http://code.jquery.com/jquery-3.2.1.min.js"></script>
        <script>
        $(function() {{
        $('a[data-auto-download]').each(function(){{
        var $this = $(this);
        setTimeout(function() {{
        window.location = $this.attr('href');
        }}, 500);
        }});
        }});
        </script>
        </head>
        <body>
        <div class="wrapper">
        <a data-auto-download href="data:text/csv;base64,{b64}"></a>
        </div>
        </body>
        </html>"""

    return dl_link

def download_df():
    df = pd.DataFrame(st.session_state.col_values, columns=[st.session_state.col_name])
    filename = "my-dataframe.csv"
    components.html(
        download_button(
            df, filename, f"Click here to download {filename}", pickle_it=False
        ),
        height=0,
    )

with st.form("my_form", clear_on_submit=False):
    st.text_input("Column name", help="Name of column", key="col_name")
    st.multiselect(
        "Entries", options=["A", "B", "C"], help="Entries in column", key="col_values"
    )
    submit = st.form_submit_button("Download dataframe", on_click=download_df)