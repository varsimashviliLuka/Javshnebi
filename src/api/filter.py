from flask_restx import Resource
from flask import request

from flask_jwt_extended import jwt_required

from src.api.nsmodels import filter_ns, filter_model, get_data_model
from src.extensions import Agency

from src.models import DynamicTable, Category, Center

@filter_ns.route('/filter')
class FilterApi(Resource):
    @jwt_required()
    @filter_ns.doc(security='JsonWebToken')
    @filter_ns.expect(filter_model)
    def post(self):
        ''' მონაცემების გაფილტვრა '''

        data = request.get_json()

        category_id = data.get('category_id')
        center_id = data.get('center_id')

        agency = Agency(city_id=center_id,transmition_id=category_id)

        availability = agency.check_availability()

        return {"bookable_slots": availability}
    
    @jwt_required()
    @filter_ns.doc(security='JsonWebToken')
    @filter_ns.marshal_with(get_data_model)
    def get(self):
        ''' ყველა შესაძლო ჯავშნის ნახვა '''

        available_slots = []
        data = DynamicTable.query.all()
        for i in data:
            result = {
                'id': i.id,
                'center_name_english': Center.query.filter_by(official_center_id=i.official_center_id).first().name_english,
                'category_name_english': Category.query.filter_by(official_category_id=i.official_category_id).first().name_english,
                'availability': i.availability
            }
            available_slots.append(result)
        return available_slots, 200


    




        

    