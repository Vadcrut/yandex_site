import sqlalchemy
from .db_session import SqlAlchemyBase

association_table = sqlalchemy.Table(
    'association',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('orders', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('orders.id')),
    sqlalchemy.Column('tovars', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('tovars.id'))
)


class Tovars(SqlAlchemyBase):
    __tablename__ = 'tovars'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    price = sqlalchemy.Column(sqlalchemy.Integer, default=1)
    amount_rest = sqlalchemy.Column(sqlalchemy.Integer, default=1)
