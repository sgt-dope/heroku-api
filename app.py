from flask import Flask, jsonify, request, make_response
import json
import os
import io


app = Flask(__name__)


AUTH_USERNAME = os.environ.get("AUTH_USERNAME")
AUTH_PASSWORD = os.environ.get("AUTH_PASSWORD")


data = []



@app.route("/", methods=["GET"])
def show_urls():
    if request.authorization and request.authorization.username == AUTH_USERNAME and request.authorization.password == AUTH_PASSWORD:
        return jsonify(data)
    return make_response("Access denied!", 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})



@app.route("/add", methods=["POST"])
def add_url():
    if request.authorization and request.authorization.username == AUTH_USERNAME and request.authorization.password == AUTH_PASSWORD:
        req_data = request.data
        fix_bytes = req_data.replace(b"'", b'"')
        req_data = json.load(io.BytesIO(fix_bytes)) 

        if len(data) == 0:
            data.append(req_data)
        else:
            data[0]["urls"]["keycloak_url"] = req_data["urls"]["keycloak_url"]
            data[0]["urls"]["app_url"] = req_data["urls"]["app_url"]

        return jsonify(data)
    return make_response("Access denied!", 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})


if __name__ == "__main__":
    app.run("0.0.0.0")