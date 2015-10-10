from flask import Flask, redirect, request, session, abort, make_response, url_for, render_template, jsonify
import configparser
import chatmodel
app = Flask(__name__)
app.debug=True

m = chatmodel.ChatModel(app)


@app.route("/")
def index():
    return redirect("/static/login.html")

@app.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    username = auth.username
    password = auth.password
    valid_user = m.is_valid_user(username, password)
    if valid_user:
        session["logged_in"] = True
        session["username"] = username
        return make_response("success") # 200 code is the important part here.
    else:
        abort(401, "Incorrect credentials")




@app.route("/createaccount", methods=["POST"])
def create_account():
    json_data = request.get_json()
    username = json_data["username"]
    password = json_data["password"]
    password_again = json_data["password_again"]

    error_message = None

    if m.user_exists(username):
        error_message = "Sorry.  User already exists"
    elif password != password_again:
        error_message = "Sorry.  The passwords you gave do not match each other"
    elif not m.is_strong_password(password):
        error_message = "Sorry.  Password has to be 8 characters or more with a combination of numbers, letters, and punctuation"

    resp = make_response()
    if error_message:
        resp.status_code = 401
        resp.data = error_message
        return resp
    else:
        m.create_user(username, password)
        session["logged_in"] = True
        session["username"] = username
        return redirect(url_for("show_chatroom"))


@app.route("/chatroom", methods=["GET"])
def show_chatroom():
    if session and session["logged_in"]:
        return render_template("chatroom.html")
    return redirect(url_for("index"))


@app.route("/sendmessage", methods=["POST"])
def send_message():
    if session and session["logged_in"]:
        username = session["username"]
        json_data = request.get_json()
        message = json_data["message"]
        m.store_message(username, message)
        okay = make_response("")
        return okay
    else:
        error = make_response("")
        error.data = "not allowed to send the message"
        error.status_code = 401
        return error


@app.route("/getmessages", methods=["GET"])
def get_messages():
    return jsonify({"messages": m.Messages})

if __name__ == '__main__':
    import os
    import sys
    cp = configparser.ConfigParser()
    cp.read("settings.ini")
    secret_key = cp["settings"]["secret_key"]
    app.secret_key = secret_key
    app.static_folder = "../static/"
    app.run("0.0.0.0", debug=True)
