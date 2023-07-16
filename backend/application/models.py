from application import db, login_manager


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    role = db.Column(db.String(20))
    token = db.Column(db.String(200), nullable=True, index=True, unique=True)

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
    card_name = db.Column(db.String(20), unique=True)
    card_price = db.Column(db.Integer, nullable=False)
    card_image = db.Column(db.String(200))


class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    text = db.Column(db.String(200))
    address = db.Column(db.String(200), nullable=True)
    date = db.Column(db.Date, nullable=True)
    status = db.Column(db.Boolean, nullable=False, default=False)


class OrderProduct(db.Model):
    order_product_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id', ondelete='CASCADE'), nullable=False)
    card_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False, default=1)