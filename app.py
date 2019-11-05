from flask import Flask, render_template, request
from main import Query

from utils.redis_db import get_common__question, get_history_question
import warnings

warnings.filterwarnings("ignore")
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index(name=None):
    return render_template('index.html', name=name)


# 查找问题主入口
@app.route('/obtain_answer')
def obtain_answer():
    question = request.args.get('question')
    answer = query.query(question)
    return answer


# 在网页端更新历史问题
@app.route('/update_history_answer')
def update_history_answer():
    history_question = get_history_question()
    answer = ""
    for question in history_question:
        answer += "<li><a href='javascript:void(0);' onclick='LinkChatSendClient(this.innerHTML)'>" + question + "</li>"
    return answer


# 在网页端更新常见问题
@app.route('/update_common_answer')
def update_common_answer():
    common_question = get_common__question()
    answer = ""
    for question in common_question:
        answer += "<li><h2><a href='javascript:void(0);' onclick='LinkChatSendClient(this.innerHTML)'>" + question + "</a></h2></li>"
    return answer


if __name__ == '__main__':
    query = Query()
    app.run(debug=False, host="127.0.0.1")
