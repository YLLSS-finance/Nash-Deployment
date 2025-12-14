
# Made By (not) Chan Yan Ching Ching
# ---------------------------------------------------------------------------------
# | Order Format                                                                  |
# | [orderID, timestamp, mpid, contractID, price, side, [red, inc], [head, tail]] |
# |   0          1       2        3         4     5        6            7         |
# ---------------------------------------------------------------------------------

from sortedcontainers import SortedList
from orderProperties import orderProperties as op
import time as t

class marginManager:
    def __init__(self, _master, mpid, contractID):
        """
        Initialises a margin manager object based on Market Participant ID and Contract ID.
        Dependencies:
        **_master.userPositions[mpid] where the key mpid must exist, and the CURRENT POSITION must be vaild;
        _master.orders[mpid]** where the key mpid must exist;
        _master.userBalances[mpid] where the key mpid must exist.
        """

        # ------------------------------------------------------------------------------------------
        # Add referances to dependencies
        self.mpid = mpid
        self.contractID = contractID

        self.accountBalance = _master.userBalances[mpid]
        self.accountPositions = _master.userPositions[mpid]
        self.accountOrders = _master.userOrders[mpid]
        if not contractID in self.accountPositions: self.accountPositions[contractID] = [[0, 0], [0, 0]]
        self.position, self.reducible = self.accountPositions[contractID]
        # ------------------------------------------------------------------------------------------

        # ------------------------------------------------------------------------------------------
        # Reconstruct reducible, sortedList of all orders by side, and list of the number of all orders containing a reducible
        # component by side This has to be done as we are going to establish the reducible position manually for
        # integrity
        self.reducible[:] = self.position
        self.orderList = [SortedList(key=op.buyOrderComparator), SortedList(key=op.sellOrderComparator)]
        self.reduceOrders = [0, 0]

        # Initialize reducible position and available margin based on the orders specific for the contract this class is pointing to.
        # Bear in mind that this would lead to a complete and proper initialization of all reducible positions and deductable balances
        # If all marginManager objects are created for all contracts that an account has interacted with.
        #
        # After all initializations we can just simply check if the available balance is positive or not to validate data integrity.

        for order in _master.orders[mpid].items():
            if order[3] == contractID:
                self.reducible[1 - order[5]] -= order[6][0]
                self.orderList[order[5]].add(order)
                if order[6][0]: self.reduceOrders[order[5]] += 1
                self.accountBalance[1] -= op.orderCost(order) * order[6][1]

        self.orders = _master.orders[mpid]
        # ------------------------------------------------------------------------------------------
        # Optimisation mappings
        # ------------------------------------------------------------------------------------------
        self.oppSideMap = [1, 0]
        self.priorityComparatorMap = [op.buyOrderComparator, op.sellOrderComparator]

    @property
    def avblOrderID(self):
        for i in range(0, 20):
            if not i in self.accountOrders:
                return i
        return None

    def addOrder(self, price, side, qty):
        orderID = self.avblOrderID
        if orderID is None:
            return

        red = min(qty, self.reducible[self.oppSideMap[side]])
        inc = qty - red
        order = [orderID, t.time(), self.mpid, self.contractID, price, side, [red, inc], [None, None]]

        # A conflict (order with increase component, the new order, having more priority than an order with a reduce
        # component) can only occur if the new order has an increase component and there are currently reduce orders
        # in the order queue
        if self.reduceOrders[side] and inc:
            # Generator object to iterate over all reduce orders on the side of the new order in ascending order of
            # execution priority
            scan_range = range(self.reduceOrders[side], -1, -1)
            scanned_orders = self.orderList[side]
            priority = self.priorityComparatorMap[side]
            for order_index in scan_range:
                reduce_order = scanned_orders[order_index]
            f