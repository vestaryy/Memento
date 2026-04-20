import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

class Content(SqlAlchemyBase):
    __tablename__ = 'content'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    yandex_path = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    
    cached_url = sqlalchemy.Column(sqlalchemy.Text, nullable=True)  
    url_expires = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)

    
    user = orm.relationship('User', back_populates='content') 
    
    def has_valid_cache(self):
        if not self.cached_url or not self.url_expires:
            return False
        return datetime.datetime.now() < (self.url_expires - datetime.timedelta(minutes=2))
