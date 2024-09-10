import os
# os.environ["STREAMLIT_SERVER_MODE"] = "production"
import streamlit as st
import requests
import json
import time


st.title("LLMDTP")

############ 

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
    password = st.text_input('请输入密码')
    if password == 'chatzocPW!@#':
        st.session_state.password = True
        st.rerun()


if st.session_state.password:


    st.session_state.student_id = st.text_input('请输入学号','')

    ############# 选择模拟患者
    option_choice = st.selectbox(
            "请选择一个标准病人并点击‘确认’",
            ('标准病人1','标准病人2'))

    if option_choice != 'ChatZOC' :

        with st.sidebar:
            
            # if option_choice == 'SP1':
            #     option = 'modified_25_翼状胬肉_1'
            #     photo = "../icons/test_patient_25.jpg"
            #     word = "male，43 years old..."
            if option_choice == '标准病人1':
                option = 'modified_7_急性原发性闭角型青光眼_1'
                photo = "../icons/test_patient_1.gif"
                word = "女，74岁..."
            if option_choice == '标准病人2':
                option = 'modified_8_麦粒肿_1'
                photo = "../icons/test_patient_2.gif"
                word = "女，44岁..."

            st.image(photo,width=256)
            st.write(word)

    ############## 确认选择
    if st.button('确认'):
        st.session_state.time = time.time()
        st.session_state.chat = 'on'
        st.session_state.option = option
        st.session_state.messages = []
        st.session_state.state = []
        st.session_state.state_goal = []
        st.session_state.auto_save = '0min'

        # # 发送POST请求
        # response = requests.post("http://10.100.168.95:8891/api", data="This is a test message")
        # # 打印响应内容
        # print("Response from server:", response.text)
        st.markdown("请等待下面的加载标志停止转动, 然后点击左边栏的 '开始问诊'")
        with st.spinner('加载中...'):
            time.sleep(1)
            if option != 'ChatZOC':
                state_goal = requests.post('http://127.0.0.1:8892/load', headers={'Content-Type': 'application/json'}, json= {"load": [{"model": option+'.json'}]})
                # print(json.loads(state_goal.text))
                st.session_state.state_goal = json.loads(state_goal.text)
                # if option == '病例5-打分test-原1':
                state_fullpoint = json.loads(state_goal.text)
                full_point = 0
                for item in state_fullpoint:
                    # print(item['问题得分'],sum(item['问题得分']))
                    full_point = full_point + sum(item['问题得分'])
                # print(full_point)
                st.session_state.state_all = full_point
            else:
                user_kb = requests.post('http://127.0.0.1:8892/load_zh', headers={'Content-Type': 'application/json'}, json= {"load": [{"model": option+'.json'}]})

        if st.session_state.option == 'ChatZOC':
            st.write('语言模型', st.session_state.option)
        else:
            st.write(option_choice, '--加载完成') 









