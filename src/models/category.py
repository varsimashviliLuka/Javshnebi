from src.extensions import db
from src.models.base import BaseModel

class Category(db.Model, BaseModel):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    official_category_id = db.Column(db.Integer, nullable=False)
    name_georgian = db.Column(db.String(50), nullable=False)
    name_english = db.Column(db.String(50), nullable=False)

    subscriptions = db.relationship('Subscription', backref='categories', lazy=True)

    def __repr__(self):
        return f'<Category(id={self.id}, official_category_id={self.official_category_id} ,name_english={self.name_english})>'