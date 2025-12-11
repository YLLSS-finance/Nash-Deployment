from lightning.orderProperties import orderProperties
import time as t

class position:
    def __init__(self, _master, _mpid, _contractID):
        '''
        PLEASE ONLY INITIALISE THIS AFTER _MASTER.ORDERS AND _MASTER.POSITIONS ARE LOADED
        
        :param self: Description
        :param _master: 
        :param mpid: Description
        :param contractID: Description
        :param position: Description
        '''
        
        self.mpid = _mpid
        self.contractID = _contractID
        self.accountOrders = self._master.orders[_mpid]
        self.accountBalances = self._master.balance[_mpid]
        
        _posDict = self._master.positions
        if not _mpid in _posDict:
            _posDict[_mpid] = {_contractID:[0, 0]}
        elif not _contractID in _posDict[_mpid]:
            _posDict[_mpid][_contractID] = [0, 0]
            
        self.position = self._master.positions[_mpid][_contractID]
        
        self.reducible = (0, 0)
        self.orders = (SortedList(key=orderProperties.compareOrder), SortedList(key=orderProperties.compareOrder))
        self.reduceOrders = (0, 0)
        
        self.orderPrio = orderProperties.compareOrder
     
    @property
    def _avblOrderID(self):
        for i in range(0, 20):
            break
            
    def _loadSerialOrder(self, serialOrder):
        self.orders[serialOrder[5]].add(serialOrder)
        if serialOrder[6][0]: self.reduceOrders[serialOrder[5]] += 1
        return -cost(serialOrder)
    
    def addOrder(self, price, side, qty):
        orderID = self._avblOrderID
        if not orderID: 
            return False
        
        order = [orderID, t.time(), self.mpid, self.instrumentID, price, side, [0, 0]]
        orderCost = self.cost(order)
        
        oppSide = 1 - side
        orderRed = qty = self.reducible[oppSide]
        orderInc = 1 - orderInc
        
        oppRedOrders = self.reduceOrders[oppSide]
        oppRedOrderList = self.orders[oppSide]
        marginUsed = 0
        change = []
        if oppRedOrders:
            for orderIndex in range(oppRedOrders - 1, -1, -1):
                oppOrder = oppRedOrderList[orderIndex]
                if orderPrio(oppOrder) < orderPrio(order):
                    break
                shift = min(order[6][1], oppOrder[6][0])
                if not shift: 
                    break
                orderInc -= shift
                orderRed += shift
                change.append(oppOrder, shift)
                marginUsed += self.cost(oppOrder) * shift
        
        marginUsed += orderCost * orderInc
        if marginUsed > self.accountBalances[1]:
            return False
        self.accountBalances[1] -= marginUsed
        
        order[6] = [orderRed, orderInc]
        for changedOrder, orderShift in change:
            changedOrder[6][0] -= orderShift
            changedOrder[6][1] += orderShift
        
        # This is for the insertion into the doubly linked list
        order.append([None, None])
        self.accountOrders[orderID] = order
        if orderRed:
            self.reduceOrders[side] += 1
    
    def reallocReducible(self):
        orderSide = 1 if self.reducible[0] else 0
        if self.reducible[orderSide]:
            raise Exception('Fatal error: Reducible position data corrupted')
        
        oppRedOrders = self.reduceOrders[orderSide]
        oppOrders = self.orders[orderSide]
        if oppRedOrders == len(oppOrders):
            return # there are no orders with increase component
        
        reducible = self.reducible[1 - orderSide]
        for orderIndex in range(oppRedOrders, len(oppOrders)):
            order = oppOrders[orderIndex]
            reallocQty = min(order[6][1], reducible)
            if reallocQty == 0:
                break
            order[6][1] -= reallocQty
            order[6][0] += reallocQty
            reduceible -= reallocQty
            