from flask import Blueprint, render_template
from . import db
import sys

views = Blueprint('views', __name__)
items = ['Oreo Original', "Lay's Classic", 'Camel Roasted Peanuts', 'Lindor Milk', 'Ruffles Original', 'Anchor Strong Beer']

class Item:
    def __init__(self, name, ntuc, store):
        self.name = name
        self.ntuc = price
        self.store = store
        
@views.route('/')
def homepage():
    # Retrieve all products from database
    from .model import Products
    products = Products.query.all()
    total_per_store = {}
    cost_per_item = {}
    store_names = []
    item_range = len(items)
    
    
    for i in range(6):
        cost_per_item[items[i]] = []
        
        for product in products:
            
            if product.productID == i:
                cost_per_item[items[i]].append(product.price)
                
                if product.store not in store_names:
                    store_names.append(product.store)
                    
                if product.store in total_per_store: 
                    total_per_store[product.store] += product.price
                else:
                    total_per_store[product.store] = product.price
    
    # Compare total prices
    
            
    print(cost_per_item, file=sys.stderr)
    print(store_names, file=sys.stderr)
    print(total_per_store, file=sys.stderr)
            
    return render_template('index.html', cost_per_item=cost_per_item, store_names=store_names, total_per_store=total_per_store)
