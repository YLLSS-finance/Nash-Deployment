class order:
    def __init__(self, _master, orderID, timestamp, contractID, price, side, red, inc, cost, compKey):
        self._master = _master

        self.orderID = orderID
        self.timestamp = timestamp
        self.mpid = _master.mpid
        self.contractID = contractID
        self.price = price
        self.side = side
        self.red = red
        self.inc = inc
        self.compKey = compKey
        self.cost = cost

        self._master.orders[self.orderID] = self
        self._master.book.add(self)
        self._master.contractOrders.add(self.orderID)
        if not self.price in self._master.ordersAtPrice:
            self._master.ordersAtPrice[self.price] = set()
        self._master.ordersAtPrice[self.price].add(self.orderID)
        
        # There is no need to attempt adding to account contract order margining queue if the order is already fully filled
        if not self.qty == 0:
            self._update()
            self._master.logChg()
        
    def __hash__(self):
        return hash(self.compKey)

    def __lt__(self, other):
        return self.compKey < other.compKey    

    @property
    def qty(self):
        return self.red + self.inc

    def _serialize(self):
        return [self.orderID, self.timestamp, self.mpid, self.contractID, self.price, self.side, self.red, self.inc, self.cost, self.compKey]

    def _update(self):
        self._master.logChg()

        inc, red = self._master.inc[self.side], self._master.red[self.side]
        inc.discard(self) if self.inc == 0 else inc.add(self)
        red.discard(self) if self.red == 0 else red.add(self)
        if self.qty == 0:
            del self._master.orders[self.orderID]
            self._master.contractOrders.discard(self.orderID)
            self._master.ordersAtPrice[self.price].discard(self.orderID)
            self._master.book.remove(self)        

    def _transfer(self, delta):
        self.inc += delta
        self.red -= delta
        self._master.balance -= delta * self.cost
        self._update()

    def fill(self, price, qty):
        if qty > self.qty:
            raise Exception('fatal error: fill quantity exceeds order quantity')
        fillRed = min(qty, self.red)
        fillInc = min(qty - fillRed, self.inc)
        self._master.balance += fillRed * (100 - self.cost) + qty * abs(price - self.price)

        if fillRed != 0:
            self._master.position[1 - self.side] -= fillRed
        if fillInc != 0:
            self._master.position[self.side] += fillInc
            self._master.reducible[self.side] += fillInc


        self.red -= fillRed
        self.inc -= fillInc

        self._update()
    
    def reduce(self, qty):
        reduceInc = min(self.inc, qty)
        reduceRed = min(self.red, qty - reduceInc)
        self.inc -= reduceInc
        self.red -= reduceRed

        self._master.balance += reduceInc * self.cost
        self._master.reducible[1 - self.side] += reduceRed
        self._master.allocReducible()
        self._update()
    
    def remove(self):
        self.reduce(self.qty)
    
    def __str__(self):
        side = 'Open Long / Close Short' if self.side == 0 else 'Open Short / Close Long'
        return f'Order #{self.orderID} {side} at {self.price} (Open {self.inc} Close {self.red})'