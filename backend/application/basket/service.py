from sqlalchemy import and_

from application import db
from application.models import Order, OrderProduct, CardProduct


def get_order_products(current_user):
    order_products = db.session.query(Order.order_id,
                                      Order.user_id,
                                      OrderProduct.card_id,
                                      OrderProduct.amount,
                                      CardProduct.name,
                                      CardProduct.image,
                                      OrderProduct.price).join(OrderProduct,
                                                               Order.order_id == OrderProduct.order_id).join(
        CardProduct, OrderProduct.card_id == CardProduct.card_id, isouter=True).where(and_(
        Order.user_id == current_user.user_id, Order.status == 'basket')).all()
    return order_products


def get_card_product(card_id):
    card = CardProduct.query.filter_by(card_id=card_id).first()
    return card


def get_basket(user_id):
    basket = Order.query.filter_by(user_id=user_id, status='basket').first()
    return basket


def create_basket(user_id):
    basket = Order(user_id=user_id)
    db.session.add(basket)
    db.session.commit()


def get_order_product(order_id, card_id):
    order_product = OrderProduct.query.filter_by(order_id=order_id, card_id=card_id).first()
    return order_product
