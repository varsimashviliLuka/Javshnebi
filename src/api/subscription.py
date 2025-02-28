from flask_restx import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.api.nsmodels import subscription_ns, create_subscription_model, view_subscription_model
from src.models import User, Subscription, Category, Center

@subscription_ns.route('/subscription')
class SubscriptionApi(Resource):
    @jwt_required()
    @subscription_ns.doc(security='JsonWebToken')
    @subscription_ns.expect(create_subscription_model)
    def post(self):
        ''' გამოწერის შექმნა '''
        data = request.get_json()
        user = User.query.filter_by(uuid=get_jwt_identity()).first()
        
        category_id = data.get('category_id')
        center_id = data.get('center_id')


        if not user:
            return {'error': 'მომხმარებელი არ მოიძებნა'}, 400
        
        if not user.verified:
            return {'error': 'გთხოვთ გაიაროთ ვერიფიკაცია'}, 400
        
        if len(user.subscriptions) >= 1:
            subscription = Subscription.query.filter_by(user_id=user.id).first()
            subscription.category_id = category_id
            subscription.center_id = center_id
            subscription.save()
            return {'message': 'თქვენი პარამეტრები წარმატებით განახლდა'}, 200
        else:
            subscription = Subscription(user_id=user.id,
                                        category_id=category_id,
                                        center_id=center_id)
            subscription.create()

            return {'message': 'თქვენი პარამეტრები წარმატებით შეიქმნა'}, 200
        
    @jwt_required()
    @subscription_ns.doc(security='JsonWebToken')
    @subscription_ns.marshal_with(view_subscription_model)
    def get(self):
        ''' საკუთარი გამოწერები '''

        user = User.query.filter_by(uuid=get_jwt_identity()).first()
        if not user:
            return {'error': 'მომხმარებელი არ მოიძებნა'}, 400
        
        result = []
        for subscription in user.subscriptions:
            category = Category.query.filter_by(id=subscription.category_id).first()
            if not category:
                return {'error': 'კატეგორია არ მოიძებნა'}, 400
            center = Center.query.filter_by(id=subscription.center_id).first()
            if not center:
                return {'error': 'ქალაქი არ მოიძებნა'}, 400

            model = {
                'subscription_id': subscription.id,
                'category_id': subscription.category_id,
                'center_id': subscription.center_id,

                'category_name_georgian': category.name_georgian,
                'category_name_english': category.name_english,

                'center_name_georgian': center.name_georgian,
                'center_name_english': center.name_english,

                'created_at': subscription.created_at,
                'email_sent_at': subscription.email_sent_at,
            }

            result.append(model)
        print(result)
        return result, 200


        
@subscription_ns.route('/subscription/<int:subscription_id>')
class SubscriptionDeleteApi(Resource):
    @jwt_required()
    @subscription_ns.doc(security='JsonWebToken')
    def delete(self,subscription_id):
        ''' გამოწერის წაშლა '''

        user = User.query.filter_by(uuid=get_jwt_identity()).first()
        if not user:
            return {'error': 'მომხმარებელი არ მოიძებნა'}, 400
        
        subscription = Subscription.query.filter_by(id=subscription_id).first()
        if not subscription:
            return {'error': 'გამოწერა ვერ მოიძებნა'}, 400
        
        if subscription.user_id == user.id:
            subscription.delete()
            return {'message': 'გამოწერა წარმატებით გაუქმდა'}, 200
        
        return {'error': 'თქვენ არ გაქვთ subscription ის წაშლის უფლება'}, 403
