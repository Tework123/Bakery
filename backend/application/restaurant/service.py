import sqlalchemy
from sqlalchemy import cast, or_

from application import db
from application.models import CardProduct, Order, OrderProduct


def get_all_cards_product():
    cards = CardProduct.query.all()
    return cards


def add_card_product(name, price, image):
    card = CardProduct(name=name, price=price, image=image.filename)
    db.session.add(card)
    db.session.flush()


def get_card_product(card_id):
    card = CardProduct.query.filter_by(card_id=card_id).first()
    return card


def delete_card_product(card_id):
    CardProduct.query.filter_by(card_id=card_id).delete()
    db.session.commit()


def get_pass_orders():
    pass_orders = (db.session.query(Order.order_id,
                                    Order.text,
                                    Order.address,
                                    Order.date,
                                    Order.status,
                                    db.func.sum(OrderProduct.price).label('price'),
                                    db.func.string_agg(CardProduct.name, ', ').label('name'),
                                    db.func.string_agg(cast(OrderProduct.amount, sqlalchemy.String), ', ')
                                    .label('amount'))
                   .join(OrderProduct, Order.order_id == OrderProduct.order_id)
                   .join(CardProduct, OrderProduct.card_id == CardProduct.card_id)
                   .group_by(Order.order_id,
                             Order.text,
                             Order.date).where(or_(Order.status == 'paid',
                                                   Order.status == 'prepared',
                                                   Order.status == 'ready',
                                                   Order.status == 'canceled_restaurant',
                                                   Order.status == 'delivered',
                                                   Order.status == 'success',
                                                   Order.status == 'canceled_delivery',
                                                   ))).order_by(Order.date.desc()).all()
    return pass_orders


def get_current_orders():
    current_orders = (db.session.query(Order.order_id,
                                       Order.text,
                                       Order.address,
                                       Order.date,
                                       Order.status,
                                       db.func.sum(OrderProduct.price).label('price'),
                                       db.func.string_agg(CardProduct.name, ', ').label('name'),
                                       db.func.string_agg(cast(OrderProduct.amount, sqlalchemy.String), ', ')
                                       .label('amount')).
                      join(OrderProduct, Order.order_id == OrderProduct.order_id)
                      .join(CardProduct, OrderProduct.card_id == CardProduct.card_id)
                      .group_by(Order.order_id,
                                Order.text,
                                Order.date).where(or_(Order.status == 'paid',
                                                      Order.status == 'prepared',
                                                      Order.status == 'ready',
                                                      Order.status == 'canceled_restaurant',
                                                      Order.status == 'delivered',
                                                      Order.status == 'canceled_delivery',
                                                      )).order_by(Order.date.desc()).all())
    return current_orders
