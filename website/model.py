from . import db

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    productName = db.Column(db.String(50))
    store = db.Column(db.String(50))
    price = db.Column(db.Float)
    productID = db.Column(db.Integer)

    def __repr__(self):
        return f"Products('{self.productName}', '{self.store}', '{self.price}', '{self.productID}')"