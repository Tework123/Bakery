from flask_restful import reqparse

# добавление товара в корзину
basket_data = reqparse.RequestParser()
basket_data.add_argument('card_id', type=int, help='Нужен id товара', required=True)

# удаление товара из корзины
basket_data_delete = reqparse.RequestParser()
basket_data_delete.add_argument('card_id', type=int, help='Нужен id товара', required=True)
