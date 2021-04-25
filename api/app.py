from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = ""
app.config["CORS_HEADERS"] = "Content-Type"
CORS(app)

@app.route('/')
def hello_world():
    return {'status' : 'OK'}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')