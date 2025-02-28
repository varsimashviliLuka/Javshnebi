from src.extensions import db
from src.models.base import BaseModel
from datetime import datetime

class Subscription(db.Model, BaseModel):
    __tablename__ = 'subscriptions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    center_id = db.Column(db.Integer, db.ForeignKey('centers.id'), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    email_sent_at = db.Column(db.DateTime, default=None, nullable=True)


    def __repr__(self):
        return f'<Subscription(id={self.id}, user_id={self.user_id} ,center_id={self.center_id})>'