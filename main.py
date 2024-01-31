import json
from flask import Flask, request, jsonify
from monitor import setup, util
import atexit
import http
from mysql.connector.locales.eng import client_error


import os
# config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

app = Flask(__name__)
atexit.register(util.cleanup)


@app.route("/api/server", methods=["POST"])
def add_webserver():
    server = request.form.get("server", "www.google.com")
    r = util.register_server(server)
    # print(r)
    if r["id"] != -1:
        return (jsonify(r), http.HTTPStatus.ACCEPTED)
    else:
        return (jsonify(r), http.HTTPStatus.FORBIDDEN)



@app.route("/api/server", methods=["GET"])
def get_server():
    server_id = request.args.get("id", -1)
    if int(server_id) == -1:
        return
    return (jsonify(util.get_server_by_id(server_id)), http.HTTPStatus.OK)



@app.route("/api/server/all", methods=["GET"])
def get_server_all():
    return (jsonify(util.get_all_servers()), http.HTTPStatus.OK)



if __name__ == "__main__":
    with open('config.json') as fp:
        config = json.load(fp)
    host, port = '0.0.0.0', config['server_port']
    setup.run()
    app.run(host=host, port=port, debug=True)

