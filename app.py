# app.py
from flask import Flask, request, jsonify
app = Flask(__name__)

# A welcome message to test our server
@app.route('/', methods=["GET", "POST"])
def index():
    msg = ""
    if request.method == "POST":
        msg = request.form
    return f"<h1>Welcome to our server !! {msg}</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
