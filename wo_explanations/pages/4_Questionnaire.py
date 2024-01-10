############################################################ SETUP ############################################################

############################################################ Imports

import os
import sys
import io
import streamlit as st
import streamlit.components.v1 as components
from annotated_text import annotated_text
from streamlit_extras.switch_page_button import switch_page

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

st.session_state.time4 = str(time.time())

############################################################ Settings

st.set_page_config(layout="wide",initial_sidebar_state="collapsed")
c_green = "#AD9"
c_red = "#FA9"

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

# stuff that's put in a streamlit container gets a light grey background
st.markdown(
    """ <style>
            div[data-testid="stHorizontalBlock"]{
                background-color: #F0F2F6 !important;
                padding: 10px !important;
                border-radius: 5px !important;
            }
        </style>
        """,
    unsafe_allow_html=True
)

# hides page nav in sidebar
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

# questionnaire - horizontal or vertical likert

likert_horizontal = True
if likert_horizontal:
    label_vis = "collapsed"
else:
    label_vis = "visible"

# randomize trust questions

likert_random_order = True

############################################################ Public variables

switch_label = {"WINNER":"LOSER", "LOSER":"WINNER"}

############################################################ Public functions




############################################################ MAIN ############################################################

try:
    data_path = os.path.join(st.session_state.project_path, "data.csv")
    filename = st.session_state.filename
    group = st.session_state.group
except:
    st.session_state.reroute_error = True
    switch_page("Home")

st.markdown("Please help us evaluate the performance of the AI by answering the following questions.")

with st.form(key='my_form'):

    #    q3b = None
    q2 = st.radio("Are you in any way familiar with AI?", ["", "YES", "NO"])
    #if q4 == "YES":
    q2b = st.text_input('If yes, how have you come in contact with AI?')
    #else:
    #    q4b = None
    q3 = st.number_input('Out of the 15 students, how many do you think you predicted correctly (with the help of the AI)?', value = int(0))
    #q4 = st.radio("What gender do you identify as?", ["", "FEMALE", "MALE", "PREFER TO SELF-IDENTIFY"])

    st.write("Please rate the following statements:")

    likert_questions = {
        "know": "I am knowledgeable enough in the problem domain to solve the task at hand",
        "rel_1": "The system always provides the advice I require to make my decision",
        "rel_2": "The system performs reliably",
        "rel_5": "The system analyzes problems consistently",
        "com_1": "The system uses appropriate methods to reach decisions",
        "com_2": "The system has sound knowledge about this kind of problem built into it",
        "com_3": "The advice the system produces is as good as that which a highly competent person could produce",
        "com_5": "The system makes use of all the knowledge and information available to it to produce its solution to the problem",
        "fai_1": "I believe advice from the system even though I don't know for certain that it is correct",
        "fai_2": "When I am uncertain I believe the system rather than myself",
        "fai_3": "If I am not sure about a decision, I have faith that the system will provide the best solution",
        "fai_4": "When the system gives unusual advice I am confident that the advice is correct",
        "fai_5": "Even if I have no reason to expect the system will be able to solve a difficult problem, I still feel certain that it will",
    }

    likert_results = {}

    likert_question_keys = list(likert_questions.keys())
    #st.write(likert_question_keys)
    if likert_random_order:
        if not "likert_question_keys" in st.session_state:
            random.shuffle(likert_question_keys)
            likert_question_keys.insert(0, likert_question_keys.pop(likert_question_keys.index("know")))
            st.session_state.likert_question_keys = likert_question_keys
        else:
            likert_question_keys = st.session_state.likert_question_keys
    #st.write(likert_question_keys)

    for key in likert_question_keys:
        with st.container():
            col_likert1, col_likert2 = st.columns([5,8], gap = "large")
            with col_likert1:
                st.write(likert_questions[key])
            with col_likert2:
                likert_results[key] = st.radio(likert_questions[key], ["", "STRONGLY AGREE", "AGREE", "NEUTRAL", "DISAGREE", "STRONGLY DISAGREE"], label_visibility = label_vis, horizontal = likert_horizontal, key = key)
            #st.write("---")

    st.markdown("""<style> div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 18px;}</style>""", unsafe_allow_html=True)
    st.markdown("""<style> div[class*="stTextInput"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 18px;}</style>""", unsafe_allow_html=True)
    st.markdown("""<style> div[class*="stnumberInput"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 18px;}</style>""", unsafe_allow_html=True)



    submit_button = st.form_submit_button(label='Submit')

#st.write(q1, likert_results)

if submit_button:
    if any(a == "" for a in likert_results.values()) or any(a == "" for a in [q2, q3]): #, q4]):
        st.error("Please answer all the questions!")
    else:
        with open(filename, 'a+') as f:
            f.write(f"{2},{q2},{q2b}\n")
            f.write(f"{3},{q3}\n")
            #f.write(f"{4},{q4}\n")
            for key in likert_question_keys:
                f.write(f"{key},{likert_results[key]}\n")
        switch_page("Goodbye")

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