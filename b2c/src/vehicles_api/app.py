from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, json
from decimal import Decimal
from dotenv import load_dotenv
import os

load_dotenv()


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        # 👇️ if passed object is an instance of Decimal, convert it to string
        if isinstance(obj, Decimal):
            return str(obj)
        # 👇️ otherwise use the default behavior
        return super(CustomJSONEncoder, self).default(obj)


app = Flask(__name__)
app.json_encoder = CustomJSONEncoder
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)


class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.BigInteger, primary_key=True)
    vin = db.Column(db.String(20), unique=True, nullable=True)
    year = db.Column(db.SmallInteger, unique=False, nullable=False)
    model = db.Column(db.String(50), unique=False, nullable=False)
    make = db.Column(db.String(50), unique=False, nullable=False)
    price = db.Column(db.Numeric(9, 2), unique=False, nullable=False)
    country = db.Column(db.String(50), unique=False, nullable=False)
    postal_code = db.Column(db.String(50), unique=False, nullable=True)
    state = db.Column(db.String(50), unique=False, nullable=True)
    city = db.Column(db.String(50), unique=False, nullable=False)
    street_address = db.Column(db.String(50), unique=False, nullable=False)

    def __init__(self, vin, year, model, make, price, country, postal_code, state, city, street_address):
        self.vin = vin
        self.year = year
        self.model = model
        self.make = make
        self.price = price
        self.country = country
        self.postal_code = postal_code
        self.state = state
        self.city = city
        self.street_address = street_address


@app.route('/vehicles/<id>', methods=['GET'])
def get_vehicle(id):
    vehicle = Vehicle.query.get(id)
    del vehicle.__dict__['_sa_instance_state']
    return jsonify(vehicle.__dict__)


@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = []
    for vehicle in db.session.query(Vehicle).all():
        del vehicle.__dict__['_sa_instance_state']
        vehicles.append(vehicle.__dict__)
    return jsonify(vehicles)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
