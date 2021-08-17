from flask import Flask, jsonify, request, make_response
import os


app = Flask(__name__)


AUTH_USERNAME = os.environ.get("AUTH_USERNAME")
AUTH_PASSWORD = os.environ.get("AUTH_PASSWORD")


app.config["DEBUG"] = True

data = []



@app.route("/", methods=["GET"])
def show_urls():
    if request.authorization and request.authorization.username == AUTH_USERNAME and request.authorization.password == AUTH_PASSWORD:
        return jsonify(data)
    return make_response("Access denied!", 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})



@app.route("/add", methods=["POST"])
def add_url():
    if request.authorization and request.authorization.username == AUTH_USERNAME and request.authorization.password == AUTH_PASSWORD:
        url = request.args.get('url')
        if len(data) == 0:
            data.append({"url":url})
        else:
            data[0]["url"] = url
        return jsonify([{"msg":"Gitpod workspace url has been changed to " + str(url)}])
    return make_response("Access denied!", 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})



if __name__ == "__main__":
    app.run()