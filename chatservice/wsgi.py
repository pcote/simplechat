from flask import Flask, redirect, request, session, abort, make_response, url_for, render_template, jsonify
import configparser
import chatmodel
import os

app = Flask(__name__)
app.debug=True

config_file_name = "settings.ini"
config_dir = __file__.rsplit("/", maxsplit=1)[0]
config_file_abs_path = "{}{}{}".format(config_dir, "/", config_file_name)
app.logger.info("CONFIG FILE PATH FOR SECRET KEY: {}".format(config_file_abs_path))

cp = configparser.ConfigParser()
cp.read(config_file_abs_path)
secret_key = cp["settings"]["secret_key"]
app.secret_key = secret_key

m = chatmodel.ChatModel(app)


@app.route("/")
def index():
    """
    Simple redirector to the login page.
    :return: 302 message to send the user to login.html
    """
    return redirect("/static/login.html")


@app.route("/login", methods=["POST"])
def login():
    """
    Basic authorization process for logging the user into the system.
    Invoked via the login form.
    :return: A message for the front side Javascript to handle.  Either 200 if login creds pass or 401 if it doesn't.
    """
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
    """
    Makes an account for a new user and sends them straight to chat if it succeeds.
    Sends an error message otherwise.
    :return: Either a redirect or an error message depending on success or failure to make an account.
    """
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
    """
    The templated chat room.
    :return:
    """
    if session and session["logged_in"]:
        return render_template("chatroom.html")
    return redirect(url_for("index"))


@app.route("/sendmessage", methods=["POST"])
def send_message():
    """
    Endpoint where sending chat messages which get passed into the database.
    :return: Either a generic 200 response or 401 depending on whether or not user is properly logged in.
    """
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
    """
    Grab all the chat messages and send it back to the chat interface as json.
    :return: json chat messages
    """
    return jsonify({"messages": m.Messages})

if __name__ == '__main__':
    app.static_folder = "../static/"
    app.run("0.0.0.0", debug=True)
