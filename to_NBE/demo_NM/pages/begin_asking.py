import os
import streamlit as st
import random
import time
import streamlit as st
import re
import json
import requests
from gtts import gTTS
from io import BytesIO
import base64
from pydub import AudioSegment
import pickle
import sys
from pygtrans import Translate


def generate_response(prompt,prev_q,prev_flag):
    if st.session_state.option == 'ChatZOC':
        url = 'http://127.0.0.1:8891/chat_zh'
    else:
        url = 'http://127.0.0.1:8891/chat'
    response_with_state = requests.post(url, headers={'Content-Type': 'application/json'}, json= {"messages": [{"role": "user", "content": prompt, "prev_q": prev_q, "prev_flag": prev_flag, 'student_id': st.session_state.student_id}]})
    return response_with_state

def show_case(option,step1,step2,step3,step4,step5,step6,step7):

        with st.sidebar:   

            tik_wide = 25
            col1, col2, col3, col4 = st.columns([1, 4, 1, 4])

            with col1:
                if step1:
                    st.image('../icons/clear.jpg',width=tik_wide) 
                else:
                    st.image('../icons/unclear.jpg',width=tik_wide)

                if step2:
                    st.image('../icons/clear.jpg',width=tik_wide) 
                else:
                    st.image('../icons/unclear.jpg',width=tik_wide)

                if step3:
                    st.image('../icons/clear.jpg',width=tik_wide) 
                else:
                    st.image('../icons/unclear.jpg',width=tik_wide)

                if step4:
                    st.image('../icons/clear.jpg',width=tik_wide) 
                else:
                    st.image('../icons/unclear.jpg',width=tik_wide)

            with col3:
                if step5:
                    st.image('../icons/clear.jpg',width=tik_wide) 
                else:
                    st.image('../icons/unclear.jpg',width=tik_wide)

                if step6:
                    st.image('../icons/clear.jpg',width=tik_wide) 
                else:
                    st.image('../icons/unclear.jpg',width=tik_wide)

                if step7:
                    st.image('../icons/clear.jpg',width=tik_wide) 
                else:
                    st.image('../icons/unclear.jpg',width=tik_wide)

            with col2:
                st.write('Basic info')
                st.write('Current hist')
                st.write('Past hist')
                st.write('Personal hist')
            with col4:
                st.write('Family hist')
                st.write('Marital hist')
                st.write('Allergy hist')

def save_point(state_goal, pointss,timess, option, student_id='0', file_path="student_goal.txt"):        
    if st.session_state.chat == 'off':

        state_out = {"student_id":student_id,"test_option":option,"student_points":pointss,"exam_time":timess}

        original_stdout = sys.stdout

        with open(file_path, "a") as file:
            sys.stdout = file  

        sys.stdout = original_stdout

def save_point_5min(state_goal, points,full_point,timess, option, student_id='0', file_path="student_goal.txt"):        
    if timess >= int(300) and st.session_state.auto_save == '0min':
 
        st.session_state.auto_save = '5min'

        state_out = {"student_id":student_id,"test_option":option,"student_points":round(points/full_point*100,2),"exam_time":timess}

        original_stdout = sys.stdout

        with open(file_path, "a") as file:
            sys.stdout = file  
            print('5min auto save')
            print(state_out)
            print(state_goal)

        sys.stdout = original_stdout

def save_point_10min(state_goal, points,full_point,timess, option, student_id='0', file_path="student_goal.txt"):  
    if timess >= int(600) and st.session_state.auto_save == '5min':
        print('time pass:',timess,type(timess))  
        st.session_state.auto_save = '10min'

        state_out = {"student_id":student_id,"test_option":option,"student_points":round(points/full_point*100,2),"exam_time":timess}

        original_stdout = sys.stdout

        with open(file_path, "a") as file:
            sys.stdout = file 

        sys.stdout = original_stdout

def save_point_15min(state_goal, points,full_point,timess, option, student_id='0', file_path="student_goal.txt"):        
        
    if timess >= int(900) and st.session_state.auto_save == '10min':
        print('time pass:',timess,type(timess))  
        st.session_state.auto_save = '15min'

        state_out = {"student_id":student_id,"test_option":option,"student_points":round(points/full_point*100,2),"exam_time":timess}

        original_stdout = sys.stdout

        with open(file_path, "a") as file:
            sys.stdout = file  


        sys.stdout = original_stdout


def show_point(points,full_point):
    with st.sidebar:  

        if st.button('End the inquiry and check the score'):       
            st.session_state.chat = 'off'
            
    if st.session_state.chat == 'off':
        st.write('The Q&A session is over')
        st.write('Your score is:',round(points/full_point*100,2))
        time2 = time.time()
        exam_time = time2 - st.session_state.time
        st.write('The time you spent:',round(exam_time),'s')
        st.session_state.point = 0
        st.session_state.state_all = 0
        st.write('Please return to the SP choose interface and select again')

        st.session_state.student_points = round(points/full_point*100,2)
        st.session_state.student_times = round(exam_time)
        





