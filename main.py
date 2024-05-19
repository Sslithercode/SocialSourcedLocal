from flask import Flask, redirect, url_for, render_template, request, session

app = Flask(__name__)
app.secret_key = "hello"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/planning", methods = ["POST", "GET"])
def interact():
    if request.method == "POST":
        response = request.form["userInput"]
        session["response"] = response  #stored user response in a session 
        return redirect(url_for("interact")) #must have a return statement so I will just put it like this for now 
    else:
        return render_template("interact.html")

@app.route("/about")
def about():    
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug = True)