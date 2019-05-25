from flask import render_template
from flask import Flask
from models import Stores
from flask import request, session
import pandas as pd
from flask_session import Session


#import os

app = Flask(__name__)

SESSION_TYPE = 'redis'
app.config.from_object(__name__)
Session(app)

@app.route('/')
def get_stores():
    stores = Stores().get_stores_from_json()
    session['data'] = stores.to_json()
    return render_template('stores.html', stores=[stores.to_html(classes='store')])

@app.route('/stores_in_radius')
def get_tores_in_radius():
    radius = request.args.get('radius')
    store_name = request.args.get('store_name')
    #stores = Stores().getStoresFromJson()
    stores_json = pd.io.json.read_json(session.get('data', 'not set'))
    stores = pd.DataFrame(stores_json)
    stores = stores[['name', 'postcode', 'latitude', 'longitude']]
    print("stores from session")
    print(stores)
    stores_in_radius = Stores().get_stores_in_radius(radius,store_name,stores)
    return render_template('stores.html', stores=[stores_in_radius.to_html(classes='store')])

if __name__ == '__main__':
    #app.secret_key = os.urandom(24)
    app.run(debug=True)
