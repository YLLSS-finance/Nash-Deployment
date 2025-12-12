
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
        orderDict = self.levels[order[5]]
        orderHeadTail = order[7]
        if not price in orderDict.keys():
            orderDict[price] = [order, order, 0, 0]
            orderHeadTail = [None, None]
            return

        priceLevelInfo = orderDict[order.price]
        priceLevelInfo[1] = order
        orderHeadTail[0] = priceLevelInfo[1]
        orderHeadTail[1] = None

        priceLevelInfo[2] += sum(order[6])
        priceLevelInfo[3] += 1

    # CAUTION: this assumes that the order is already a member of the book
    def removeOrder(self, order):
        priceLevelInfo = self.levels[order[5]][order[4]]
        if order == priceLevelInfo[0]:
            priceLevelInfo[0] = order[7][1]
        elif order == priceLevelInfo[1]:
            priceLevelInfo[1] = order[7][0]
        priceLevelInfo[2] -= sum(order[6])
        priceLevelInfo[3] -= 1

        orderHead = order[7][0]
        orderTail = order[7][1]
        orderHead[7][1] = orderTail
        orderTail[7][0] = orderHead
