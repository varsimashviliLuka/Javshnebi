from src.extensions import api
from flask_restx import fields

auth_ns = api.namespace('Authentification', description='API მომხმარებლის აუტენტიფიკაციის შესახებ', path='/api')

auth_model = api.model('Authentication', {
    'email': fields.String(required=True, description='შეიყვანეთ თქვენი მეილი', example='luka.varsimashvili@iliauni.edu.ge'),
    'password': fields.String(required=True, description='შეიყვანეთ პაროლი', example='LUKAluka123')
})

registration_model = api.model('Registration', {
    'email': fields.String(required=True, description='შეიყვანეთ თქვენი მეილი', example='luka.varsimashvili@iliauni.edu.ge'),
    'password': fields.String(required=True, description='შეიყვანეთ პაროლი', example='LUKAluka123'),
    'password_repeat': fields.String(required=True, description='გაიმეორეთ პაროლი', example='LUKAluka123')
})