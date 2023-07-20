from application import db, login_manager


class User(db.Model):
    # админ = ресторан, может добавлять, удалять карточки, менять цены,
    # имеет свой адрес и почту, телефон может быть
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    address = db.Column(db.String(200), nullable=True)
    # main
    role = db.Column(db.String(20))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def get_id(self):
        return str(self.user_id)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class CardProduct(db.Model):
    card_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    text = db.Column(db.String(1000))
    price = db.Column(db.Integer)
    image = db.Column(db.String(200), unique=True)


class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'))
    text = db.Column(db.String(1000))
    address = db.Column(db.String(200), nullable=True)
    date = db.Column(db.DateTime, nullable=True)
    # заполнение корзины: basket, оплата: paid, кухня: prepared, ready,
    # canceled_restaurant, курьер: delivered, success, canceled_delivery
    status = db.Column(db.String(20), default='basket')


class OrderProduct(db.Model):
    order_product_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id', ondelete='CASCADE'))
    card_id = db.Column(db.Integer, db.ForeignKey('card_product.card_id', ondelete='CASCADE'))
    amount = db.Column(db.Integer, default=1)
    price = db.Column(db.Integer)
