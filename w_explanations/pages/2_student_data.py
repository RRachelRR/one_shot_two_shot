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
	explanations_num = st.session_state.x_num
	
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

def explanation_cols_as_list(explanation_columns):
	explanation_columns = explanation_columns.replace('[\'', '').replace('\']', '').replace(' \'', ' ').replace('\',', ',')
	explanation_columns = explanation_columns.replace('["', '').replace('"]', '').replace(' "', ' ').replace('",', ',')
	explanation_columns = explanation_columns.split(", ")
	return explanation_columns

def explanation_sublists_as_list(explanation_columns):
	explanation_columns_new = []
	explanation_columns = explanation_columns[2:-2]
	explanation_columns = explanation_columns.split("], [")
	for e in explanation_columns:
		e = e.split(", ")
		e = [ee.strip('\'').strip('"') for ee in e]
		e = [ee for ee in e if not ee == ""]
		if not e == []:
			explanation_columns_new.append(e)
	return explanation_columns_new

def highlight(row): 

	highlight_grad = [144, 238, 144]
	highlight_drop = [240, 128, 128]
	default = ''

	row_student = row.name
	row_student_num = int(row_student.split()[-1])-1
	explanation_columns_num = explanation_cols_as_list(df_full.loc[indexes[student_num]]["explanation_num"])
	explanation_columns_cat = explanation_sublists_as_list(df_full.loc[indexes[student_num]]["explanation_cat"])
	explanation_columns_cat = {e[0]:e[2] for e in explanation_columns_cat}
	ai_pred = df_full.loc[indexes[row_student_num]]["AI prediction"].upper()

	highlights = []
	for c in row.index:
		if c in explanation_columns_num:
			if ai_pred == "GRADUATE": #explanations_num[c] == "high" and 
				highlights.append(f'background-color: rgba({highlight_grad[0]},{highlight_grad[1]},{highlight_grad[2]},1)')
			else:
				highlights.append(f'background-color: rgba({highlight_drop[0]},{highlight_drop[1]},{highlight_drop[2]},1)')
		elif c in explanation_columns_cat:
			opacity = explanation_columns_cat[c]
			opacity = float(opacity) - 0.1
			opacity = min(opacity*2,1)
			opacity = str(opacity)
			if ai_pred == "GRADUATE":
				highlights.append(f'background-color: rgba({highlight_grad[0]},{highlight_grad[1]},{highlight_grad[2]},{opacity})')
			else:
				highlights.append(f'background-color: rgba({highlight_drop[0]},{highlight_drop[1]},{highlight_drop[2]},{opacity})')
		else:
			highlights.append(default)

	return highlights

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

#st.dataframe(df.loc[st.session_state.indexes[student_num]], use_container_width=True)
#st.dataframe(df_full.loc[st.session_state.indexes[student_num]], use_container_width=True)
with col3:
	if state_num == 2:

		ai_pred = df_full.at[indexes[student_num],"AI prediction"]
		
		explanation_columns_num = explanation_cols_as_list(df_full.loc[indexes[student_num]]["explanation_num"])
		explanation_columns_cat = explanation_sublists_as_list(df_full.loc[indexes[student_num]]["explanation_cat"])

		if ai_pred.upper() == "DROPOUT":
			st.error("AI prediction\: " + ai_pred.upper())
			h = "red"
		else:
			st.success("AI prediction\: " + ai_pred.upper())
			h = "green"

		explanation = f"Explanation:   \n   The information that contributed the most to this prediction is highlighted in {h} in the table on the left. The highlighted values were important in comparison to similar students in the training dataset. Here, the most important factors were:"
		
		for e in explanation_columns_num:
			d = explanations_num[e]
			if ai_pred.upper() == "DROPOUT":
				if d == "high": d = "low"
				elif d == "low": d = "high"
			explanation += "   \n   - **" + d +"** value in **"+e+"**"

		for e in explanation_columns_cat:
			explanation += "   \n   - **" + e[0] + "** is **" + e[1] + "**"# + e[2]
		
		if ai_pred.upper() == "DROPOUT":
			st.error(explanation)
		else:
			st.success(explanation)

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

with col1:
	student_table = df.T.loc[:, df.T.columns=="Student " + str(student_num +1) ]
	if state_num == 2:
		student_table = student_table.style.apply(highlight, axis=0)
	st.table(student_table)

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