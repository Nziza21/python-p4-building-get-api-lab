#!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries_list = Bakery.query.all()
    bakeries_data = [{'id': bakery.id, 'name': bakery.name} for bakery in bakeries_list]
    return jsonify(bakeries_data)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get_or_404(id)
    bakery_data = {'id': bakery.id, 'name': bakery.name}
    return jsonify(bakery_data)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_list = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_data = [{'id': baked_good.id, 'name': baked_good.name, 'price': baked_good.price} for baked_good in baked_goods_list]
    return jsonify(baked_goods_data)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    baked_good_data = {'id': most_expensive.id, 'name': most_expensive.name, 'price': most_expensive.price}
    return jsonify(baked_good_data)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
