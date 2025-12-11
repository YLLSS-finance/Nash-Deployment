

# Made By (not) Chan Yan Ching Ching
# ---------------------------------------------------------------------------------
# | Order Format                                                                  |
# | [orderID, timestamp, mpid, contractID, price, side, [red, inc], [head, tail]] |
# |   0          1       2        3         4     5        6            7         |
# --------------------------------------------------------------------------------

from orderProperties import orderProperties as op

class exchange:
    def __init__(self):
        self.userBalances = {}
        self.userOrders = {}
        
        # {mpid:{contractID:[pos, red]}}
        self.userPositions = {}
        
        self.contracts = {}
    
    # TODO: Logging
    def _fillOrder(self, userBalances, order, price, qty):
        fillRed = min(qty, order[6][0])
        fillInc = qty - fillRed
         
        priceImprovement = abs(price - order.price)
        orderCost = op.orderCost(order)
        
        userBalances = self.userBalances[mpid]
        saleRevenue = fillRed * (orderCost + priceImprovement)
        increaseCost = fillInc * (orderCost - priceImprovement)
        
        userBalances[1] += priceImprovement * fillInc + saleRevenue
        userBalances[0] += -increaseCost + saleRevenue
        
        if sum(order[6]) == 0:
            self.removeOrder(order, skip_balance=True)
        
    def fillOrder(self, mpid, orderID, price, qty):
        self._fillOrder(order=self.userOrders[mpid][orderID], price=price, qty=qty)
    
    # TODO: Logging
    def removeOrder(self, order, skip_balance=False):
        mpid = order[2]
        del self.userOrders[mpid][order[0]]
        self.userPositions[mpid][1][1 - order[5]] += order[6][0]
        self.marginManagers[mpid][order[3]].allocReducible()
        if not skip_balance:
            self.userBalances[mpid][1] += op.orderCost(order) * order[6][1]
            