# -*- coding:utf-8 -*-
import functools
promos = []


def promotion(func):
    promos.append(func)
    # @functools.wraps(func)
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        return res
    return wrapper

@promotion
def bulk_item_promo(order):
    discount = 0
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * 0.1
    return discount


@promotion
def large_order_promo(order):
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * .07
    return 0


@promotion
def fidelity_promo(order):
    if order.customer.fidelity >= 1000:
        return order.total() * 0.05
    else:
        return 0