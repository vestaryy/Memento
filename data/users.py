import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    tg_id = sqlalchemy.Column(sqlalchemy.BigInteger, unique=True, index=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    
    content = orm.relationship("Content", back_populates='user')