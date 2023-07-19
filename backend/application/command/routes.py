from flask.cli import with_appcontext
from application import db
from application.command import bp


@bp.cli.command('create_db')
@with_appcontext
def create_db():
    db.drop_all()
    db.create_all()
    print('create db')
    print('***Complete***')

# надо сделать по командам добавление следующей информации в базу данных:
# главного админа, работника, 5 пользователей
# 10 различных позиций товаров
# у каждого пользователя по 2 выполненных заказа с разными позициями
# у 3 в корзине есть позиции
# некоторые заказы полностью готовы success, другие на стадии ready, prepared, paid на кухне
#
