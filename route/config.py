
class Config:
    SECRET_KEY = '91967abbb5fec4870c12b9cb0a8afbd9'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123456@localhost/pointage'

class Default:
    DAYS = ["LUNDI", "MARDI", "MERCREDI", "JEUDI", "VENDREDI", "SAMEDI", "DIMANCHE"]
    TAUX_INDEMNITE = 0.3