from flask_restful import reqparse

basket_data = reqparse.RequestParser()
basket_data.add_argument('card_id', type=int, help='Нужен id товара', required=True)
basket_data.add_argument('card_name', type=str, help='Требуется имя товара', required=True)
basket_data.add_argument('card_price', type=int, help='Требуется цена товара', required=True)


basket_data_delete = reqparse.RequestParser()
basket_data_delete.add_argument('card_id', type=int, help='Нужен id товара', required=True)