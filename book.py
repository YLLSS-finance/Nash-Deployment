
from sortedcontainers import SortedSet

class orderBook:
    def __init__(self):
        self.priceLevels = [SortedSet(), SortedSet()]
        # price level: [head, tail]
        self.ordersAtLevel = [{}, {}]
        self.bestPrices = [None, None]
        
        self.orders = {}
    
    def addOrderToLevel(self, order):
        priceLevel = self.priceLevels[order.side]
        if not order.price in priceLevel:
            priceLevel.add(order.price)
            self.ordersAtLevel[order.side][order.price] = [None, None, 0]
        if self.bestPrices[order.side] is None:
            self.bestPrices[order.side] = order.price
        else:
            if order.side == 0:
                if order.price > self.bestPrices[order.side]: self.bestPrices[order.side] = order.price 
            else:
                if order.price < self.bestPrices[order.side]: self.bestPrices[order.side] = order.price 
    
        headTails = self.ordersAtLevel[order.side][order.price]
        headTails[2] += 1
        orderHead = headTails[1]
        orderTail = None
        
        self.orders[orderHead][1] = order
        self.orders[order] = [orderHead, orderTail]
        if headTails[0] is None:
            headTails[0] = order
        headTails[1] = order
    
    def removeOrder(self, order):
        orderLinks = self.orders[order]
        listEnds = self.ordersAtLevel[order.side][order.price]
        listEnds[2] -= 1
        
        if order == listEnds[0]:
            listEnds[0] = orderLinks[1]
        if order == listEnds[1]:
            listEnds[1] = orderLinks[0]
        
        # set the tail of the head of the removed order to the tail of the removed order
        self.orders[orderLinks[0]][1] = orderLinks[1]
        # set the head of the tail of the removed order to the head of the removed order
        self.orders[orderLinks[1]][0] = orderLinks[0]
        
        del self.orders[order]
        if listEnds[2] == 0:
            del self.ordersAtLevel[order.side][order.price]