# 左侧边栏实时状态显示
def steps_retrieval(state,state_goal):

    step1 = False
    step2 = False
    step3 = False
    step4 = False
    step5 = False
    step6 = False
    step7 = False

    for i in range(len(state)):
        if state[i] != {}:

            for item in state_goal:
                if item['病历分类'] == state[i]['病历分类']:
                    if state[i]['问题的序号'] in item['问题的序号']:
                        item['问题的序号'].remove(state[i]['问题的序号'])

                if not item['问题的序号']:
 
                    if item['病历分类'] == '基本信息':
                        step1 = True
                    elif item['病历分类'] == '现病史':
                        step2 = True
                    elif item['病历分类'] == '既往史':
                        step3 = True
                    elif item['病历分类'] == '个人史':
                        step4 = True
                    elif item['病历分类'] == '家族史':
                        step5 = True
                    elif item['病历分类'] == '婚育史':
                        step6 = True
                    elif item['病历分类'] == '过敏史':
                        step7 = True


    return step1,step2,step3,step4,step5,step6,step7


def steps_and_point_retrieval(points,state,state_goal):

    step1 = False
    step2 = False
    step3 = False
    step4 = False
    step5 = False
    step6 = False
    step7 = False

    for i in range(len(state)):
        if state[i] != {}:

            for item in state_goal:
                if item['病历分类'] == state[i]['病历分类']:
                    if state[i]['问题的序号'] in item['问题的序号']:
                        item['问题的序号'].remove(state[i]['问题的序号'])
                        item['问题得分'].remove(state[i]['问题得分'])
                        points = points + state[i]['问题得分']

                if not item['问题的序号']:
  
                    if item['病历分类'] == '基本信息':
                        step1 = True
                    elif item['病历分类'] == '现病史':
                        step2 = True
                    elif item['病历分类'] == '既往史':
                        step3 = True
                    elif item['病历分类'] == '个人史':
                        step4 = True
                    elif item['病历分类'] == '家族史':
                        step5 = True
                    elif item['病历分类'] == '婚育史':
                        step6 = True
                    elif item['病历分类'] == '过敏史':
                        step7 = True


    return points,step1,step2,step3,step4,step5,step6,step7


def info_extract_from_excel(type_name,item,df):
    if item == []:
        print('empty')
        response_detail = f"[{type_name}]部分无缺漏"
    
    else:
        result = ''
        print(item,type(item))
        for i in item:
            print(i)
            for index,row in df.iterrows():
                if row['问题的序号'] == i:

                    big_type = row['大类别']

                    if row['小类别'] == '/' or row['小类别'] is None:
                        print('set null')
                        small_type = ''
                    else:
                        small_type = '-' + row['小类别']

                    print(row['症状细节'])
                    if row['症状细节'] == '/' or row['症状细节'] is None:
                        print('set null')
                        snyp_detail = ''
                    else:
                        snyp_detail = '-' + row['症状细节']

                    result = result + '  \n' + big_type + small_type + snyp_detail + ',问题的例子是：' + row['医生问诊问题']
                    break
        response_detail = f"[{type_name}]部分的缺漏为：  {result}"
    return response_detail


def detail_retrieval(state_goal,option):

    if st.session_state.chat == 'off':
        import pandas as pd
        df = pd.read_excel('../knowledge_excel/'+option+'.xlsx')

        for index,item in enumerate(state_goal):

            if index == (len(state_goal)-1):
                break
            elif item['病历分类'] == '基本信息':
                response_detail = info_extract_from_excel('基本信息',item['问题的序号'],df)
                st.markdown(response_detail) 
            elif item['病历分类'] == '现病史':
                response_detail = info_extract_from_excel('现病史',item['问题的序号'],df)
                st.markdown(response_detail)  
            elif item['病历分类'] == '既往史':
                response_detail = info_extract_from_excel('既往史',item['问题的序号'],df)
                st.markdown(response_detail)  
            elif item['病历分类'] == '个人史':
                response_detail = info_extract_from_excel('个人史',item['问题的序号'],df)
                st.markdown(response_detail)   
            elif item['病历分类'] == '家族史':
                response_detail = info_extract_from_excel('家族史',item['问题的序号'],df)
                st.markdown(response_detail)   
            elif item['病历分类'] == '婚育史':
                response_detail = info_extract_from_excel('婚育史',item['问题的序号'],df)
                st.markdown(response_detail)  
            elif item['病历分类'] == '过敏史':
                response_detail = info_extract_from_excel('过敏史',item['问题的序号'],df)
                st.markdown(response_detail)   


