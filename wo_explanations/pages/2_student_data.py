############################################################ SETUP ############################################################

############################################################ Imports

import os
import sys
import io
import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.switch_page_button import switch_page

import os

import requests

import math
import pandas as pd
import numpy as np
import json
import random
import re
from collections import Counter

import time

## TimeStamp

time_first = str(time.time())

############################################################ Settings

st.set_page_config(layout="wide",initial_sidebar_state="collapsed")

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
        div[data-testid="stSidebarNav"] {display: none;}
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

############################################################ load data

try:
	df = st.session_state.data
	df_full = st.session_state.data_full
	data_path = os.path.join(st.session_state.project_path, "sample.csv")
	group = st.session_state.group
	filename = st.session_state.filename
	state_num = st.session_state.state_num
	student_num = st.session_state.student_num
	indexes = st.session_state.indexes
	
except:
	st.session_state.reroute_error = True
	switch_page("Home")

############################################################ Public variables

show_prediction = True
debug = False

############################################################ Public functions

def first_decision_submit(student_number):
	st.session_state["time_first"] = time_first
	st.session_state["time_second"] = str(time.time())
	st.session_state["state_num"] = 2
	st.session_state["first_choice"] = choice

def final_decision_submit(student_number):
	first_choice = st.session_state["first_choice"]
	second_choice = choice
	correct_choice = df_full.at[indexes[student_num],"Target"].upper()
	if second_choice == correct_choice:
		if not "num_correct" in st.session_state:
			st.session_state["num_correct"] = 1
		else:
			st.session_state["num_correct"] = st.session_state["num_correct"] + 1
	#else:
	#	st.write(correct_choice, choice)
	time1 = st.session_state["time_first"]
	time2 = st.session_state["time_second"]
	time3 = str(time.time())
	with open(filename, 'a+') as f:
		f.write(f"{indexes[student_num]},{first_choice},{second_choice},{time1},{time2},{time3}\n")
	st.session_state["state_num"] = 1
	st.session_state["student_num"] += 1

############################################################ MAIN ############################################################

############################################################ text

st.markdown("### Graduate or Dropout?")

st.markdown(f'''Here you will be shown 20 sets of student information. Your task is to predict for each student whether they will graduate or drop out.
Below, you can see the student’s file with various information about their person and academic career. First, make a decision based on the student's data, without the help of the AI. After entering your decision, you will be shown the prediction of our AI system and will have the option to change your mind. Once you have considered the AI’s suggestion, make your final decision and proceed to the next student.


---''')


############################################################ display student data

# Printing the chosen random order and student data for debugging purposes
if debug:
	st.write(df)
	st.write(st.session_state.indexes)

if st.session_state["student_num"] == len(df.index):
	st.write("Go to next page")
	switch_page("Questionnaire")

#style = df.style.hide_index()
#style.hide_columns()
#style = df.style.format(index='st.session_state.indexes[student_num]', precision=3)
#st.write(style.to_html(), unsafe_allow_html=True)
#st.write(df)
#st.write(indexes)

#df_show = pd.DataFrame(df, index  = indexes)
#st.write(df_show)
#st.write(df_show2.to_html(header=False))
col1, col2, col3= st.columns([4, 1, 5])
#st.table(df.loc[st.session_state.indexes[student_num]])
with col1:
	st.table(df.T.loc[:, df.T.columns=="Student " + str(student_num +1) ])
#st.dataframe(df.loc[st.session_state.indexes[student_num]], use_container_width=True)
#st.dataframe(df_full.loc[st.session_state.indexes[student_num]], use_container_width=True)
with col3:
	if state_num == 2:
		ai_pred = df_full.at[indexes[student_num],"AI prediction"]
		if ai_pred.upper() == "DROPOUT":
			st.error("AI prediction\: " + ai_pred.upper())
		else:
			st.success("AI prediction\: " + ai_pred.upper())
		#st.write("Explanation\: REASONS")
	choice = st.radio("What is your prediction for this student's academic career?", ["", "GRADUATE", "DROPOUT"], key = "decision_choice_"+ str(student_num))

	if state_num == 1:
		st.button("Enter decision and show AI suggestion",disabled = len(choice) == 0,key="first_submit", on_click=first_decision_submit, args = (0,))
	else:
		st.button("Confirm final decision",disabled = len(choice) == 0,key="second_submit", on_click=final_decision_submit, args = (0,))

	st.warning('''
	**Notes about Portuguese University System**  
	    
	| Portuguese Grade| Grade Description                 | US Grade |
	|---------------|---------------------------------------|--------------|
	| 20.00         | Very good with distinction and honors | A+           |
	| 18.00 - 19.99 | Excellent                             | A+           |
	| 16.00 - 17.99 | Very Good                             | A            |
	| 14.00 - 15.99 | Good                                  | B            |
	| 10.00 - 13.99 | Sufficient                            | C            |
	| 1.00 - 9.99   | Poor                                  | F            |
	    
	''')

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