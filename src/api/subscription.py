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
        active = data.get('active')


        # Validate category
        category = Category.query.filter_by(official_category_id=category_id).first()
        if not category:
            return {'error': 'Invalid Category'}, 400

        # Validate center
        center = Center.query.filter_by(official_center_id=center_id).first()
        if not center:
            return {'error': 'Invalid City'}, 400

        if not user:
            return {'error': 'Invalid User'}, 400
        
        if not user.verified:
            return {'error': 'User is Not Verified'}, 400
        
        if len(user.subscriptions) >= 1:
            subscription = Subscription.query.filter_by(user_id=user.id).first()
            subscription.category = category
            subscription.center = center
            subscription.active = active
            print()
            subscription.save()
            return {'message': 'Subscription Updated Successfully'}, 200
        else:
            subscription = Subscription(user=user,
                                        category=category,
                                        center=center,
                                        active=active)
            subscription.create()

            return {'message': 'Subscription Created Successfully'}, 200
        
    @jwt_required()
    @subscription_ns.doc(security='JsonWebToken')
    @subscription_ns.marshal_with(view_subscription_model)
    def get(self):
        ''' საკუთარი გამოწერები '''

        user = User.query.filter_by(uuid=get_jwt_identity()).first()
        if not user:
            return {'error': 'Invalid User'}, 400
        
        result = []
        for subscription in user.subscriptions:
            category = Category.query.filter_by(id=subscription.category_id).first()
            if not category:
                return {'error': 'Invalid Category'}, 400
            center = Center.query.filter_by(id=subscription.center_id).first()
            if not center:
                return {'error': 'Invalid City'}, 400

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
                'active': subscription.active
            }

            result.append(model)
        return result, 200


        
@subscription_ns.route('/subscription/<int:subscription_id>')
class SubscriptionDeleteApi(Resource):
    @jwt_required()
    @subscription_ns.doc(security='JsonWebToken')
    def delete(self,subscription_id):
        ''' გამოწერის წაშლა '''

        user = User.query.filter_by(uuid=get_jwt_identity()).first()
        if not user:
            return {'error': 'Invalid User'}, 400
        
        subscription = Subscription.query.filter_by(id=subscription_id).first()
        if not subscription:
            return {'error': 'Invalid Subscription'}, 400
        
        if subscription.user_id == user.id:
            subscription.delete()
            return {'message': 'Subscription Deleted Successfully'}, 200
        
        return {'error': 'You do not have permission to delete Subscription'}, 403
    
    @jwt_required()
    @subscription_ns.doc(security='JsonWebToken')
    def patch(self,subscription_id):
        ''' გამოწერის დეაქტივაცია/აქტივაცია '''

        user = User.query.filter_by(uuid=get_jwt_identity()).first()
        if not user:
            return {'error': 'Invalid User'}, 400
        
        subscription = Subscription.query.filter_by(id=subscription_id).first()
        if not subscription:
            return {'error': 'Invalid Subscription'}, 400
        
        if subscription.user_id == user.id:
            if subscription.active:
                subscription.active = False
            else:
                subscription.active = True
            subscription.save()
            
            return {'message': 'Subscription Edited Successfully'}, 200
        
        return {'error': 'You do not have permission to edit Subscription'}, 403
