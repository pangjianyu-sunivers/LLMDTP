from zhipuai import ZhipuAI
from flask import Flask, request, jsonify
import json

client = ZhipuAI(api_key="a70b9280bfb005a9a904ec35550e0d40.GGgqgnCARTT6IbC9")

app = Flask(__name__)

@app.route("/", methods=["POST"])
def create_item():
    global client
    json_post_raw = request.get_json()
    json_post = json.dumps(json_post_raw)
    json_post_list = json.loads(json_post)
    input_text_q = json_post_list.get('prompt')
    
    response = client.chat.completions.create(
        model="glm-4",
        messages=[{"role": "user", "content": input_text_q}],
        temperature=0.3
    )
    
    output_text_q = str(response.choices[0].message).split('role=')[0][9:-1]
    return output_text_q

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5008)

