from flask import Flask, request, render_template, make_response, send_file, abort
from docx import Document
import time
import os
import json

app = Flask(__name__)

today = time.strftime("%Y-%m-%d", time.localtime(time.time()))  # 当前日期字符串
cur_dir = os.path.dirname(__file__)  # 当前文件所在目录（即项目根目录）


@app.route('/parse_docx', methods=['POST'])  # 解析前端发过来的word文件，将解析的结果以json的形式进行返回
def parse_docx():
    docs = list()
    files = request.files.getlist('file')
    upload_loc = os.path.join(cur_dir, 'static', 'upload')
    for f in files:
        f.save(os.path.join(upload_loc, f.filename))
        document = Document(os.path.join(upload_loc, f.filename))
        paras = [p.text for p in document.paragraphs]
        content = {'content': paras}
        docs.append(content)
    return json.dumps(docs)


@app.route('/save_mark', methods=['POST'])
def save_mark():
    data = request.get_data(as_text=True)  # 获取前端发送过来的数据
    file_loc = os.path.join(cur_dir, 'static', 'saved', today)
    with open(file_loc, 'a', encoding='utf-8') as logfile:
        logfile.write(data + '\n')
    return 'ok'


@app.route('/download_file', methods=['GET'])
def download_file():
    file_loc = os.path.join(cur_dir, 'static', 'saved', today)
    try:
        response = make_response(
            send_file(file_loc, as_attachment=True)
        )
        return response
    except Exception as e:
        print('"code": "异常", "message": "{}"'.format(e))
        abort(404)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('dragging_div.html')


if __name__ == "__main__":
    app.run(debug=True)
