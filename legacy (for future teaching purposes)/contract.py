
from sortedcontainers import SortedList
from order import order
import time as t

class contract:
    def __init__(self, _master, _initData):
        self._master = _master
        
        self.position = _initData['p']
        self.reducible = _initData['r']
        
        self.orders = self._master.orders
        self.redOrders = [0, 0]
        self.ordersBySide = [SortedList(), SortedList()]

    @property
    def account(self):
        return self._master

    def getOrders(self, side, type, return_iter=False, reversed=False):
        orders, reds = self.ordersBySide[side], self.redOrders[type]
        incs = len(orders) - reds
        if (type == 0 and not reds) or (type == 1 and not incs):
            return None
        start_index = 0 if type == 0 else reds
        end_index = reds - 1 if type == 0 else len(orders) - 1
        if return_iter:
            return range(start_index, end_index + 1) if not reversed else range(end_index, start_index - 1, -1)
        else:
            return orders[start_index] if type == 0 else orders[end_index]
    
    def addOrder(self, price, side, qty):
        orderID = self.account.getOrderID()
        if not orderID:
            return False
        red = min(qty, self.reducible[1 - side])
        inc = qty - red
        ordr = order(
            _master = self,
            orderID = orderID, 
            price = price, 
            side = side, 
            qty = [red, inc]
        )