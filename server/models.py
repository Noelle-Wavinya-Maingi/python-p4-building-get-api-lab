from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Bakery(db.Model, SerializerMixin):
    __tablename__ = 'bakeries'

    serialize_rule = ('-bakedgoods.bakery',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    def __repr__(self):
        return f'{self.name} {self.created_at} {self.updated_at}'
class BakedGood(db.Model, SerializerMixin):
    __tablename__ = 'baked_goods'

    serialize_rule = ('-bakery.bakedgoods',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())
    bakery_id = db.Column(db.Integer, db.ForeignKey('bakeries.id'))

    bakery = db.relationship('Bakery', backref = 'bakedgoods')

    def __repr__(self):
        return f'{self.name} {self.price} {self.created_at} {self.updated_at}'

    