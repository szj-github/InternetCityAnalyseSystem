from app import db
class Info(db.Model):
    __tablename__ = 'infos'
    position = db.Column(db.String(100),primary_key=True)
    money = db.Column(db.String(100))
    city = db.Column(db.String(100))
    company = db.Column(db.String(100))
    company_size = db.Column(db.Text)
    detail = db.Column(db.Text)