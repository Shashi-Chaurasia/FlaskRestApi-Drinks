from enum import unique
from os import name
from flask import Flask , request
# from flask.wrappers import Request
# from werkzeug.wrappers import request

app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)


class Drink(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80) , unique = True , nullable=False)
    desc = db.Column(db.String(120))



    def __repr__(self) -> str:
        return f"{self.name} - {self.desc}"



@app.route('/')
def index():
    return "Hello!"



@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()
    output = []

    for drink in drinks:
        drink_data = {'name': drink.name , 'desc':drink.desc}
        output.append(drink_data)

    return {"drinks":output}


@app.route('/drinks/<id>')
def get_drink(id):
    drink = Drink.query.get_or_404(id)
    return {"name":drink.name , "desc": drink.desc}


@app.route('/drinks' , methods=['POST'])
def add_drink():
    drink = Drink(name = request.json['name'] , desc = request.json['desc'])
    db.session.add(drink)
    db.session.commit()
    return {'id':drink.id}


@app.route('/drinks/<id>' , methods = ['DELETE'])
def delete_drink(id):
    drink = Drink.query.get(id)
    if drink is None:
        return {'error': 'not found'}
    db.session.delete(drink)
    db.session.commit()
    return {'message': 'yeh@.......'}

