import subprocess
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    try:
        result = subprocess.check_output(['ls', '-l', '/test-pd']).decode('utf-8')
    except subprocess.CalledProcessError as error:
        result = str(error)
    return "Hello World!\n\n" + result + '\n'

if __name__ == "__main__":
    print (hello())
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
