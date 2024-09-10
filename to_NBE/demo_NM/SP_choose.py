import os
import streamlit as st
import requests
import json
import time


st.title("LLMDTP")

if 'chat' not in st.session_state:
    st.session_state.chat = 'off'

if 'option' not in st.session_state:
    st.session_state.option = 'none'

if 'state' not in st.session_state:
    st.session_state.state = []

if 'state_goal' not in st.session_state:
    st.session_state.state_goal = []

if 'state_all' not in st.session_state:
    st.session_state.state_all = []

if 'student_id' not in st.session_state:
    st.session_state.student_id = []

if 'student_points' not in st.session_state:
    st.session_state.student_points = 0

if 'student_times' not in st.session_state:
    st.session_state.student_times = 0

if 'auto_save' not in st.session_state:
    st.session_state.auto_save = '0min'


if 'password' not in st.session_state:
    st.session_state.password = False


if st.session_state.password == False:
    password = st.text_input('please enter the password')
    if password == 'chatzocPW!@#':
        st.session_state.password = True
        st.rerun()


if st.session_state.password:


    st.session_state.student_id = st.text_input('Please type your student ID','')

    option_choice = st.selectbox(
            "Please choose a SP and click 'submit'",
            ('SP1','SP2'))

    if option_choice != 'ChatZOC' :

        with st.sidebar:

            if option_choice == 'SP1':
                option = 'modified_7_急性原发性闭角型青光眼_1'
                photo = "../icons/test_patient_1.gif"
                word = "female，74 years old..."
            if option_choice == 'SP2':
                option = 'modified_8_麦粒肿_1'
                photo = "../icons/test_patient_2.gif"
                word = "female，44 years old..."

            st.image(photo,width=256)
            st.write(word)

    if st.button('submit'):
        st.session_state.time = time.time()
        st.session_state.chat = 'on'
        st.session_state.option = option
        st.session_state.messages = []
        st.session_state.state = []
        st.session_state.state_goal = []
        st.session_state.auto_save = '0min'

        st.markdown("Please wait until the spinner below stop and SP dataset loaded, then go to the sidebar and click 'begin asking'")
        with st.spinner('Processing...'):
            time.sleep(1)
            if option != 'ChatZOC':
                state_goal = requests.post('http://127.0.0.1:8891/load', headers={'Content-Type': 'application/json'}, json= {"load": [{"model": option+'.json'}]})
                st.session_state.state_goal = json.loads(state_goal.text)
                state_fullpoint = json.loads(state_goal.text)
                full_point = 0
                for item in state_fullpoint:
                    full_point = full_point + sum(item['问题得分'])
                st.session_state.state_all = full_point
            else:
                user_kb = requests.post('http://127.0.0.1:8891/load_zh', headers={'Content-Type': 'application/json'}, json= {"load": [{"model": option+'.json'}]})

        if st.session_state.option == 'ChatZOC':
            st.write('语言模型', st.session_state.option)
        else:
            st.write(option_choice, '--loaded') 









