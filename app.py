from flask import Flask, request


app = Flask(__name__)


@app.route('/url1', methods=['GET'])
def func1():
	if request.method == 'GET':
		return 'STH'


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=18000)

