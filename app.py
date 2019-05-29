from flask import Flask, jsonify, make_response, abort, request
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema
from flask_cors import CORS
from pprint import pprint
from yelpapi import YelpAPI
from keys import Keys
yelp_api = YelpAPI(Keys()._id, Keys().secret)

la = 42.39
lo = -72.52


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./db/plated.db'
db = SQLAlchemy(app)

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    type = db.Column(db.String(250)) #cuisine
    popularity = db.Column(db.Float)
    recommendation = db.Column(db.Float, nullable=True) #dict {user_id : float}
    price = db.Column(db.String(5))
    phone = db.Column(db.String(250))
    image_url = db.Column(db.String(250))
    address = db.Column(db.String(250))
    url = db.Column(db.String(250))
    distance = db.Column(db.Float)


class RestaurantSchema(Schema):
    class Meta:
        fields = ['id','name','type','popularity', 'recommendation', 'price', 'phone', 'image_url', 'address', 'url', 'distance']
restaurant_schema = RestaurantSchema()

@app.route('/api/restaurants', methods=['GET'])
def get_restaurants():
    return jsonify([restaurant_schema.dump(restaurant) for restaurant in Restaurant.query.order_by(Restaurant.popularity).all()])


@app.route('/api/restaurants/<int:restaurant_id>', methods=['GET'])
def get_restaurant(restaurant_id):
    restaurant = Restaurant.query.filter(Restaurant.id == restaurant_id).first()#find in resturants
    if not (restaurant): 
        abort(404)
    return jsonify(restaurant_schema.dump(restaurant))

@app.route('/api/restaurants/like', methods=['POST'])
def like_restaurant():
    print(request.form)
    if not request.form:
        abort(400)
    restaurant_id = request.form['id']
    liked = request.form['like']
   
    restaurant = Restaurant.query.filter(Restaurant.id == restaurant_id).first()
    
        
    restaurant.popularity += int(liked);
    db.session.commit()

    return jsonify(restaurant_schema.dump(restaurant)), 201

def create_restaurant(json_data):
    r = Restaurant(name=json_data['name'],
                   popularity = json_data['review_count'],
                   type=json_data['categories'][0]['title'],
                   recommendation=None,
                   price=json_data['price'],
                   phone=json_data['display_phone'],
                   image_url=json_data['image_url'],
                   url=json_data['url'],
                   address= ' '.join(json_data['location']['display_address']),
                   distance=json_data['distance'])
    db.session.add(r)
    db.session.commit()
    return r
@app.route('/api/restaurants', methods=['POST'])
def add_restaurant():
    if not request.json:
        abort(400)
    restaurant = create_restaurant(request.json)
    return jsonify(restaurant_schema.dump(restaurant)), 201

def clear_restaurants():
    Restaurant.query.delete()
    db.session.commit()

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def get_search_parameters(lat, long):
    
    params = {}
    #params["term"] = "restaurant"
    params["ll"] = "{},{}".format(str(lat), str(long))
    #params["radius_filter"] = "2000"
    #params["limit"] = "10"
    return params

def get_results():
    
    la = 42.39
    lo = -72.52
    data = yelp_api.search_query(longitude=lo,latitude=la, sort_by = 'review_count', limit = 20, term = 'restaurant')
    add_to_db(data)
    return data

def add_to_db(results):
    for business in results["businesses"]:
        create_restaurant(business)

clear_restaurants()
get_results()

if __name__ == '__main__':
    app.run(debug=False)

