from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

# 数据文件路径
DATA_FILE = 'memos.json'


def load():
    """加载数据"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save(data):
    """保存数据"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@app.route('/')
def home():
    return 'Memo API'


# 查看所有
@app.route('/memos', methods=['GET'])
def get_all():
    data = load()
    return jsonify(data)


# 新增
@app.route('/memos', methods=['POST'])
def add():
    data = load()
    new_item = request.get_json()
    if not new_item:
        return jsonify({'error': '无效的JSON数据'}), 400

    new_item['id'] = len(data) + 1
    data.append(new_item)
    save(data)
    return jsonify({'id': new_item['id']}), 201


if __name__ == '__main__':
    # 关键修改：监听所有网络接口，而不仅仅是127.0.0.1
    app.run(host='0.0.0.0', port=5000, debug=False)
