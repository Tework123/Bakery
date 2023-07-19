from werkzeug.datastructures import FileStorage
from flask_restful import reqparse

# создание карточки
card_data = reqparse.RequestParser()
card_data.add_argument('name', type=str, location='form', help='Требуется имя товара', required=True)
card_data.add_argument('price', type=int, location='form', help='Требуется цена товара', required=True)
card_data.add_argument('image', type=FileStorage, location='files', help='Требуется картинка товара', required=True)

# как то записать фоточку товара сюда


# удаление карточки
card_delete_data = reqparse.RequestParser()
card_delete_data.add_argument('card_id', type=str, help='Нужен id товара', required=True)
card_delete_data.add_argument('name', type=str, help='Требуется имя товара', required=False)
card_delete_data.add_argument('price', type=int, help='Требуется цена товара', required=False)
card_delete_data.add_argument('image', type=str, help='Требуется картинка товара', required=False)

# изменение карточки, любого поля или полей
card_patch_data = reqparse.RequestParser()
card_patch_data.add_argument('card_id', type=str, location='form', help='Нужен id товара', required=True)
card_patch_data.add_argument('name', type=str, location='form', help='Требуется имя товара', required=False)
card_patch_data.add_argument('price', type=int, location='form', help='Требуется цена товара', required=False)
card_patch_data.add_argument('image', type=FileStorage, location='files', help='Требуется картинка товара',
                             required=False)