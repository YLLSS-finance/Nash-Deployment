
# Don't worry, all order logging is done over at the book!

class order:
    def __init__(self, _master, orderID, timestamp, price, side, qty):
        self._master = _master
        self.orderID = orderID
        self.timestamp = timestamp
        self.price = price
        self.side = side
        self.red, self.inc = qty
        
        self.cost = self.price if self.side == 0 else (100 - self.price)
        self.comparisonKey = (self.cost, self.timestamp, self.mpid, self.orderID)
    
    @property
    def __lt__(self, other):
        return self.comparisonKey < other.comparisonKey
    
    @property
    def __hash__(self, other):
        return hash(self.comparisonKey)
    
    @property
    def mpid(self):
        return self._master._master.mpid
    
    @property
    def contractID(self):
        return self._master._master.contractID
    
    @property
    def account(self):
        return self._master._master
    
    @property 
    def contract(self):
        return self._master
    
    @property
    def qty(self):
        return self.red + self.inc

    def _setup(self, defer=False):
        self.contract.book.add(self, defer)
        if self.qty:
            if self.red: self.contract.redOrders[self.side] += 1
            self.contract.ordersBySide[self.side].add(self)
            self.contract.contractOrders.add(self.orderID)
            self.account.orders[self.orderID] = self
    
    def _remove(self):
        self.contract.contractOrders.remove(self.orderID)
        self.contract.ordersBySide[self.side].remove(self)
        del self.account.orders[self.orderID]
        
    def chgRedInc(self, redChg, incChg):
        lastRed = self.red
        self.red += redChg
        self.inc += incChg
        
        if (not lastRed) and self.red:
            self.contract.redOrders[self.side] += 1
        if lastRed and (not self.red):
            self.contract.redOrders[self.side] -= 1
    
    def shift(self, qty, chg_balance=True):
        self.chgRedInc(incChg=qty, redChg=-qty)
        self.account.balance += self.cost * qty
    
    def fill(self, price, qty):
        fillRed = min(qty, self.red)
        fillInc = qty - self.red
        priceImprovement = abs(price - self.price)
        self.chgRedInc(redChg=-fillRed, incChg=-fillInc)
        
        purchaseCost = price if self.side == 0 else 100 - price
        saleRevenue = (100 - self.cost + priceImprovement) * fillRed
        incMarginReturned = priceImprovement * fillInc
        
        self.account.avblBalance += saleRevenue + incMarginReturned
        self.account.balance += -(purchaseCost * fillInc) + saleRevenue
    
        self.contract.position[self.side] += fillInc
        self.contract.position[1 - self.side] -= fillRed
        
        self.contract.reducible[self.side] += fillInc
        self.contract.processReducible()
    
    def reduce(self, qty):
        reduceInc = min(qty, self.inc)
        reduceRed = min(qty, self.red)
        self.chgRedInc(redChg=-reduceRed, incChg=-reduceInc)
        
        self.contract.reducible[1 - self.side] += reduceRed
        self.contract.processReducible()
        
        