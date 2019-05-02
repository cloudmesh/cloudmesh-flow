
import connexion
from flask import render_template, request

app = connexion.App(__name__, specification_dir="./")


# Read the yaml file to configure the endpoints
app.add_api("server.yaml")

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

# create a URL route in our application for "/"
@app.route("/flow/")
def home():


    return render_template("home.html")


@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

def run():
    try:
        app.run(host="127.0.0.1", port=8080, debug=True)
    except RuntimeError as error:
        if  str(error) == "The server is shutting down.":
            pass
        else:
            print("An unexpected error has happended.")

if __name__ == "__main__":
    run()




