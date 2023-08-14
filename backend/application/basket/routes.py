import datetime
from flask import jsonify, url_for
from flask_login import current_user
from application import db
from application.auth.auth import login_required
from application.basket import api_basket
from application.basket.fields_validation import basket_data, basket_data_delete
from application.basket.service import get_order_products, get_card_product, get_basket, create_basket, \
    get_order_product

from application.models import CardProduct, Order, OrderProduct
from flask_restful import Resource, marshal_with, fields


class Basket(Resource):
    card_fields = {
        'order_id': fields.Integer,
        'user_id': fields.Integer,
        'card_id': fields.Integer,
        'amount': fields.Integer,
        'name': fields.String,
        'image': fields.String,
        'price': fields.Integer
    }

    @login_required(current_user)
    @marshal_with(card_fields)
    def get(self):
        order_products = get_order_products(current_user)

        if not order_products:
            response = {'name': 'Корзина пустая'}
            return response, 200

        basket_dicts = []
        for row in order_products:
            row = {'order_id': row.order_id, 'user_id': row.user_id,
                   'image': url_for('static', filename=row.image),
                   'card_id': row.card_id, 'amount': row.amount, 'name': row.name,
                   'price': row.price}
            basket_dicts.append(row)

        return basket_dicts

    @login_required(current_user)
    def patch(self):
        data = basket_data.parse_args()

        card = get_card_product(data['card_id'])
        if card is None:
            response = jsonify({'data': f'Такой товар не существует'})
            response.status_code = 200
            return response

        basket = get_basket(current_user.user_id)
        if basket is None:
            create_basket(current_user.user_id)
        order_product = get_order_product(basket.order_id, data['card_id'])

        # если такой товар уже есть в корзине, то нужно увеличить его amount на один
        if order_product and data['action'] == '+':
            order_product.amount += 1
            order_product.price += card.price
            response = jsonify({'data': f'Товар {card.name} добавлен в корзину'})

        elif order_product and data['action'] == '-':
            if order_product.amount == 1:
                OrderProduct.query.filter_by(order_id=basket.order_id, card_id=data['card_id']).delete()
                response = jsonify({'data': f'Товар {card.name} удален окончательно из корзины'})
            else:
                order_product.amount -= 1
                order_product.price -= card.price
                response = jsonify({'data': f'Товар {card.name} удален из корзины'})

        elif data['action'] == '+':
            order_product = OrderProduct(order_id=basket.order_id, card_id=data['card_id'], price=card.price)
            db.session.add(order_product)
            response = jsonify({'data': f'Товар {card.name} первый раз добавлен в корзину'})

        elif data['action'] == '-':
            response = jsonify({'data': f'Товара {card.name} еще нет в корзине'})

        db.session.commit()

        response.status_code = 200
        return response

    @login_required(current_user)
    def delete(self):

        # удаляет все продукты с данным id (значок корзины возможно)
        data = basket_data_delete.parse_args()
        basket = Order.query.filter_by(user_id=current_user.user_id, status='basket').first()
        card = OrderProduct.query.filter_by(order_id=basket.order_id, card_id=data['card_id']).first()
        if card is None:
            response = jsonify({'data': f'В вашей корзине нет такого товара'})
            response.status_code = 200
            return response

        OrderProduct.query.filter_by(order_id=basket.order_id, card_id=data['card_id']).delete()
        db.session.commit()

        response = jsonify({'data': f'Товар удален окончательно из корзины'})
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
        'date': fields.DateTime,
        'order_id': fields.Integer,
        'amount': fields.Integer,
        'name': fields.String,
        'image': fields.String,
        'price': fields.Integer
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
        response = {'data': f'Перенаправление на страницу оплаты, цена заказа: {sum_price}'}
        if not response:
            pass
            # если страница оплаты возвращает True, то status = paid и заказ появляется у ресторана,
            # он может принять его или отклонить
        basket.status = 'paid'
        basket.date = datetime.datetime.now()
        db.session.commit()
        return order_products


api_basket.add_resource(Basket, '/')
api_basket.add_resource(Buy, '/buy')
