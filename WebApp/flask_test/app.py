import os
from flask import Flask, render_template, url_for
app = Flask(__name__)

# @app.route("/")
# def hello():
#     return "Hello World!"

@app.route("/")
def getplots():
    plots = [(x ,str("../../files/plot/" + x)) for x in os.listdir("static/Plot")]
    return render_template("template.html", plots=plots)

if __name__ == "__main__":
    app.run()
