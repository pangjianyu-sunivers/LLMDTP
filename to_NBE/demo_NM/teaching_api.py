# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import json
import chromadb 
from sentence_transformers import SentenceTransformer
from chromadb.utils import embedding_functions
import random


app = Flask(__name__)


chroma_client = chromadb.Client() 
emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="../../distiluse-base-multilingual-cased-v1")
collection = chroma_client.get_or_create_collection(name="chatZOC", embedding_function=emb_fn) 

def load_data_to_chroma(data_path):

    if 'modified' in data_path:
        with open(data_path, 'r', encoding='utf-8') as file:
            jss = json.load(file)

            # parse
            # print(jss[:]['no.'])
            # print(jss[:]['no.'].values())
            ids = list((jss['no.']).values())
            ids = [str(x) for x in ids]
            documents = list((jss['医生问诊问题']).values())     
            metadatas = []

            for key in jss['医生问诊问题'].keys():
                entry = {
                    k: jss[k][key] if jss[k][key] is not None else "" for k in ["no.", "问题的序号", "问题得分", "病历分类", "大类别", "小类别", "症状细节", "医生问诊问题", "是否需要问该问题（0不需要问，1必须要问，2可问可不问）", "患者信息（病历）", "口语化回答", "口语化回答1", "口语化回答0"]
                }
                metadatas.append(entry)
        return documents, metadatas, ids

    else:
        with open(data_path, 'r', encoding='utf-8') as file:
            jss = json.load(file)

            ids = list((jss['no.']).values())
            ids = [str(x) for x in ids]
            documents = list((jss['医生问诊问题']).values())    

            metadatas = []

            for key in jss['医生问诊问题'].keys():
                entry = {
                    k: jss[k][key] if jss[k][key] is not None else "" for k in ["no.", "问题的序号", "问题得分", "病历分类", "大类别", "小类别", "症状细节", "医生问诊问题", "是否需要问该问题（0不需要问，1必须要问，2可问可不问）", "患者信息（病历）", "口语化回答1", "口语化回答0"]
                }
                metadatas.append(entry)
        return documents, metadatas, ids


def building_collection(data_path):

    del_ids = collection.get(include=["documents"])['ids']
    if del_ids != []:
        collection.delete(ids=del_ids)
    documents, metadatas, ids = load_data_to_chroma(data_path)

    collection.upsert(documents=documents, metadatas=metadatas, ids=ids)

def convert_to_embedding(user_input, n_results=1, collection=collection):
    results = collection.query(
        query_texts=[user_input],
        n_results=n_results
    )
    return results


def parse_response(res, verbose=True):

    distance_cutoff0 = 0.85
    distance_cutoff1 = 0.65
    distance_cutoff2 = 0.35
    col_choice = '医生问诊问题'

    
    result_ls = []
    distances = res['distances'][0]

    if len(distances) == 0 or min(distances) > distance_cutoff0:
        flag = -1
        state = {}
        return "No match from database", flag, state
    elif min(distances) < distance_cutoff0 and min(distances) > distance_cutoff1:
        flag = 0
        state = {}
        return "No match from database", flag, state
    else:
        for idx, distance in enumerate(distances):

            if distance < distance_cutoff2:
                flag = 2
                if res['metadatas'][0][idx]['口语化回答'] == 1 or res['metadatas'][0][idx]['口语化回答'] == 2:
                    match_out = res['metadatas'][0][idx]['口语化回答1']
                elif res['metadatas'][0][idx]['口语化回答'] == 0:
                    match_out = res['metadatas'][0][idx]['口语化回答0']
                state_meta = res['metadatas'][0][idx]
                result_ls.append({'result':match_out, 'flag':flag, 'idx':idx, "state":state_meta, "distance":distance})

                break

            if distance < distance_cutoff1 and distance > distance_cutoff2:
                flag = 1
                if res['metadatas'][0][idx]['口语化回答'] == 1:
                    match_out = res['metadatas'][0][idx]['口语化回答1']
                elif res['metadatas'][0][idx]['口语化回答'] == 0:
                    match_out = res['metadatas'][0][idx]['口语化回答0']
                state_meta = res['metadatas'][0][idx]
                result_ls.append({'result':match_out, 'flag':flag, 'idx':idx, "state":state_meta, "distance":distance})


        if flag == 2:
            result = result_ls[0]['result']
            flag = 2
            state = result_ls[0]['state']

        if flag == 1:
            result = "\n".join([x['result'] for x in result_ls])
            flag = 1
            state_ls = [x['state'] for x in result_ls]
            state = {k: v for d in state_ls for k, v in d.items()}

    if verbose==True:

        all_match = res['metadatas'][0]
        q_match = [x['医生问诊问题'] for x in all_match]

        return result, flag, state


