from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import user_management as dbHandler
import html
import re
import validate_and_sanatise as vs
import two_fa

# Code snippet for logging a message
# app.logger.critical("message")

app = Flask(__name__)


@app.route("/success.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"]) #accepts everything
def addFeedback():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        feedback = request.form["feedback"]
        if vs.check_feedback(feedback):
            feedback = vs.replace_characters(feedback)
            dbHandler.insertFeedback(feedback)
            dbHandler.listFeedback()
        else:
            return render_template("/success.html", error=True, value="Back")
        return render_template("/success.html", state=True, value="Back")
    else: #exceptions not handled properly, security risk as can be exploited
        dbHandler.listFeedback()
        if ValueError:
            return render_template("/success.html", error=True, value="Back")
        return render_template("/success.html", state=True, value="Back")

@app.route("/signup.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def signup():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if password == vs.check_password(password):
            password = vs.hash(password)
            dbHandler.insertUser(username, password)
            return render_template("/index.html")
        else:
            return render_template("/signup.html", error=True, value="Back")
    else:
        return render_template("/signup.html")


@app.route("/index.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"]) #Should only have methods required allowed (i.e. Post and Get)
@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password = vs.hash(password)
        isLoggedIn = dbHandler.retrieveUsers(username, password) #No exception handling, or data santised
        if isLoggedIn:
            key = two_fa.get_2fa()
            return render_template("/2fa.html")
        else:
            return render_template("/index.html")
    else:
        return render_template("/index.html")

@app.route("/verify_2fa", methods=["POST"])
def verify_2fa():
    key = request.form["key"]
    code = request.form["code"]
    if two_fa.check_2fa(code):
        dbHandler.listFeedback()
        return render_template("/success.html")
    else:
        return render_template("/2fa.html", error=True, value="Back")


if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0 #
    app.run(debug=True, host="0.0.0.0", port=5000)
