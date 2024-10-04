import json
import functools

with open('challenge.json','r') as f:
    information = json.load(f)


def filter_names(buyers : list[dict[str,str]], equal : str):
    value = buyers.pop()
    if equal == value['name']:
        return False
    elif len(buyers) > 0:
        return filter_names(buyers,equal)
    return True

def reduce_price(accu,value):
    if 'price' in accu:
        accu = {'total_revenue' : accu['price']*accu['quantity'],'transactions_per_product' : {accu['product'] : accu['quantity']}, 'unique_buyers' : [accu['buyer']]}

    price = value['price']
    quantity = value['quantity']
    product = value['product']
    accu['total_revenue'] += price*quantity
    
    x = accu['transactions_per_product']
    x.setdefault(product,0)
    x[product] += quantity

    if filter_names(accu['unique_buyers'].copy(),value['buyer']['name']):
        accu['unique_buyers'].append(value['buyer'])
    return accu

print(functools.reduce(reduce_price,information))