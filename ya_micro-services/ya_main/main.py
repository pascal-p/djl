from dataclasses import dataclass
from flask import Flask
from flask_cors import CORS
from flask import Flask, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

import requests

from producer import publish

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@db:5432/ya_main"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

db = SQLAlchemy(app)

@dataclass
class Product(db.Model):
    id: int
    title: str
    image: str

    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=False)  # Product (hence id) created from Django App...
    #                                    # ...and here we will this create id
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))

@dataclass
class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    UniqueConstraint('user_id', 'product_id', name='user_product_unique')


@app.route('/api/products')
def index():
    return jsonify(Product.query.all())

@app.route('/api/products/<int:id>/like', methods=['POST'])
def like(id):
    # get the random id (for user) from ther Django App
    req = requests.get('http://172.17.0.1:8000/api/user')
    json = req.json()

    try:
        productUser = ProductUser(user_id=json['id'], product_id=id)
        db.session.add(productUser)
        db.session.commit()
        publish('product_liked', id)

    except:
        abort(400, 'You already liked this product')

    else:
        return jsonify({
            'message': 'success'
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
