from sortedcontainers import SortedSet

class orderBook:
    def __init__(self, _master, _initData):
        self._master = master
        self.contractName = str(_initData['contractName'])
        self.contractID = int(_initData['contractID'])
        self.orders = (SortedSet(), SortedSet())
    
        self._master.contractNameIDs[self.contractName] = self.contractID

    def serialize(self):
        return {
            'contractName':self.contractName, 
            'contractID':self.contractID
        }

    def add(self, order):
        opposingSide = self.orders[1 - order.side]
        while True:
            if order.qty == 0 or len(opposingSide) == 0: 
                break

            opposingOrder = opposingSide[0]
            if (order.side == 0 and opposingOrder.price > order.price) or (order.side == 1 and opposingOrder.price < order.price):
                break
            if opposingOrder.mpid == order.mpid:
                opposingOrder.remove()
                continue

            fillPrice, fillQty = opposingOrder.price, min(order.qty, opposingOrder.qty)
            order.fill(fillPrice, fillQty)
            opposingOrder.fill(fillPrice, fillQty)
        
        if order.qty != 0:
            self.orders[order.side].add(order)

    def remove(self, order):
        self.orders[order.side].discard(order)
        