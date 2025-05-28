from src.extensions import db


class BaseModel():

    def create(self, commit=True):
        db.session.add(self)
        if commit:
            self.save()
        else:
            db.session.flush()

    def save(self):  # ← remove @staticmethod
        db.session.add(self)  # ← ensure self is added (important for update tracking)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        self.save()