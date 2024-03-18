from flask import Flask, jsonify, json, request
from api.getKeyWords import getEnKeyWords
import api.my_config as config

app = Flask(__name__)
# app.config['DEFAULT_CHARSET'] = 'utf-8'
# 定义一个路由来处理GET请求
@app.route('/api/getKeywords', methods=['POST'])
def hello():
    jsonObject = json.loads(request.data);
    # print(jsonObject['text'][0])
    return jsonify({"results": getEnKeyWords(jsonObject['text'][0])})
    # return "";

# if __name__ == '__main__':
#     app.run(debug=config.debug ,host=config.host, port=config.port)
