from src.extensions import api
from flask_restx import fields

filter_ns = api.namespace('Filter API', description='API დინამიურად ცვლადი მონაცემების შესახებ', path='/api')

filter_model = api.model('Filter', {
    'category_id': fields.Integer(required=True, description='კატეგორიის id', example=4),
    'center_id': fields.Integer(required=True,description='ცენტრის id', example=2)
})