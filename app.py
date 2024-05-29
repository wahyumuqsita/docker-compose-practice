from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello_world():
    response = {
        "return_code": 200,
        "message": "hello world"
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1)