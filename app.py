#!/usr/bin/python

import sys, hashlib, base64, json
from flask import Flask, request, jsonify, abort, render_template
from mysql import MySQL

config = json.loads(open("config.json").read())
db_data = (config["db"]["host"], config["db"]["port"], config["db"]["user"], config["db"]["pass"], config["db"]["name"], config["db"]["charset"])
try:
    db = MySQL(*db_data)
except Exception as e:
    raise Exception('Database Error')

app = Flask(__name__)
# Message if successful
msg = "Das haben Sie gut gemacht! Leider muss ich ihnen mitteilen, dass sich die Gesch&auml;ftsf&uuml;hrung dagegen entschieden hat Ihnen eine Abfindung - geschweige denn Unternehmensanteile - zu &uuml;berlassen. Vielmehr wurde ihr Vertrag als nichtig angesehen. Wir haben soeben der Polizei ihren Standort &uuml;bermittelt. Sie haben etwa 20 Minuten bevor Sie verhaftet werden. Nutzen Sie die Zeit sinnvoll.<br/>Mit freundlichen Gr&uuml;&szlig;en<br/>Itrago IT Leitung"

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data:
        return jsonify({'error': 'JSON expected'}), 400
    if 'username' not in data:
        return jsonify({'error': 'missing key \'username\''}), 400
    if 'password' not in data:
        return jsonify({'error': 'missing key \'password\''}), 400
    try:
      db = MySQL(*db_data)
    except Exception as e:
      raise Exception('Database Error')
    usr = db.query('SELECT password FROM itrago WHERE username = "{}"'.format(data["username"]))
    if usr is not None and usr.get("password") == hashlib.sha1(data['password'].encode()).hexdigest():
        return jsonify({'msg': msg}), 200
    else:
        return jsonify({'error': 'wrong credentials'}), 400

@app.route('/getInfo', methods=['POST'])
def getInfo():
    return open(config["shell"]["gpgdir"] + "/keyfile.asc", "r").read()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=config["web"]["port"])