def autoplay_audio(file_path: str):
    print('autoplay')
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )

def find_and_read_mp3(folder_path, file_name):

    files = os.listdir(folder_path)


    for file in files:
        if file.endswith(".mp3") and file == file_name:

            file_path = os.path.join(folder_path, file)

            return file_path

    print(f"未找到文件名为 {file_name} 的MP3文件。")
    return None

client = Translate()

responses_no = [
  "没有啊",
  "这个没有",
  "这没有",
  "没有的",
  "没有",
  "没啊",
  "没",
  "没有",
  "没有的",
  "无",
]
def get_random_response_no():
  return random.choice(responses_no)



if st.session_state.option == 'ChatZOC':
    st.title("ChatZOC")
else:
    st.title("ChatZOC SPs")

sound = BytesIO()

if 'chat' not in st.session_state:
    st.session_state.chat = 'off'

if 'state' not in st.session_state:
    st.session_state.state = []

if 'point' not in st.session_state:
    st.session_state.point = 0

if 'flag' not in st.session_state:
    st.session_state.flag = 2

if 'prompt' not in st.session_state:
    st.session_state.prompt = None

if st.session_state.chat == 'on':


    if st.session_state.option != 'ChatZOC' :

        if st.session_state.option == 'modified_7_急性原发性闭角型青光眼_1':
            photo = "../icons/test_patient_1.gif"
            word = "female，74 yesrs old..."
        if st.session_state.option == 'modified_8_麦粒肿_1':
            photo = "../icons/test_patient_2.gif"
            word = "患者女，44岁..."

        st.image(photo,width=496)
        
    if "messages" not in st.session_state:
        st.session_state.messages = []

    prev_q = ''
    prev_flag = st.session_state.flag

    for message in st.session_state.messages:

        prev_q = message["content"]


    if st.session_state.prompt:
        prompt = client.translate(st.session_state.prompt, target="zh").translatedText
        st.session_state.messages.append({"role": "user", "content": prompt})

        asking = prompt

        response_with_state = generate_response(asking,prev_q,prev_flag)
        if st.session_state.option != 'ChatZOC' :

            output = json.loads(response_with_state.text)['response']

            output = client.translate(output, target="en").translatedText
            output = output.replace("&#39;","'")
            prev_flag = json.loads(response_with_state.text)['flag']

            st.session_state.state.append(json.loads(response_with_state.text)['state'])
        else:
            output = response_with_state.text


        message_placeholder = st.empty()

        if output == '没有':
            output = get_random_response_no()


        if len(output) > 50:
            output_audio = output[:50]
        else:
            output_audio = output
            
        audio_data = find_and_read_mp3("../audio/", "%s.mp3"%output_audio)
        if audio_data:

            st.audio(audio_data,autoplay = True)

        else:
            try:
                tts = gTTS(output, lang='en', tld='com')
            except gtts.tts.gTTSError:
                st.write('The network is unstable, please try again')

            tts.save("../audio/%s.mp3"%output_audio)

            st.audio("../audio/%s.mp3"%output_audio,autoplay = True)

        st.session_state.messages.append({"role": "assistant", "content": output})
        st.session_state.flag = prev_flag
        st.session_state.prompt = None

    else:
        st.text('type to talk')


    prompt_input = st.chat_input("type to talk or use the keyboard’s built-in speech-to-text")
    if prompt_input:
        st.session_state.prompt = prompt_input
        st.rerun()

    st.session_state.point,step1,step2,step3,step4,step5,step6,step7 = steps_and_point_retrieval(st.session_state.point,st.session_state.state,st.session_state.state_goal)
    show_case(st.session_state.option,step1,step2,step3,step4,step5,step6,step7)   
    show_point(st.session_state.point,st.session_state.state_all) 
    save_point(state_goal=st.session_state.state_goal, pointss=st.session_state.student_points,timess=st.session_state.student_times, option=st.session_state.option, student_id=st.session_state.student_id, file_path="student_goal.txt")
    
    time_now = time.time()
    passed_time = round(time_now - st.session_state.time)

    save_point_5min(state_goal=st.session_state.state_goal, points=st.session_state.point,full_point=st.session_state.state_all,timess=passed_time, option=st.session_state.option, student_id=st.session_state.student_id, file_path="student_goal.txt")
    save_point_10min(state_goal=st.session_state.state_goal, points=st.session_state.point,full_point=st.session_state.state_all,timess=passed_time, option=st.session_state.option, student_id=st.session_state.student_id, file_path="student_goal.txt")
    save_point_15min(state_goal=st.session_state.state_goal, points=st.session_state.point,full_point=st.session_state.state_all,timess=passed_time, option=st.session_state.option, student_id=st.session_state.student_id, file_path="student_goal.txt")

    detail_retrieval(st.session_state.state_goal,st.session_state.option)





