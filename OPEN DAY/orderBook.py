
# Made By (not) Chan Yan Ching Ching
# ---------------------------------------------------------------------------------
# | Order Format                                                                  |
# | [orderID, timestamp, mpid, contractID, price, side, [red, inc], [head, tail]] |
# |   0          1       2        3         4     5        6            7         |
# --------------------------------------------------------------------------------

from sortedcontainers import SortedDict

class orderBook:
    def __init__(self, _master, contractID):
        self.fillOrder = _master.fillOrder
        self.bestPrices = [None, None]
        self.levels = [SortedDict(key=lambda x:-x), SortedDict()]

    def addOrder(self, order):
        price = order[4]
        order_dict = self.levels[order[5]]
        order_headtail = order[7]
        if not price in order_dict.keys():
            order_dict[price] = [order, order, 0, 0]
            order_headtail[0] = None
            order_headtail[1] = None
            return

        pricelevel_info = orderDict[order.price]
        pricelevel_info[1] = order
        order_headtail[0] = pricelevel_info[1]
        order_headtail[1] = None

        pricelevel_info[2] += sum(order[6])
        pricelevel_info[3] += 1

    # CAUTION: this assumes that the order is already a member of the book
    def removeOrder(self, order):
        pricelevel_info = self.levels[order[5]][order[4]]
        if order == pricelevel_info[0]:
            pricelevel_info[0] = order[7][1]
        elif order == pricelevel_info[1]:
            pricelevel_info[1] = order[7][0]
        pricelevel_info[2] -= sum(order[6])
        pricelevel_info[3] -= 1

        order_head = order[7][0]
        order_tail = order[7][1]
        order_head[7][1] = orderTail
        orderTail[7][0] = orderHead

