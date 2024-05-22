from flask import Flask, redirect, url_for, render_template, request, session

app = Flask(__name__)
app.secret_key = "hello"

messages = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/planning", methods = ["POST", "GET"])
def interact():
    if request.method == "POST":
        response = request.form["userInput"]
        messages.append(response)
        return render_template("interact.html", data = messages)
    else:
        return render_template("interact.html", data = messages)

@app.route("/about")
def about():    
    return render_template("about.html")

@app.route('/clean_list', methods=['POST'])
def clean_list():
    global messages
    messages = []
    return redirect(url_for("interact"))


if __name__ == "__main__":
    app.run(debug = True)

