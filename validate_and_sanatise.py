from flask import current_app as app
import re
import bcrypt

def check_feedback(feedback: str) -> bool:
    if not issubclass(type(feedback), str):
        return False
    if len(feedback) < 9 or len(feedback) > 12:
        return False
    if re.search(r"[ ]", feedback):
        return False
    if len(re.findall(r"[0-9]", feedback)) < 3:
        return False
    if len(re.findall(r"[a-zA-Z]", feedback)) < 4:
        return False
    if re.search(r"[@$!%*?&]", feedback):
        return False
    return feedback

def replace_characters(input_string: str) -> str:
    to_replace = ["<", ">", ";"]
    replacements = ["%3C", "%3E", "%3B"]
    char_list = list(input_string)
    for i in range(len(char_list)):
        if char_list[i] in to_replace:
            index = to_replace.index(char_list[i])
            char_list[i] = replacements[index]
    return "".join(char_list)


def check_password(password: str) -> bool:
    if not issubclass(type(password), str):
        return False
    if len(password) < 8:
        return False
    if len(re.findall(r"[0-9]", password)) < 2:
        return False
    if len(re.findall(r"[a-zA-Z]", password)) < 2:
        return False
    if not re.search(r"[@$!%*?&]", password):
        return False
    return password

def hash(password: str) -> str:
    salt = b"$2b$12$ieYNkQp8QumgedUo30nuPO"
    encoded_password = password.encode()
    hashed_password = bcrypt.hashpw(password=encoded_password, salt=salt)
    return hashed_password.decode()

def salt() -> str:
    return bcrypt.gensalt().decode()

if __name__ == "__main__":
    app.run(debug=True)