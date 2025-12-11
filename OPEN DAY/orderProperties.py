
# Made By (not) Chan Yan Ching Ching
# ---------------------------------------------------------------------------------
# | Order Format                                                                  |
# | [orderID, timestamp, mpid, contractID, price, side, [red, inc], [head, tail]] |
# |   0          1       2        3         4     5        6            7         |
# ---------------------------------------------------------------------------------

class orderProperties:
    @staticmethod
    def buyOrderComparator(self, order):
        return (-order[4], order[1], order[2], order[3])
    
    @staticmethod
    def sellOrderComparator(self, order):
        return (order[4], order[1], order[2], order[3])
    
    @staticmethod
    def orderCost(self, order):
        return order[4] if order[5] else 100 - order[4]
