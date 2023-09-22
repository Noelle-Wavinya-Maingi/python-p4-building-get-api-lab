from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

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
    try:
        bakeries = Bakery.query.all()
        bakeries_list = [bakery.to_dict() for bakery in bakeries]
        response = jsonify(bakeries_list)
        return response, 200
    except Exception as e:
        error_message = "An error occurred while fetching bakeries."
        print(f"Error: {e}")
        response = jsonify({"error": error_message})
        response.status_code = 500
        return response
    
@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()
    if bakery is None:
        return jsonify({'message': 'Bakery not found'}), 404
    
    bakery_dict = bakery.to_dict()
    response = make_response(jsonify(bakery_dict), 200)
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_list = []
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    for baked_good in baked_goods_by_price:
        bakery_dict = baked_good.to_dict()
        baked_goods_list.append(bakery_dict)

    response = make_response(jsonify(baked_goods_list), 200)
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive_baked_good = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    if most_expensive_baked_good is None:
        return jsonify({'message': 'No baked goods found'}), 404

    bakery_dict = most_expensive_baked_good.to_dict()
    response = make_response(jsonify(bakery_dict), 200)
    response.headers['Content-Type'] = 'application/json'
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
