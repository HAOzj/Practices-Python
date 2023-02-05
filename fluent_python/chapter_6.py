# -*- coding:utf-8 -*-
from collections import namedtuple
from promotions import promo as promotions
import inspect

Customer = namedtuple('Customer', 'name fidelity')

class LineItem:
    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.quantity * self.price


class Order:
    def __init__(self, customer, cart, promo=None):
        self.customer = customer
        self.cart = list(cart)
        self.promo = promo

    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total

    def due(self):
        if not self.promo:
            discount = 0
        else:
            discount, name = self.promo(self)
            print('discount is {:^10.2f} promotion is {}'.format(discount, name))
        return self.total() - discount

    def __repr__(self):
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(), self.due())


def main():
    hzj = Customer('hzj', 1200)
    cart = [LineItem('monitor', 20, 100),
            LineItem('burger', 20, 3),
            LineItem('dock', 1, 100),
            LineItem('converter', 1, 50),
            LineItem('slope', 1, 50)]

    def best_promo(order):
        """选择可用的最佳折扣
        """
        return max((promo(order), promo.__name__) for promo in promotions.promos)
        # return max((promo(order), name) for name, promo in inspect.getmembers(promotions, inspect.isfunction))

    order = Order(hzj, cart, best_promo)
    print('bulk_item_promo func has name as ', promotions.bulk_item_promo.__name__)
    print(order)


if __name__ == "__main__":
    main()

