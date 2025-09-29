# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquakes(id):
    earthquake = Earthquake.query.get(id)

    if not earthquake:
       return jsonify({'message': f'Earthquake {id} not found.'}) , 404


    return jsonify({
        "id": earthquake.id,
        "magnitude": earthquake.magnitude,
        "location": earthquake.location,
        "year": earthquake.year
    }) , 200

@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()

    if not earthquakes:
       return jsonify({
        "count": 0, 
        "quakes": []
       }) , 200

    earthquakes_list = [{
        "id": eq.id,
        "magnitude": eq.magnitude,
        "location": eq.location,
        "year": eq.year
    } for eq in earthquakes]


    return jsonify({
        "count": len(earthquakes_list), 
        "quakes":earthquakes_list
        }) , 200
    

if __name__ == '__main__':
    app.run(port=5555, debug=True)