def format_prompt(user_input, supporting_material, lang):

    if lang == 'ch':
        
        if type(supporting_material) == list:
            supporting_material = "。".join(supporting_material)+"。"

        prompt = f"""以第一人称回答，仅回答医生提问的内容，不要回答多余的内容，不要自己延伸回答的内容，如果 #患者信息# 中没有提到，则说”我不知道“\n\n#患者信息#\n{supporting_material}\n\n#医生问题#\n{user_input}"""
    return prompt


import requests
def send_to_llm(prompt):
    data = {"prompt": prompt}
    response = requests.post("http://localhost:5008/", json=data)
    return response.text[:-1]


def retrieve_goal(path):

    with open(path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    inquiry_content = data.get("病历分类")
    question_numbers = data.get("问题的序号")
    question_points = data.get("问题得分")

    unique_numbers = []
    unique_state = []
    unique_point = []
    pre_content = '基本信息'
    pre_num = 0
    for i in range(len(question_numbers)):
        i = str(i)
        if inquiry_content[i] != pre_content:
            unique_state.append({"病历分类":pre_content,"问题的序号":unique_numbers,"问题得分":unique_point})       
            unique_numbers = []
            unique_point = []    
        pre_content = inquiry_content[i]   
        if question_numbers[i] != pre_num:
            unique_numbers.append(question_numbers[i]) 
            unique_point.append(question_points[i])   
        pre_num = question_numbers[i]
    unique_state.append({"病历分类":pre_content,"问题的序号":unique_numbers,"问题得分":unique_point})
    return unique_state

responses_no_related = [
  "这个问题跟我的眼病没有关系吧",
  "问题请集中在我眼病上",
  "我不想回答这个问题，因为这好像跟我的眼病无关",
  "我现在正在担心自己的眼病，请不要闲聊了",
  "我现在不想回答眼病无关的问题"
]
responses_1 = [
  "能不能问的再仔细点？具体指的是？",
  "能问详细点吗？具体是？",
  "你能重复一遍吗？问详细一点",
  "你的问题具体是指什么？可以问详细一点吗？",
  "你问的具体是什么？说详细一点可以吗？"
]
responses_2 = [
  "这个问题我真的不太清楚",
  "这问题真的不太清楚",
  "这个不太清楚",
  "这个就不大清楚了",
  "这个问题就不太清楚了"
]
def get_random_response_not_related():
    return random.choice(responses_no_related)
def get_random_response_first():
    return random.choice(responses_1)
def get_random_response_second():
    return random.choice(responses_2)


@app.route('/load', methods=['POST'])
def loading_knowledge_base():
    user_kb = '../knowledge_base_new/' + request.json['load'][0]['model']
    building_collection(user_kb)
    print(user_kb)
    print('成功创建知识库')
    state_goal = retrieve_goal(user_kb)
    return state_goal



@app.route('/chat', methods=['POST'])
def chat_with_chatZOC():
    user_input = request.json['messages'][0]['content']
    prev_q = request.json['messages'][0]['prev_q']
    prev_flag = request.json['messages'][0]['prev_flag']

    student_id = request.json['messages'][0]['student_id']
    res = convert_to_embedding(user_input, n_results=3)
    
    supporting_material, flag, state = parse_response(res, verbose=True)
 
    if flag == -1:
        response_to_not_related = get_random_response_not_related()
        response_with_state = {'response':response_to_not_related, 'state': state, 'flag':flag}
        return response_with_state

    if flag == 0:
        print('prev_flag:',prev_flag,type(prev_flag),type(flag))
        if prev_flag != 0:
            response_to_0 = get_random_response_first()
        else:
            response_to_0 = get_random_response_second()
        response_with_state = {'response':response_to_0, 'state':state, 'flag':flag}
        return response_with_state

    if flag == 2:
        if supporting_material == '柳某':
            response = '我的名字是柳某'
        elif supporting_material == '冯某某':
            response = '我的名字是冯某某'
        else:
            new_prompt = f"现在有一段医患问答对话：\n医生：{user_input}\n患者：{supporting_material}\n现在你需要扮演其中的患者，同义转述患者的回答，用第一人称回答，不需要生成其他多余的内容"
            response = send_to_llm(new_prompt)
        response_with_state = {'response':response, 'state': state, 'flag':flag}
        return response_with_state

    if flag == 1:    
        lang = 'ch'  

        new_prompt = format_prompt(user_input, supporting_material, lang)


        response = send_to_llm(new_prompt)

        response_with_state = {'response':response, 'state':state, 'flag':flag}
        response_with_state = json.dumps(response_with_state)

        return response_with_state


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8891, debug=True)


        
