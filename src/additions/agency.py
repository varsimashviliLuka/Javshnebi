import requests

class Agency:
    def __init__(self,city_id,transmition_id):
        self.city_id = city_id
        self.transmition_id = transmition_id
        self.agency_link = f"https://api-my.sa.gov.ge/api/v1/DrivingLicensePracticalExams2/DrivingLicenseExamsDates2?CategoryCode={self.transmition_id}&CenterId={self.city_id}"

    def check_availability(self):
        response = requests.get(self.agency_link)
        if not response.ok:
            return {'error': 'დაფიქსირდა შეცდომა მონაცემების წამოღების დროს'}
        else:
            final = response.json()
            return final
        