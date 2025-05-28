from src.extensions import api
from flask_restx import fields

filter_ns = api.namespace('Filter API', description='API დინამიურად ცვლადი მონაცემების შესახებ', path='/api')

filter_model = api.model('Filter', {
    'category_id': fields.Integer(required=True, description='კატეგორიის id', example=4),
    'center_id': fields.Integer(required=True,description='ცენტრის id', example=2)
})

get_data_model = api.model('Get_Data', {
    'id': fields.Integer(readOnly=True, description='ID'),
    'center_name_english': fields.String(required=True,description='სახელი ცენტრის'),
    'category_name_english': fields.String(required=True,description='სახელი კატეგორიის'),
    'availability': fields.Raw(description='Availability JSON data')
})