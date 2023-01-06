from . import db

class Prices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    price = db.Column(db.Float)

    def __repr__(self):
        return f"Prices('{self.product_id}', '{self.store_id}', '{self.price}')"
    
class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f"Products('{self.product_name}')"
    
class Stores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    store_name = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f"Stores('{self.store_name}')"