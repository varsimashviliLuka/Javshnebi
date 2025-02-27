from src.extensions import db
from src.models.base import BaseModel

class Center(db.Model,BaseModel):
    __tablename__ = 'centre'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    official_center_id = db.Column(db.Integer, nullable=False)
    name_georgian = db.Column(db.String(50), nullable=False)
    name_english = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Center(id={self.id}, official_center_id={self.official_center_id}, name_english={self.name_english})>'

