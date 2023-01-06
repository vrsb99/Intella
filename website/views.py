from flask import Blueprint, render_template, request, redirect
from . import db
import sys

views = Blueprint('views', __name__)
images = ['https://media.nedigital.sg/fairprice/fpol/media/images/product/L/13012296_L1_20220706.jpg?q=60','https://media.nedigital.sg/fairprice/fpol/media/images/product/L/13218718_L1_20221228.jpg?q=60'
          , 'https://media.nedigital.sg/fairprice/fpol/media/images/product/L/13010730_L1_20221021.jpg?q=60', 'https://media.nedigital.sg/fairprice/fpol/media/images/product/L/12006645_L1_20220920.jpg?q=60',
          'https://media.nedigital.sg/fairprice/fpol/media/images/product/L/11880752_L1_20221211.jpg?q=60', 'https://media.nedigital.sg/fairprice/fpol/media/images/product/L/13018295_L1_20220427.jpg?q=60']
        
@views.route('/', methods=['GET', 'POST'])
def homepage():
    # Retrieve all products from database
    from .model import Prices, Stores, Products
    products = Products.query.all()
    stores = Stores.query.all()
    prices = Prices.query.all()
    items = []
    shops = []
    totals = []
    cost_per_item = {}
    
    if request.method == 'POST':
        number_of_products = request.form.get('number_of_products')
        
        if not number_of_products:
            return redirect('/')
        
        products = products[:int(number_of_products)+1]
        
    # Obtain list of all items
    for product in products:
        items.append(product.product_name)
        
    # Obtain list of all shops
    for store in stores:
        shops.append(store.store_name)
        
    # Obtain total prices for each shop
    for idx,shop in enumerate(shops):
        total = 0
        counter = 0
        length  = len(items)
        
        for price in prices:
            if price.store_id == idx and price.product_id < length:
                total += price.price 
                counter += 1

        if counter == length:
            totals.append(total)

    recommended = min(totals) 
    not_recommended = max(totals)
        
    # Cost per Item
    for idx,item in enumerate(items):
        cost_per_item[item] = []
        
        for price in prices:
            
            if price.product_id == idx:
                cost_per_item[item].append(price.price)
            
    return render_template('index.html', items=items, store_names=shops, total_per_store=totals, images=images, cost_per_item=cost_per_item, recommended=recommended, not_recommended=not_recommended)
