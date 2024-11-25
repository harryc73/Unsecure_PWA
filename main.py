from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import user_management as dbHandler
import html
import re

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
        feedback = check_feedback(feedback)
        feedback = replace_characters(feedback)
        dbHandler.insertFeedback(feedback)
        dbHandler.listFeedback()
        return render_template("/success.html", state=True, value="Back")
    else: #exceptions not handled properly, security risk as can be exploited
        dbHandler.listFeedback()
        if ValueError:
            return render_template("/success.html", error=True, value="Back")
        return render_template("/success.html", state=True, value="Back")

# Function to sanitise text manually
def replace_characters(input_string: str) -> str:
    to_replace = ["<", ">", ";"]
    replacements = ["%3C", "%3E", "%3B"]
    char_list = list(input_string)
    for i in range(len(char_list)):
        if char_list[i] in to_replace:
            index = to_replace.index(char_list[i])
            char_list[i] = replacements[index]
    return "".join(char_list)

def check_feedback(feedback: str) -> bytes:
    if not issubclass(type(feedback), str):
        raise TypeError("Expected a string")
    if len(feedback) < 9 or len(feedback) > 12:
        raise ValueError("Must be between 9 and 12 characters")
    if re.search(r"[ ]", feedback):
        raise ValueError("contains ' ' space characters")
    if len(re.findall(r"[0-9]", feedback)) < 3:
        raise ValueError("must contain at least 3 digits")
    if len(re.findall(r"[a-zA-Z]", feedback)) < 4:
        raise ValueError("must contain at least 4 letters")
    if re.search(r"[@$!%*?&]", feedback):
        raise ValueError("does contain one of '@$!%*?&' special characters")
    return feedback

@app.route("/signup.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def signup():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        username = request.form["username"]
        feedback = request.form["feedback"]
        DoB = request.form["dob"]
        dbHandler.insertUser(username, feedback, DoB) #no hashing or salting function 
        return render_template("/index.html")
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
        isLoggedIn = dbHandler.retrieveUsers(username, password) #No exception handling, or data santised
        if isLoggedIn:
            dbHandler.listFeedback()
            return render_template("/success.html", value=username, state=isLoggedIn)
        else:
            return render_template("/index.html")
    else:
        return render_template("/index.html")


if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0 #
    app.run(debug=True, host="0.0.0.0", port=5000)
