from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        issue = request.form["issue"]
        against = request.form["against"]
        # Complaint logic
        complaint = f"This is to report an issue regarding {issue} against {against}. Please take the necessary action."
        return render_template("result.html", complaint=complaint)
    return render_template("index.html")
