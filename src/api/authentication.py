from flask_restx import Resource
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from src.models import User, Role
from src.api.nsmodels import auth_ns,auth_model




@auth_ns.route('/login')
@auth_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Forbidden', 404: 'Not Found'})
class AuthorizationApi(Resource):
    @auth_ns.expect(auth_model)
    def post(self):
        ''' სისტემაში შესვლა '''

        data = request.get_json()

        user = User.query.filter_by(email=data.get('email')).first()
        if not user:
            return {'error': 'შეყვანილი პაროლი ან ელ.ფოსტა არასწორია'}, 400
        
        if not user.check_password(data.get('password')):
            return {'error': 'შეყვანილი პაროლი ან ელ.ფოსტა არასწორია'}, 400
        
        access_token = create_access_token(identity=user.uuid)
        refresh_token = create_refresh_token(identity=user.uuid)

        return {"message": "წარმატებით გაიარეთ ავტორიზაცია",
                "access_token": access_token,
                "refresh_token": refresh_token}, 200



@auth_ns.route('/refresh')
@auth_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Forbidden', 404: 'Not Found'})
class AccessTokenRefreshApi(Resource):
    @jwt_required(refresh=True)
    @auth_ns.doc(security='JsonWebToken')
    def post(self):
        ''' JWT ტოკენის დარეფრეშება '''

        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        response = {
            "access_token": access_token
        }

        return response
