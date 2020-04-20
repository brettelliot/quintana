import os
from flask import Flask
from decimal import Decimal
import flask.json
from datetime import datetime, timedelta, date

app = Flask(__name__)

# Load our flask config from class.
configurations = {
    "development": "flask_app.config.DevelopmentConfig",
    "production": "flask_app.config.ProductionConfig",
}
app.config.from_object(configurations[os.getenv("FLASK_ENV")])

# jsonify doesn't naturally turn certain types into json. Use
# this custom encoder to specify how to encode those types.
class MyJSONEncoder(flask.json.JSONEncoder):

    def default(self, obj):
        if type(obj) == Decimal:
            # Convert decimal instances to floats.
            return float(obj)
        elif type(obj) == timedelta:
            # Convert timedeltas to strings
            return str(o)
        elif type(obj) == datetime:
            # Convert datetimes to strings
            return o.isoformat()
        elif type(obj) == date:
            return obj.isoformat()

        return super(MyJSONEncoder, self).default(obj)

app.json_encoder = MyJSONEncoder

import flask_app.views
