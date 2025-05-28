# subscriptions.py
from src.extensions import db
from src.models.base import BaseModel
from datetime import datetime

class Subscription(db.Model, BaseModel):
    __tablename__ = 'subscriptions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Foreign key fields
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    center_id = db.Column(db.Integer, db.ForeignKey('centers.id'), nullable=False)

    active = db.Column(db.Boolean, nullable=False, default=True)

    # Relationships to access full objects
    user = db.relationship('User', back_populates='subscriptions', lazy='joined')
    category = db.relationship('Category', back_populates='subscriptions', lazy='joined')
    center = db.relationship('Center', back_populates='subscriptions', lazy='joined')

    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    email_sent_at = db.Column(db.DateTime, default=None, nullable=True)

    def __repr__(self):
        return f'<Subscription(id={self.id}, user_id={self.user_id}, category_id={self.category_id}, center_id={self.center_id})>'
