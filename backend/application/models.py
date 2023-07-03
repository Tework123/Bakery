from application import db, login_manager


class Users(db.Model):
    id_user = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(40))
    phone = db.Column(db.String(30))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def get_id(self):
        return str(self.id_user)


@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))


class Card(db.Model):
    id_card = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    price = db.Column(db.Integer)
