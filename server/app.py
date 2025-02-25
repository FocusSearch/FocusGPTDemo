# -*- coding: utf-8 -*-
# @Time    : 2025/2/24 10:33
# @Author  : ShaoJK
# @File    : app.py.py
# @Remark  :
import traceback

from flask import Flask, render_template, jsonify

import config
from services.focus import list_tables, init, chat

app = Flask(__name__, static_folder="static", static_url_path="/")
app.config.from_object(config)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/listTables', methods=['POST'])
def api_list_table():
    return jsonify(list_tables())


@app.route('/init', methods=['POST'])
def api_init():
    return jsonify(init())


@app.route('/chat', methods=['POST'])
def api_chat():
    return jsonify(chat())


@app.errorhandler(Exception)
def exception(e):
    traceback.print_exception(e)
    return jsonify({"message": str(e), "errorType": str(type(e).__name__)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
