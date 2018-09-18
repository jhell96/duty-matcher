#!/usr/bin/python3

from flask import Flask, request, jsonify, send_file
from duties import get_match_results

app = Flask(__name__)


@app.route('/')
def index():
    index_file = 'www/index.html'
    return send_file(index_file)


@app.route('/scripts.js')
def js():
    js_file = 'www/scripts.js'
    return send_file(js_file)


@app.route('/run', methods=['GET'])
def run():
    freshq = int(request.values.get('freshman-q')) if request.values.get('freshman-q') else 0
    sophq = int(request.values.get('sophomore-q')) if request.values.get('sophomore-q') else 0
    junq = int(request.values.get('junior-q')) if request.values.get('junior-q') else 0
    senq = int(request.values.get('senior-q')) if request.values.get('senior-q') else 0

    results = get_match_results(quota=[freshq, sophq, junq, senq])
    return jsonify({'results': results})

if __name__ == "__main__":
    port = 5000
    app.run(host='0.0.0.0', port=port)
