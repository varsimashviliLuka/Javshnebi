from flask_restx import Resource
from flask import request

from src.api.nsmodels import filter_ns, filter_model
from src.extensions import Agency

@filter_ns.route('/filter')
class FilterApi(Resource):
    @filter_ns.expect(filter_model)
    def post(self):
        ''' მონაცემების გაფილტვრა '''

        data = request.get_json()

        category_id = data.get('category_id')
        center_id = data.get('center_id')

        agency = Agency(city_id=center_id,transmition_id=category_id)

        availability = agency.check_availability()

        return {"bookable_slots": availability}



        

    