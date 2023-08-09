from application.models import CardProduct


def get_all_cards():
    cards = CardProduct.query.all()
    return cards


def get_one_card(card_id):
    card = CardProduct.query.filter_by(card_id=card_id).first()
    return card
