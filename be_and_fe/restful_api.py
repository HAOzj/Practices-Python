# -*- coding: utf8 -*-
"""
Created on Sep 29, 2024

@author: woshihaozhaojun@sina.com
"""

from flask import Flask, request, jsonify
from flask_api import status
from flask_cors import CORS

from util.pg import Postgres

conf_dict = {
    'database': "hzj_db",
    "host": "127.0.0.1",
    "port": "5432",
    "user": "hzj",
    "password": "haozhao1991"
}

post_gres = Postgres(conf_dict)
app = Flask(__name__)

CORS(app)

@app.route("/get_full_name", methods=["GET"])
def hello():
    init = request.args.get("init")
    res = post_gres.query(f"SELECT full_name FROM user_name WHERE init='{init}'")
    if not res:
        return jsonify(dict()), status.HTTP_404_NOT_FOUND
    return jsonify({"full_name": ','.join([tmp[0] for tmp in res])}), status.HTTP_200_OK

if __name__ == "__main__":
    app.run(port=3527, debug=True)



