from flask import Flask, render_template, request
import random

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        issue = request.form["issue"]
        against = request.form["against"]

        templates = [
            f"""
            To Whom It May Concern,

            I am writing to file a formal complaint regarding a matter involving "{issue}" against "{against}". The situation has caused considerable concern and must be addressed by the appropriate authorities.

            I urge you to take immediate and appropriate legal or administrative action to resolve this matter efficiently.

            Thank you for your attention to this serious concern.

            Sincerely,  
            The Complainant
            """,

            f"""
            Respected Sir/Madam,

            This is to bring to your notice that I have encountered an issue concerning "{issue}" involving "{against}". I believe this issue is unjust and deserves legal scrutiny.

            Kindly investigate the matter and initiate the required proceedings to ensure justice is served.

            Regards,  
            The Aggrieved
            """,

            f"""
            Dear Concerned Authority,

            I wish to formally report a matter related to "{issue}" in connection with "{against}". This incident has negatively impacted me and I request immediate attention to the problem.

            Please take the necessary steps as per applicable laws to address and resolve the issue effectively.

            Yours faithfully,  
            Complainant
            """
        ]

        complaint = random.choice(templates).strip()
        return render_template("result.html", complaint=complaint)
    return render_template("index.html")
