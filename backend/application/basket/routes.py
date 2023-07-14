import datetime
import json

from flask import jsonify
from flask_login import login_user, current_user

from application import db
from application.auth.auth import login_required
from application.basket import api_basket
from application.basket.fields_validation import basket_data, basket_data_delete
from application.cards import api_cards
from application.email.email import send_email
from application.models import User, CardProduct, Order, OrderProduct
from flask_restful import Resource, marshal_with, fields

from start_app import CONFIG


class Index(Resource):
    card_fields = {
        'order_id': fields.Integer,
        'user_id': fields.Integer,
        'card_id': fields.Integer,
        'amount': fields.Integer,
        'card_name': fields.String,
        'card_image': fields.String,
        'card_price': fields.Price
    }

    @login_required(current_user)
    @marshal_with(card_fields)
    def get(self):
        subject = 'Bakery email'
        body = 'Bakery HERE?'
        # x = 1 / 0


        # send_email(subject, CONFIG.MAIL_USERNAME, [current_user.email], body)

        basket = db.session.query(Order.order_id, Order.user_id, OrderProduct.card_id, OrderProduct.amount,
                                  CardProduct.card_name,
                                  CardProduct.card_image,
                                  (CardProduct.card_price * OrderProduct.amount).label("card_price")).join(OrderProduct,
                                                                                                           Order.order_id == OrderProduct.order_id).join(
            CardProduct, OrderProduct.card_id == CardProduct.card_id).where(
            Order.user_id == current_user.user_id, Order.status == False).all()

        # может быть еще какие-то данные вернуть, и картинки вставить
        return basket

    @login_required(current_user)
    def patch(self):
        # наверное нужно передавать с фронта какой-то знак, что пользователь нажал на - или на +
        # и уже тут с if провернуть операции, все таки это тоже patch

        # кнопка добавить в корзину на карточке товара и значок + около этого товара в корзине
        data = basket_data.parse_args()
        basket = Order.query.filter_by(user_id=current_user.user_id, status=False).first()
        if basket is None:
            response = jsonify({'data': f'У вас нет корзины'})
            response.status_code = 200
            return response
        card = OrderProduct.query.filter_by(order_id=basket.order_id, card_id=data['card_id']).first()

        # если такой товар уже есть в корзине, то нужно увеличить его amount на один
        if card:
            card.amount += 1
            db.session.commit()
        else:
            card = OrderProduct(order_id=basket.order_id, card_id=data['card_id'])
            db.session.add(card)
            db.session.flush()
            db.session.commit()
        response = jsonify({'data': f'Товар {data["card_name"]} добавлен в корзину'})
        response.status_code = 200
        return response

    @login_required(current_user)
    def delete(self):

        # удаляет все продукты с данным id (значок корзины возможно)
        data = basket_data_delete.parse_args()
        basket = Order.query.filter_by(user_id=current_user.user_id, status=False).first()
        OrderProduct.query.filter_by(order_id=basket.order_id, card_id=data['card_id']).delete()
        db.session.commit()

        response = jsonify({'data': f'Товар удален из корзины'})
        response.status_code = 200
        return response


class Buy(Resource):
    # если пользователь нажимает на кнопку сделать заказ, то он перемещается на страницу(или открывается окно)
    # где можно добавить адрес доставки с помощью карты мейби (отдельный роут мейби это фронт все),
    # на этой же странице будет кнопка с оплатой, оплата перемещает на эквайринг, только если выбран адрес
    # или выбрано - заберу сам
    # если адрес выбран, и оплата подтверждена от экваринга, то status order = True, и сообщения улетают работникам
    # потом этот адрес запоминается,
    #
    pass


api_basket.add_resource(Index, '/')
api_basket.add_resource(Buy, '/buy')
