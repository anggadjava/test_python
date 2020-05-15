from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Class/Model


class Person(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), unique=True)
  phone = db.Column(db.String(200))

  def __init__(self, name, phone):
    self.name = name
    self.phone = phone

# Schema


class PersonSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'phone')


# Init schema
person_schema = PersonSchema()
persons_schema = PersonSchema(many=True)

# Create 
@app.route('/person', methods=['POST'])
def add_person():
  name = request.json['name']
  phone = request.json['phone']

  new_person = Person(name, phone)

  db.session.add(new_person)
  db.session.commit()

  return person_schema.jsonify(new_person)

# Get All 
@app.route('/person', methods=['GET'])
def get_persons():
  all_persons = Person.query.all()
  result = persons_schema.dump(all_persons)
  return jsonify(result)

# Get 
@app.route('/person/<id>', methods=['GET'])
def get_person(id):
  person = Person.query.get(id)
  return person_schema.jsonify(person)

# Update 
@app.route('/person/<id>', methods=['PUT'])
def update_person(id):
  person = Person.query.get(id)

  name = request.json['name']
  phone = request.json['phone']

  person.name = name
  person.phone = phone

  db.session.commit()

  return person_schema.jsonify(person)

# Delete
@app.route('/person/<id>', methods=['DELETE'])
def delete_person(id):
  person = Person.query.get(id)
  db.session.delete(person)
  db.session.commit()

  return person_schema.jsonify(person)


# Run Server
if __name__ == '__main__':
  app.run(debug=True)
