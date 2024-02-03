from flask import Flask
app = Flask(__name__)

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True, port=30000)


@app.route("/content")
def read_file():
    return open("words.txt").read(), 200


@app.route("/register")
def write_to_file():
    open("words.txt", 'w').write("hello")
    return "success", 201



