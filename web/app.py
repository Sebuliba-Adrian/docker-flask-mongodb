from flask import Flask
app = Flask(__name__)


@app.route('/hello')
def index():
    return {"message": "Hello Universe!"}, 200


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
