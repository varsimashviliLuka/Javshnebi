from src.extensions import db
from src.models.base import BaseModel
from sqlalchemy.dialects.mysql import JSON

class DynamicTable(db.Model,BaseModel):
    __tablename__ = 'dynamicTable'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    official_center_id = db.Column(db.Integer, nullable=False)
    official_category_id = db.Column(db.Integer, nullable=False)

    availability = db.Column(JSON)

    def __repr__(self):
        return f'<DynamicTable: id={self.id}>'

