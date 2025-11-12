from order import order
from sortedcontainers import SortedSet
import time as t

class contract:
    def __init__(self, _master, _initData=None):

        self._master = _master
        self.mpid = _master.mpid
        self.balance = _master.balance
        self.orders = _master.orders

        self.contractID = _initData['contractID']
        self.book = _master._master.contracts[self.contractID]

        self.position = _initData['position']
        self.reducible = _initData['reducible']

        self.contractOrders = set()
        self.ordersAtPrice = {}
        self.inc = (SortedSet(), SortedSet())
        self.red = (SortedSet(), SortedSet())

        for ordrData in _initData['orders'].values():
            order(
                _master = self, 
                *ordrData
            )
            
    def batchRemoveOrders(self, orders):
        for orderID in list(orders):
            if orderID in self.orders:
                self.orders[orderID].remove()

    def resolve(self, resolutionValue):
        self.batchRemoveOrders(self.contractOrders)
        self._master.balance += self.position[0] * resolutionValue
        self._master.balance += self.position[1] * (100 - resolutionValue)
        del self._master.contracts[self.contractID]

    def getOrderID(self):
        for i in range(0, self._master.order_limit):
            if not i in self.orders:
                return i
        return False

    def addOrder(self, price, side, qty):
        orderID = self.getOrderID()
        if orderID is False:
            return {
                'callback':000, 
                'debug':'All order slots have been taken up'
            }

        cost = price if side == 0 else 100 - price
        red = min(self.reducible[1 - side], qty)
        inc = qty - red

        timestamp = round(1000 * t.time())
        prioKey = (-cost, timestamp, self.mpid, orderID)

        chgs = []
        redOrders = self.red[side]
        marginUsed = 0
        while True:
            if len(redOrders) == 0:
                break
            existingOrder = redOrders[-1]

            if inc == 0 or existingOrder.prioKey < prioKey:
                break
            
            swapQty = min(inc, existingOrder.red)
            if swapQty == 0:
                break
                
            chgs.append(existingOrder, swapQty)
            inc -= swapQty
            red += swapQty

        marginUsed += inc * cost

        if marginUsed > self.balance:
            return {
                'callback':'001', 
                'debug':'Insufficient balance'
            }

        self.reducible[1 - self.side] -= red
        order(
            _master = self, 
            timestamp = timestamp, 
            orderID = orderID, 
            mpid = self.mpid,
            contractID = self.contractID, 
            price = price, 
            side = side, 
            red = red, 
            inc = inc,
            compKey = prioKey, 
            cost = cost
        )
        
        return {
            'callback':'100', 
            'debug':'Order placed successfully'
        }
    
    def allocReducible(self):
        reduceSide = 0 if self.reducible[0] != 0 else 1
        if self.reducible[1 - reduceSide] == 0: return None
        if self.reducible[1 - reduceSide] != 0: raise Exception('Fatal error: reducible component is two-sided')

        incOrders = self.inc[1 - reduceSide]
        reducible = self.reducible[reduceSide]
        while True:
            if len(incOrders) == 0: 
                break
            incOrder = incOrders[0]
            transferQty = min(reducible, incOrder.inc)
            if transferQty == 0:
                break
            incOrder._transfer(-transferQty)
            reducible -= transferQty

        self.reducible[reduceSide] = reducible
    
    def reprPos(self, pos):
        return pos[0] - pos[1]
    
    def reprSideOrders(self, side):
        result = 'BIDS\n' if side == 0 else 'ASKS\n'
        coveredOrderIDs = set()
        for ordrs in (self.red[side], self.inc[side]):
            for ordr in ordrs:
                if not ordr.orderID in coveredOrderIDs:
                    result = f'{result}{str(ordr)}\n'
                    coveredOrderIDs.add(ordr.orderID)
        return result
            
    
    def __str__(self):
        l1 = f'{self.book.contractName} (#{self.contractID})/n'
        l2 = f'Pos {self.reprPos(self.position)} (Avbl. {self.reprPos(self.reducible)})/n'
        l3 = self.reprSideOrders(0)
        l4 = self.reprSideOrders(1)
        return f'{l1}{l2}{l3}{l4}'