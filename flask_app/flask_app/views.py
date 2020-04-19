"""Flask application views."""
from flask import render_template
from . import app
from flask import jsonify
from . import env_auth

@app.route("/")
def root():
    """Main."""
    return render_template("index.html", msg="Awesome, juniper works!")

@app.route('/api/v1/tests/simple-object', methods=['GET'])
def simple_object():
    obj = {'string_member': 'string value', 'int_member': 2}
    return jsonify(obj)

@app.route('/api/v1/tests/secure-object', methods=['GET'])
@env_auth.require_api_key
def secure_object():
    obj = {'secure_string_member': 'secure string value', \
           'secure_int_member': 3}
    return jsonify(obj)
