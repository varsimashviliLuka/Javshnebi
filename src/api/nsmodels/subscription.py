from src.extensions import api
from flask_restx import fields

subscription_ns = api.namespace('Subscription', description='API გამოწერების შესახებ', path='/api')

create_subscription_model = api.model('SubscriptionCreate',{
    'category_id': fields.Integer(required=True, description='შეიყვანეთ გადაცემათა კოლოფის კოდი (3 მექანიკა, 4 ავტომატიკა)', example=3),
    'center_id': fields.Integer(required=True, description='შეიყვანეთ ქალაქის კოდი', example=15),
})

view_subscription_model = api.model('SubscriptionView',{
    'subscription_id': fields.Integer(required=True, description='subscription id', example=3),
    'category_id': fields.Integer(required=True, description='შეიყვანეთ გადაცემათა კოლოფის კოდი (3 მექანიკა, 4 ავტომატიკა)', example=3),
    'center_id': fields.Integer(required=True, description='შეიყვანეთ ქალაქის კოდი', example=15),

    'category_name_georgian': fields.String(required=True, description='კატეგორიის დასახელება ქართულად', example='მექანიკა'),
    'category_name_english': fields.String(required=True, description='კატეგორიის დასახელება ინგლისურად', example='Manual'),
    'center_name_georgian': fields.String(required=True, description='ქალაქის დასახელება ქართულად', example='რუსთავი'),
    'center_name_english': fields.String(required=True, description='ქალაქის დასახელება ინგლისურად', example='Rustavi'),

    'created_at': fields.DateTime(required=True, description='გამოწერის შექმნის თარიღი'),
    'email_sent_at': fields.DateTime(description='ბოლოს გაგზავნილი მეილის თარიღი')
})

