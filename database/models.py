from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    price = db.Column(db.Float)
    size = db.Column(db.String(50))
    brand = db.Column(db.String(100))
    description = db.Column(db.Text)
    image_url = db.Column(db.Text)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "size": self.size,
            "brand": self.brand,
            "description": self.description,
            "image_url": self.image_url
        }
