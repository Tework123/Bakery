from application import db, login_manager


class Users(db.Model):
    id_user = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    role = db.Column(db.String(20))
    token = db.Column(db.String(200), nullable=True, index=True, unique=True)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def get_id(self):
        return str(self.id_user)


@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))


class CardProducts(db.Model):
    card_id = db.Column(db.Integer, primary_key=True)
    card_name = db.Column(db.String(20), unique=True)
    card_price = db.Column(db.Integer)
    card_image = db.Column(db.String(200))
