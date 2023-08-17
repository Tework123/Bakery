import sqlalchemy
from sqlalchemy import cast, and_

from application import db
from application.models import User, Order, OrderProduct, CardProduct


def get_user(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    return user


def get_orders(user_id):
    orders = (db.session.query(Order.order_id,
                               Order.text,
                               Order.date,
                               Order.status,
                               db.func.sum(OrderProduct.price).label('price'),
                               db.func.string_agg(CardProduct.name, ', ').label('name'),
                               db.func.string_agg(cast(OrderProduct.amount, sqlalchemy.String), ', ')
                               .label('amount'),
                               db.func.string_agg(cast(CardProduct.image, sqlalchemy.String), ', ')
                               .label('image')).
              join(OrderProduct, Order.order_id == OrderProduct.order_id)
              .join(CardProduct, OrderProduct.card_id == CardProduct.card_id)
              .group_by(Order.order_id,
                        Order.text,
                        Order.date)
              .where(and_(Order.user_id == user_id, Order.status != 'basket')).order_by(
        Order.date.desc()).all())
    return orders