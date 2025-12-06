
from sortedcontainers import SortedSet

class orderBook:
    def __init__(self, _master):
        self._master = _master
        
        self.priceLevels = [SortedSet(key=lambda x:-x), SortedSet()]
        # price level: [head, tail, number of orders]
        self.ordersAtLevel = [{}, {}]
        self.bestPrices = [None, None]
        
        # CONTAINS ORDER OBJECTS
        self.orders = {None:[None, None]}
        
        self._CACHE = None #Not implemented
    
    def matchIncomingOrder(self, order):
        opposingLevel = self.ordersAtLevel[1 - order.side]
        while True:
            bestPrice = self.bestPrices[1 - order.side]
            if not order.qty: break
            if not bestPrice: break
            if order.side == 0:
                if bestPrice > order.price: break
            else:
                if bestPrice < order.price: break
            # first order in line at the best price at the matching side
            bestOrder = opposingLevel[bestPrice][0]
            fillPrice = bestOrder.price
            fillQty = min(order.qty, bestOrder.qty)
            bestOrder.fill(fillPrice, fillQty)
            order.fill(fillPrice, fillQty)
            if not bestOrder.qty:
                self.removeOrder(bestOrder)
        if order.qty:
            self.addOrderToLevel(order)
    
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
            priceLevel = self.priceLevels[order.side]
            priceLevel.remove(order.price)
            self.bestPrices[order.side] = priceLevel[0] if len(priceLevel) else None