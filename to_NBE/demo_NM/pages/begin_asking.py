import os
# os.environ["STREAMLIT_SERVER_MODE"] = "production"
import streamlit as st
import random
import time
import streamlit as st
# from bokeh.models.widgets import Button
# from bokeh.models import CustomJS
import re
# from streamlit_bokeh_events import streamlit_bokeh_events
import json
import requests
from gtts import gTTS
from io import BytesIO
# import openai
import base64
from pydub import AudioSegment
import pickle
import sys
from pygtrans import Translate


# 函数用于向服务器内建的API发送请求并获取回复
def generate_response(prompt,prev_q,prev_flag):
    if st.session_state.option == 'ChatZOC':
        url = 'http://127.0.0.1:8891/chat_zh'
    else:
        url = 'http://127.0.0.1:8891/chat'
    response_with_state = requests.post(url, headers={'Content-Type': 'application/json'}, json= {"messages": [{"role": "user", "content": prompt, "prev_q": prev_q, "prev_flag": prev_flag, 'student_id': st.session_state.student_id}]})
    # print(response_with_state.text['response'])
    # print(response.text)
    return response_with_state

# 左侧边栏显示基础
def show_case(option,step1,step2,step3,step4,step5,step6,step7):

        # st.write(word)


        with st.sidebar:   
            
            ############## 显示问诊状况
            tik_wide = 25
            col1, col2, col3, col4 = st.columns([1, 4, 1, 4])
            # step1 = True
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

        # 打开文件以写入模式，将标准输出重定向到文件
        with open(file_path, "a") as file:
            sys.stdout = file  # 将标准输出重定向到文件

            # 这里写入你想要保存的内容，使用 print
            print('test finish')
            print(state_out)
            print(state_goal)

        # 恢复原始的标准输出对象
        sys.stdout = original_stdout

def save_point_5min(state_goal, points,full_point,timess, option, student_id='0', file_path="student_goal.txt"):        
    if timess >= int(300) and st.session_state.auto_save == '0min':
        print('time pass:',timess,type(timess))  
        st.session_state.auto_save = '5min'

        state_out = {"student_id":student_id,"test_option":option,"student_points":round(points/full_point*100,2),"exam_time":timess}

        original_stdout = sys.stdout

        # 打开文件以写入模式，将标准输出重定向到文件
        with open(file_path, "a") as file:
            sys.stdout = file  # 将标准输出重定向到文件

            # 这里写入你想要保存的内容，使用 print
            print('5min auto save')
            print(state_out)
            print(state_goal)

        # 恢复原始的标准输出对象
        sys.stdout = original_stdout

def save_point_10min(state_goal, points,full_point,timess, option, student_id='0', file_path="student_goal.txt"):  
    if timess >= int(600) and st.session_state.auto_save == '5min':
        print('time pass:',timess,type(timess))  
        st.session_state.auto_save = '10min'

        state_out = {"student_id":student_id,"test_option":option,"student_points":round(points/full_point*100,2),"exam_time":timess}

        original_stdout = sys.stdout

        # 打开文件以写入模式，将标准输出重定向到文件
        with open(file_path, "a") as file:
            sys.stdout = file  # 将标准输出重定向到文件

            # 这里写入你想要保存的内容，使用 print
            print('10min auto save')
            print(state_out)
            print(state_goal)

        # 恢复原始的标准输出对象
        sys.stdout = original_stdout

def save_point_15min(state_goal, points,full_point,timess, option, student_id='0', file_path="student_goal.txt"):        
        
    if timess >= int(900) and st.session_state.auto_save == '10min':
        print('time pass:',timess,type(timess))  
        st.session_state.auto_save = '15min'

        state_out = {"student_id":student_id,"test_option":option,"student_points":round(points/full_point*100,2),"exam_time":timess}

        original_stdout = sys.stdout

        # 打开文件以写入模式，将标准输出重定向到文件
        with open(file_path, "a") as file:
            sys.stdout = file  # 将标准输出重定向到文件

            # 这里写入你想要保存的内容，使用 print
            print('15min auto save')
            print(state_out)
            print(state_goal)

        # 恢复原始的标准输出对象
        sys.stdout = original_stdout


def show_point(points,full_point):
    with st.sidebar:  
        ############## 确认选择
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
            # print(state[i]['病历分类'], state[i]['问题的序号'])
            # 寻找匹配的项并删除问题的序号
            for item in state_goal:
                if item['病历分类'] == state[i]['病历分类']:
                    if state[i]['问题的序号'] in item['问题的序号']:
                        item['问题的序号'].remove(state[i]['问题的序号'])
                # 如果问题的序号为空，则输出病历分类
                if not item['问题的序号']:
                    # print("病历分类:", item['病历分类'])   
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
            # print(state)
            # print(state_goal)


    return step1,step2,step3,step4,step5,step6,step7


