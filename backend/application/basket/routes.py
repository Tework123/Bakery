import datetime
import json
import time

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
        'data': fields.String,
        'order_id': fields.Integer,
        'user_id': fields.Integer,
        'card_id': fields.Integer,
        'amount': fields.Integer,
        'name': fields.String,
        'image': fields.String,
        'price': fields.Price
    }

    @login_required(current_user)
    @marshal_with(card_fields)
    def get(self):
        order_products = db.session.query(Order.order_id, Order.user_id, OrderProduct.card_id, OrderProduct.amount,
                                          CardProduct.name,
                                          CardProduct.image,
                                          OrderProduct.price).join(OrderProduct,
                                                                   Order.order_id == OrderProduct.order_id).join(
            CardProduct, OrderProduct.card_id == CardProduct.card_id, isouter=True).where(
            Order.user_id == current_user.user_id, Order.status == 'basket').all()

        if not order_products:
            response = {'data': 'Корзина пустая'}
            return response, 200

        return order_products

    @login_required(current_user)
    def patch(self):
        # наверное нужно передавать с фронта какой-то знак, что пользователь нажал на - или на +
        # и уже тут с if провернуть операции, все таки это тоже patch

        # кнопка добавить в корзину на карточке товара и значок + около этого товара в корзине
        data = basket_data.parse_args()
        basket = Order.query.filter_by(user_id=current_user.user_id, status='basket').first()
        if basket is None:
            basket = Order(user_id=current_user.user_id)
            db.session.add(basket)
        order_product = OrderProduct.query.filter_by(order_id=basket.order_id, card_id=data['card_id']).first()

        # если такой товар уже есть в корзине, то нужно увеличить его amount на один
        if order_product:
            order_product.amount += 1
            order_product.price += data['price']
            db.session.commit()
        else:
            card = OrderProduct(order_id=basket.order_id, card_id=data['card_id'], price=data['price'])
            db.session.add(card)
            db.session.flush()
            db.session.commit()

        response = jsonify({'data': f'Товар {data["name"]} добавлен в корзину'})
        response.status_code = 200
        return response

    @login_required(current_user)
    def delete(self):

        # удаляет все продукты с данным id (значок корзины возможно)
        data = basket_data_delete.parse_args()
        basket = Order.query.filter_by(user_id=current_user.user_id, status='basket').first()
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
    # если адрес выбран, и оплата подтверждена от экваринга, то status order = paid, и сообщения улетают работникам
    # потом этот адрес запоминается,
    card_fields = {
        'data': fields.String,
        'order_id': fields.Integer,
        'amount': fields.Integer,
        'name': fields.String,
        'image': fields.String,
        'price': fields.Price
    }

    @login_required(current_user)
    @marshal_with(card_fields)
    def get(self):
        basket = Order.query.filter_by(user_id=current_user.user_id, status='basket').first()
        if basket is None:
            response = {'data': 'Корзина пустая'}
            return response, 200

        order_products = db.session.query(Order.order_id, OrderProduct.amount,
                                          OrderProduct.price,
                                          CardProduct.image, CardProduct.name).join(
            OrderProduct,
            Order.order_id == OrderProduct.order_id).join(
            CardProduct, OrderProduct.card_id == CardProduct.card_id).where(
            OrderProduct.order_id == basket.order_id, Order.status == 'basket').all()

        if not order_products:
            response = {'data': 'Корзина пустая'}
            return response, 200

        sum_price = 0
        for i in order_products:
            sum_price += i.price
        print(sum_price)
        response = {'data': f'Перенаправление на страницу оплаты, цена заказа: {sum_price}'}

        # если страница оплаты возвращает True, то status = paid и заказ появляется у ресторана,
        # он может принять его или отклонить
        basket.status = 'paid'
        basket.date = datetime.datetime.now()
        print(basket.date)
        db.session.commit()
        return order_products


api_basket.add_resource(Index, '/')
api_basket.add_resource(Buy, '/buy')
