import json
from os import environ
import re

from app import app
from models import db, Bakery, BakedGood
from datetime import datetime

class TestApp:
    '''Flask application in flask_app.py'''

    def test_bakeries_route(self):
        '''has a resource available at "/bakeries".'''
        response = app.test_client().get('/bakeries')
        assert(response.status_code == 200)

    def test_bakeries_route_returns_json(self):
        '''provides a response content type of application/json at "/bakeries"'''
        response = app.test_client().get('/bakeries')
        assert response.content_type == 'application/json'

    def test_bakeries_route_returns_list_of_bakery_objects(self):
        '''returns JSON representing models.Bakery objects.'''
        with app.app_context():
            b = Bakery(name="My Bakery")
            db.session.add(b)
            db.session.commit()

            response = app.test_client().get('/bakeries')
            data = json.loads(response.data.decode())
            print("Returned data:", data)

            contains_my_bakery = False
            for record in data:
                print("Record:", record)
                assert type(record) == dict
                assert record['id']
                assert record['name']
                assert 'created_at' not in record, f"Record: {record}"
                if 'created_at' in record:
                    assert record['created_at'] is not None, f"Record: {record}"
                    assert isinstance(record['created_at'], str)

                    # Check if 'created_at' can be parsed as datetime
                    try:
                        datetime.strptime(record['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
                    except ValueError:
                        assert False, f"Invalid 'created_at' format: {record['created_at']}"

                    if record['name'] == "My Bakery":
                        contains_my_bakery = True

            assert contains_my_bakery

            db.session.delete(b)
            db.session.commit()

    def test_bakery_by_id_route(self):
        '''has a resource available at "/bakeries/<int:id>".'''
        with app.app_context():
            b = Bakery(name="My Bakery")
            db.session.add(b)
            db.session.commit()

            response = app.test_client().get(f'/bakeries/{b.id}')
            assert(response.status_code == 200)
            db.session.delete(b)
            db.session.commit()

    def test_bakery_by_id_route_returns_json(self):
        '''provides a response content type of application/json at "/bakeries/<int:id>"'''
        with app.app_context():
            b = Bakery(name="My Bakery")
            db.session.add(b)
            db.session.commit()

            response = app.test_client().get(f'/bakeries/{b.id}')
            assert response.content_type == 'application/json'
            db.session.delete(b)
            db.session.commit()
        

    def test_bakeries_route_returns_one_bakery_object(self):
        '''returns JSON representing one models.Bakery object.'''
        with app.app_context():
            b = Bakery(name="My Bakery")
            db.session.add(b)
            db.session.commit()

            response = app.test_client().get(f'/bakeries/{b.id}')
            data = json.loads(response.data.decode())
            assert(type(data) == dict)
            assert(data['id'] == b.id)
            assert(data['name'] == "My Bakery")
            if 'created_at' in data:
                assert(data['created_at'] is not None)
                assert(isinstance(data['created_at'], str))

                # Check if 'created_at' can be parsed as datetime
                try:
                    datetime.strptime(data['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
                except ValueError:
                    assert False, f"Invalid 'created_at' format: {data['created_at']}"

            db.session.delete(b)
            db.session.commit()

    def test_baked_goods_by_price_route(self):
        '''has a resource available at "/baked_goods/by_price".'''
        response = app.test_client().get('/baked_goods/by_price')
        assert(response.status_code == 200)
    
    def test_baked_goods_by_price_route_returns_json(self):
        '''provides a response content type of application/json at "/baked_goods/by_price"'''
        response = app.test_client().get('/baked_goods/by_price')
        assert response.content_type == 'application/json'

    def test_baked_goods_by_price_returns_list_of_baked_goods_in_descending_order(self):
        '''returns JSON representing one models.Bakery object.'''
        with app.app_context():
            prices = [baked_good.price for baked_good in BakedGood.query.all()]
            highest_price = max(prices)

            b1 = BakedGood(name="Madeleine", price=highest_price + 1)
            db.session.add(b1)
            db.session.commit()
            b2 = BakedGood(name="Donut", price=highest_price - 1)
            db.session.add(b2)
            db.session.commit()

            response = app.test_client().get('/baked_goods/by_price')
            data = json.loads(response.data.decode())
            assert(type(data) == list)
            for record in data:
                assert(record['id'])
                assert(record['name'])
                assert(record['price'])
                if 'created_at' in record:
                    assert(record['created_at'] is not None)

            prices = [record['price'] for record in data]
            assert(all(prices[i] >= prices[i+1] for i in range(len(prices) - 1)))

            db.session.delete(b1)
            db.session.delete(b2)
            db.session.commit()
            
    def test_most_expensive_baked_good_route(self):
        '''has a resource available at "/baked_goods/most_expensive".'''
        response = app.test_client().get('/baked_goods/most_expensive')
        assert(response.status_code == 200)

    def test_most_expensive_baked_good_route_returns_json(self):
        '''provides a response content type of application/json at "/bakeries/<int:id>"'''
        response = app.test_client().get('/baked_goods/most_expensive')
        assert response.content_type == 'application/json'

    def test_most_expensive_baked_good_route_returns_one_baked_good_object(self):
        '''returns JSON representing one models.BakedGood object.'''
        with app.app_context():
            prices = [baked_good.price for baked_good in BakedGood.query.all()]
            highest_price = max(prices)

            b1 = BakedGood(name="Madeleine", price=highest_price + 1)
            db.session.add(b1)
            db.session.commit()
            b2 = BakedGood(name="Donut", price=highest_price - 1)
            db.session.add(b2)
            db.session.commit()

            response = app.test_client().get('/baked_goods/most_expensive')
            data = json.loads(response.data.decode())
            assert(type(data) == dict)
            assert(data['id'])
            assert(data['name'])
            assert(data['price'])
            if 'created_at' in data:
                assert('created_at' in data)
                assert(data['created_at'] is not None)

                try:
                    datetime.strptime(data['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
                except ValueError:
                    assert False, f"Invalid 'created_at' format: {data['created_at']}"

            db.session.delete(b1)
            db.session.delete(b2)
            db.session.commit()