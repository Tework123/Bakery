# функции одинаковые, но пока оставить как есть, вдруг нужно будет поменять что-то
def pass_orders_to_list_dicts(pass_orders):
    list_dicts_pass_orders = []
    for row in pass_orders:
        for i in range(len(row)):

            if i == 6:
                list_cards = [list(a) for a in (zip(row[6].split(', '),
                                                    row[7].split(', '), ))]
                list_dicts_cards = []
                for i in list_cards:
                    dicts = {}
                    for j in range(len(i)):
                        if j == 0:
                            dicts['name'] = i[j]
                        else:
                            dicts['amount'] = i[j]

                    list_dicts_cards.append(dicts)

        row = {'order_id': row.order_id, 'text': row.text, 'address': row.address, 'date': row.date,
               'status': row.status,
               'price': row.price, 'cards': list_dicts_cards}

        list_dicts_pass_orders.append(row)
    return list_dicts_pass_orders


def current_orders_to_list_dicts(current_orders):
    list_dicts_current_orders = []
    for row in current_orders:
        for i in range(len(row)):

            if i == 6:
                list_cards = [list(a) for a in (zip(row[6].split(', '),
                                                    row[7].split(', ')))]
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

        row = {'order_id': row.order_id, 'text': row.text, 'address': row.address, 'date': row.date,
               'status': row.status,
               'price': row.price, 'cards': list_dicts_cards}

        list_dicts_current_orders.append(row)
    return list_dicts_current_orders
