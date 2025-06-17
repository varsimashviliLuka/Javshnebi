from flask_restx import Resource
from flask import request

from collections import defaultdict
from datetime import datetime

from src.api.nsmodels import filter_ns, filter_model, get_data_model
from src.extensions import Agency

from src.models import DynamicTable, Category, Center

@filter_ns.route('/filter')
class FilterApi(Resource):
    @filter_ns.expect(filter_model)
    def post(self):
        ''' მონაცემების გაფილტვრა '''

        data = request.get_json()

        category_id = data.get('category_id')
        center_id = data.get('center_id')

        data = DynamicTable.query.filter_by(official_center_id=center_id,official_category_id=category_id).first()

        availability = data.availability

        return {"available_slots": availability}
    
    def get(self):
        ''' ყველა შესაძლო ჯავშნის ნახვა (optimized for main page) '''
        
        grouped = defaultdict(lambda: {'automatic': None, 'manual': None})

        data = DynamicTable.query.all()

        for record in data:
            center = Center.query.filter_by(official_center_id=record.official_center_id).first()
            category = Category.query.filter_by(official_category_id=record.official_category_id).first()
            
            if not center or not category:
                continue

            city = center.name_english
            category_name = category.name_english.lower()
            
            # Sort dates
            valid_dates = [a['bookingDate'] for a in record.availability if a.get('bookingDateStatus') == 1]
            valid_dates = sorted(valid_dates, key=lambda d: datetime.strptime(d, "%d-%m-%Y"))

            if valid_dates:
                grouped[city][category_name] = {
                    'category': category_name,
                    'earliest_date': valid_dates[0],
                    'all_dates': valid_dates
                }

        final_response = []

        for city, slots in grouped.items():
            if slots['automatic']:
                final_response.append({'city': city, **slots['automatic']})
            elif slots['manual']:
                final_response.append({'city': city, **slots['manual']})
        return final_response, 200


    




        

    