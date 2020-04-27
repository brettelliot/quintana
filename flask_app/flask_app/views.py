"""Flask application views."""
from flask import render_template
from . import app
from flask import jsonify
from . import env_auth
from . import model

@app.route("/")
def root():
    """Main."""
    return render_template("index.html", msg="Awesome, quintana works.")

@app.route('/api/v1/stock/<string:symbol>/financials', methods=['GET'])
@env_auth.require_api_key
def get_financials(symbol):
    financials = model.get_financials(symbol)
    return jsonify(financials)
