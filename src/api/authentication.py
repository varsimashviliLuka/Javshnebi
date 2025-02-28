from flask_restx import Resource
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from itsdangerous import BadSignature, SignatureExpired

from src.models import User, Role
from src.api.nsmodels import auth_ns,auth_model, registration_model
from src.extensions import url_serializer, mail




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



@auth_ns.route('/registration')
@auth_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Forbidden', 404: 'Not Found'})
class RegistrationApi(Resource):
    @auth_ns.expect(registration_model)
    def post(self):
        ''' რეგისტრაცია '''

        data = request.get_json()

        user = User.query.filter_by(email=data.get('email')).first()

        if user:
            if user.verified:
                return {'error': 'მითითებული მეილი უკვე დარეგისტრირებულია'}, 400
        
        if data.get('password') != data.get('password_repeat'):
            return {'error': 'პაროლები ერთმანეთს არ ემთხვევა'}, 400

        if not user:
            user_role = Role.query.filter_by(name='User').first()
            new_user = User(email=data.get('email'),
                            password=data.get('password'),
                            verified=False,
                            role=user_role)
            new_user.create()
        
        token = url_serializer.dumps(data.get('email'), salt='email-confirm')

        verification_url = f'{request.url_root}api/verify/{token}'

        subject = "Verify Your Email"
        message = f"Click the link to verify your email: {verification_url}"

        email = data.get('email')
        try:
            status = mail.send_mail(emails=[email], subject=subject, message=message)

            if not status:
                return{'error': 'ელ.ფოსტის გაგზავნის დროს დაფიქსირდა შეცდომა'}, 400
            
            return {'message': 'გთხოვთ შეამოწმოთ ელ.ფოსტა, ვერიფიკაციის კოდი გამოგზავნილია'}, 200
        
        except Exception as err:
            return {'error': f'ელ.ფოსტის გაგზავნის დროს დაფიქსირდა შეცდომა: {err}'}, 400
        


@auth_ns.route('/verify/<string:token>')
@auth_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Forbidden', 404: 'Not Found'})
class VerifyEmailApi(Resource):
    def get(self, token):
        ''' მეილის ვერიფიკაცია '''

        try:
            email = url_serializer.loads(token, salt='email-confirm', max_age=3600)
        except SignatureExpired:
            email = "expired"
        except BadSignature:
            email = "invalid"
            

        if email == "expired":
            return {'error': 'მოცემულ ტოკენს გაუვიდა ვადა, გთხოვთ სცადოთ თავიდან'}, 400
        elif email == "invalid":
            return {'error': 'არასწორი ტოკენი, სცადეთ თავიდან'}, 400
        
        user = User.query.filter_by(email=email).first()

        if not user:
            return {'error': 'მითითებული ელ.ფოსტა არ არსებობს'}, 400
        
        if user.verified:
            return {'error': 'თქვენ უკვე ვერიფიცირებული ხართ!'}, 400

        user.verified = True
        user.save()
        return {'message': 'თქვენ წარმატებით გაიარეთ ვერიფიკაცია'}, 200
        

        
        
        
