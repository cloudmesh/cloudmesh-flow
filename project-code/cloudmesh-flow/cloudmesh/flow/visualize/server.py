
import connexion
from flask import render_template

app = connexion.App(__name__, specification_dir="./")


# Read the yaml file to configure the endpoints
app.add_api("server.yaml")

# create a URL route in our application for "/"
@app.route("/flow/")
def home():


    return render_template("home.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)


