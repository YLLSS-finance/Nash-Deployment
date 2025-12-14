
# order format
# [orderID, timestamp, mpid, contractID, price, side, qty, [head, tail]]
#    0          1       2        3         4      5     6        7

from sortedcontainers import SortedDict

class orderProcessor:
    def __init__(self, contract_types):
        self.priceLevels = {cp:SortedDict(key=lambda x:-x) for cp in contract_types}
        self.bestPrices = {cp:None for cp in contract_types}

    def addOrder(self, order):

        price = order[5]
        if not price in self.priceLevels:
