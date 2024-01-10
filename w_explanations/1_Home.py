############################################################ SETUP ############################################################

############################################################ Imports

import os
import sys
import io
import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.switch_page_button import switch_page

import requests

import math
import pandas as pd
import numpy as np
import json
import random
import re

############################################################ Settings

st.set_page_config(layout="centered", initial_sidebar_state="collapsed")

# hides the first option in a radio group
# note: this applies to ALL radio groups across the app; it cannot be done for an individual button!
st.markdown(
    """ <style>
            div[role="radiogroup"] >  :first-child{
                display: none !important;
            }
        </style>
        """,
    unsafe_allow_html=True
)

no_sidebar_style = """
	<style>
        div[data-testid="stSidebarNav"] {pointer-events: none; cursor: default;}
    </style>
"""
st.markdown(no_sidebar_style, unsafe_allow_html=True)

# hides button to close sidebar, open settings
no_button_style = """
    <style>
        button[kind="header"] {display:none;}
    </style>
"""
st.markdown(no_button_style, unsafe_allow_html=True)

############################################################ Public variables

# paths
project_path = os.path.dirname(__file__) or '.'
data_path = os.path.join(project_path, "sample_x.csv")

st.session_state.project_path = project_path

user_predictions = {}
st.session_state.user_predictions = user_predictions
student_num = 0
st.session_state.student_num = student_num
st.session_state.state_num = 1

# Randomly shuffle data
df = pd.read_csv(data_path, index_col = 0)
df_random = df.sample(frac=1)
# Save data including target
st.session_state.data_full = df
# Adjust version of data for display
df_display = df.loc[:, ~df.columns.isin(['Target', 'AI prediction', 'explanation_num', 'explanation_cat'])]
randomized_indexes = df_random.index.tolist()
st.session_state.indexes = randomized_indexes
for i in range(15):
	df_display.at[randomized_indexes[i],"DisplayIndex"] = "Student " + str(i + 1)
df_display.set_index('DisplayIndex',inplace=True)
st.session_state.data = df_display

explanations_num = {'Age at enrollment': 'low',
 'Curricular units 1st sem enrolled': 'high',
 'Curricular units 1st sem grade': 'high',
 'Curricular units 1st sem passed': 'high',
 'Curricular units 1st sem recognized from previous education or work': 'na',
 'Curricular units 1st sem without exams': 'na',
 'Curricular units 2nd sem enrolled': 'high',
 'Curricular units 2nd sem grade': 'high',
 'Curricular units 2nd sem passed': 'high',
 'Curricular units 2nd sem recognized from previous education or work': 'na',
 'Curricular units 2nd sem without exams': 'na',
 'GDP at enrollment': 'na',
 'Inflation rate at enrollment': 'na',
 'Total exams across all classes in 1st sem': 'low',
 'Total exams across all classes in 2nd sem': 'low',
 'Unemployment rate at enrollment': 'na',
 "University's position in preferences when applying": 'high'}
st.session_state.x_num = explanations_num

############################################################ sort user into group

# group 0 gets to make their decision first, 1 immediately gets shown the AI decision

if not "group" in st.session_state:

	zeroCounter = 0
	while os.path.exists('0_' + str(zeroCounter)+'.csv'):
		zeroCounter = zeroCounter + 1
	oneCounter = 0
	while os.path.exists('1_' + str(oneCounter)+'.csv'):
		oneCounter = oneCounter + 1
	if oneCounter > zeroCounter:
		st.session_state.group = 0	
	else:
		st.session_state.group = 1



############################################################ Public functions




############################################################ MAIN ############################################################

if "reroute_error" in st.session_state and st.session_state.reroute_error:
	st.warning("Sorry! The page was reloaded in your browser, which started a new session. As this site does not save any cookies, it's not possible to remember data between sessions. Please start again.")

############################################################ load data


# show of hide data for debug
if False:

	st.write("This is the data:")
	st.write(df_display)

	st.write("But participants won't actually see this; it's just for us to check. Instead, they only see the lower part:")
	st.write("---")

############################################################ text

st.write("# Academic Career Predictions")

st.markdown(
f"""
This is a research study on the usefulness of Artificial Intelligence (AI) decision aids to predict the outcome of a student's academic career.

Students dropping out before finishing their degree impacts economic growth, employment, competiveness as well as students' lives and families as well as educational institutions. Tutors and advisors can use student data to make predictions about their academic career to offer more accurate help to students.

Your task will be to have a look at twenty randomly selected sets of student data, and predict if the student will graduate or drop out.
Our AI tool trained specifically for this task will make a recommendation to assist you with your decision. Finally, we will ask you to answer a few questions about how useful the AI tool was in making your decisions.""")



st.markdown(
f"""
---
##### About this study:

The entire study should take about 20 minutes. All your answers will be collected anonymously. We do not collect personal information, like your name or IP address. You are free to quit the study at any time.

The data that we collect is stored on a server of the X, in X. After the study finishes, the data from all participants will be analysed together and the results might be published in future research papers. After finishing the experiment, it is not possible to withdraw your data because of the anonymization. 

If you have any questions about this study, please contact:

X or X

If you want to proceed with the study, please click "Start"!

"""
)

next_page = st.button("Start", key = 1)
if next_page:
	id = 0
	while os.path.exists(str(st.session_state.group) + '_' + str(id)+'.csv'):
		id = id + 1
	filename = str(st.session_state.group) + '_' + str(id) + '.csv'
	st.session_state.filename = filename
	with open(filename, 'a+') as f:
		f.write(f"Filename,{filename}\n")
	if st.session_state.group == 0:
		switch_page("student_data")
	else:
		switch_page("data_student")

footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}
</style>
"""
st.write(footer,unsafe_allow_html=True)






