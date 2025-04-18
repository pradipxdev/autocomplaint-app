from flask import Flask, render_template, request

app = Flask(__name__)  # <- THIS LINE is super important

@app.route("/")
def home():
    return render_template("index.html")  # ya jo bhi page hai

# More routes if needed...

if __name__ == "__main__":
    app.run(debug=True)
