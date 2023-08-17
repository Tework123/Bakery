from flask import url_for


def orders_to_list_dicts(orders):
    list_dicts_orders = []
    for row in orders:
        for i in range(len(row)):

            if i == 5:
                list_cards = [list(a) for a in (zip(row[5].split(', '),
                                                    row[6].split(', '),
                                                    list(map(lambda image:
                                                             url_for('static', filename=image),
                                                             row[7].split(', ')))))]
                list_dicts_cards = []
                for i in list_cards:
                    dicts = {}
                    for j in range(len(i)):
                        if j == 0:
                            dicts['name'] = i[j]
                        if j == 1:
                            dicts['amount'] = i[j]
                        else:
                            dicts['image'] = i[j]
                    list_dicts_cards.append(dicts)

        row = {'order_id': row.order_id, 'text': row.text, 'date': row.date,
               'status': row.status,
               'price': row.price, 'cards': list_dicts_cards}

        list_dicts_orders.append(row)
    return list_dicts_orders
