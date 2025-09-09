import requests
import inspect
from datetime import datetime

from src import db
from src.models import DynamicTable
from src.logger import get_logger
from src.extensions import mail

from Utils.sendable_subscriptions import get_sendable_subscriptions

city_ids = [2,3,4,5,6,7,8,9,10,15]
transmition_ids = [3,4]

logger = get_logger("update_availability")

def update_availability():
    function_name = inspect.currentframe().f_code.co_name
    try:
        from flask import current_app  # Import here to avoid circular issues
        with current_app.app_context():
            subscriptions = get_sendable_subscriptions()
            for city_id in city_ids:
                for transmition_id in transmition_ids:
                    API_LINK = f"https://api-my.sa.gov.ge/api/v1/DrivingLicensePracticalExams2/DrivingLicenseExamsDates2?CategoryCode={transmition_id}&CenterId={city_id}"

                    response = requests.get(API_LINK)

                    if not response.ok:
                        logger.error(f'While sending request to {API_LINK}: status_code: {response.status_code}, text: {response.text}. FUNCTION: {function_name}')
                    else:
                        data = response.json()
                        for subscription in subscriptions:
                            if subscription.category.official_category_id == transmition_id and subscription.center.official_center_id == city_id:
                                if len(data) > 1:
                                    email = subscription.user.email

                                    subject = 'ქალაქის ჯავშანი გახსნილია!\n\nThe city booking is now open!'
                                    message = 'მოგესალმებით, გაცნობებთ, რომ მართვის მოწმობის ქალაქის ჯავშანი გახსნილია, ეწვიეთ მომსახურეობის სააგენტოს საიტს დასაჯავშნად. საიტის ბმული: https://my.sa.gov.ge/drivinglicenses/practicalexam\n\nHello, we inform you that the booking for the city driving license exam is now open. Please visit the Service Agency website to make a reservation. Website link: https://my.sa.gov.ge/drivinglicenses/practicalexam'
                                    status = mail.send_mail(emails=[email], subject=subject, message=message)
                                    if not status:
                                        logger.error(f'error while sending email to: {email}')
                                    else:
                                        subscription.email_sent_at = datetime.now()
                                        subscription.save()
                                        logger.info(f'email sent to: {email}')

                        # Database Population
                        dynamic_data = DynamicTable.query.filter_by(official_center_id=city_id,official_category_id=transmition_id).first()
                        dynamic_data.availability = data
                        dynamic_data.save()
                        logger.info(f'Successfully added data to dynamic table. FUNCTION: {function_name}')

        logger.info(f'Done executing. FUNCTION: {function_name}')

    except:

        logger.error(f'Job failed going to exception. FUNCTION: {function_name}')
