import sqlalchemy
from .db_session import SqlAlchemyBase


class Korzina(SqlAlchemyBase):
    __tablename__ = 'korzina'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('users.id'))
    tovar_id = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey('tovars.id'))
    amount = sqlalchemy.Column(sqlalchemy.Integer)