# 左侧边栏实时状态显示
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
            # print(state[i]['病历分类'], state[i]['问题的序号'])
            # 寻找匹配的项并删除问题的序号
            for item in state_goal:
                if item['病历分类'] == state[i]['病历分类']:
                    if state[i]['问题的序号'] in item['问题的序号']:
                        item['问题的序号'].remove(state[i]['问题的序号'])
                        item['问题得分'].remove(state[i]['问题得分'])
                        points = points + state[i]['问题得分']
                # 如果问题的序号为空，则输出病历分类
                if not item['问题的序号']:
                    # print("病历分类:", item['病历分类'])   
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
            # print(state)
            # print('----------------------')
            # print(state_goal)

    return points,step1,step2,step3,step4,step5,step6,step7


def info_extract_from_excel(type_name,item,df):
    if item == []:
        print('empty')
        response_detail = f"[{type_name}]部分无缺漏"
    
    else:
        result = ''
        print(item,type(item))
        # item = list(item)
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
            # print("病历分类:", item['病历分类'])
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
    # 获取文件夹中所有文件
    files = os.listdir(folder_path)

    # 检查每个文件是否是MP3格式并且文件名符合要求
    for file in files:
        if file.endswith(".mp3") and file == file_name:
            # 构建完整的文件路径
            file_path = os.path.join(folder_path, file)

            # 读取MP3文件
            # audio = AudioSegment.from_mp3(file_path)
            # with open(file_path, "rb") as f:
            #     data = f.read()

            # 在这里你可以对音频进行其他处理，或者返回音频对象
            return file_path

    # 如果没有找到指定文件名的MP3文件
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
############# 设定全局保持变量

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

# ############# 选择模拟患者
# option = st.selectbox(
#         '请选择一位患者',
#         ('none','no.1', 'no.2', 'no.3'))

# ############## 确认选择
# if st.button('确认'):  
#     st.write('当前患者:', option)      
#     st.session_state.chat = 'on'


############## 选择完毕患者后开始问答
if st.session_state.chat == 'on':

    # Initialize chat history
    if st.session_state.option != 'ChatZOC' :
        # if st.session_state.option == 'modified_25_翼状胬肉_1':
        #     option = 'modified_25_翼状胬肉_1'
        #     photo = "../icons/test_patient_25.jpg"
        #     word = "male，43 years old..."
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
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:

        # with st.chat_message(message["role"]):
            # # st.markdown(message["content"])
            # if message["role"] == 'assistant':
        prev_q = message["content"]
                # prev_flag = st.session_state.flag

    if st.session_state.prompt:
        prompt = client.translate(st.session_state.prompt, target="zh").translatedText
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        # with st.chat_message("user"):
            # st.markdown(prompt)
        asking = prompt
        # print('前-----------',prev_flag)
        response_with_state = generate_response(asking,prev_q,prev_flag)
        if st.session_state.option != 'ChatZOC' :
            print(response_with_state)
            output = json.loads(response_with_state.text)['response']
            print(output)
            output = client.translate(output, target="en").translatedText
            output = output.replace("&#39;","'")
            prev_flag = json.loads(response_with_state.text)['flag']
            # print(json.loads(response_with_state.text)['state'])
            st.session_state.state.append(json.loads(response_with_state.text)['state'])
        else:
            output = response_with_state.text

        # Display assistant response in chat message container
        # with st.chat_message("assistant"):
        message_placeholder = st.empty()
        # full_response = ""

        # for chunk in output.split():
        #     full_response += chunk + " "
        #     time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            # message_placeholder.markdown(full_response + "▌")
            # message_placeholder.markdown(full_response)
        # Add assistant response to chat history
        if output == '没有':
            output = get_random_response_no()
        print('student_id :',st.session_state.student_id,'output', output)

        # with open("../audio/%s.mp3"%output, "rb") as f:
        #     data = f.read()
        if len(output) > 50:
            output_audio = output[:50]
        else:
            output_audio = output
            
        audio_data = find_and_read_mp3("../audio/", "%s.mp3"%output_audio)
        if audio_data:
            print('有重复')
            st.audio(audio_data,autoplay = True)
            # autoplay_audio(audio_data)
        else:
            print('无重复')
            try:
                tts = gTTS(output, lang='en', tld='com')
            except gtts.tts.gTTSError:
                st.write('The network is unstable, please try again')

            tts.save("../audio/%s.mp3"%output_audio)
            # tts.write_to_fp(sound)
            # autoplay_audio("../audio/%s.mp3"%output_audio)
            st.audio("../audio/%s.mp3"%output_audio,autoplay = True)

        st.session_state.messages.append({"role": "assistant", "content": output})
        st.session_state.flag = prev_flag
        st.session_state.prompt = None
        # st.rerun()
        # if st.button('next'):
        #     st.rerun()
    else:
        st.text('type to talk')
        # st.text("2. click 'next' to enter next question")

    prompt_input = st.chat_input("type to talk or use the keyboard’s built-in speech-to-text")
    if prompt_input:
        st.session_state.prompt = prompt_input
        st.rerun()
    # print('@@@@@@@@@@@@@@@@@@@@@@st.session_state.state:', st.session_state.state)
    # 左侧边栏实时状态显示
    # option = 'no.1'  
    # if st.session_state.option == '病例5-打分test-原1': 
    # print(st.session_state.state_goal)
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





