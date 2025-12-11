
from sortedcontainers import SortedList
from lightning.orderProperties import orderComparator as orderProperties
import time as t

class exchange:
    # Order Format
    # [orderID, timestamp, mpid, instrumentID, price, side, [red, inc]]
    #    0          1       2         3          4     5        6
    def __init__(self):
        # LOAD THESE
        self.accounts = set()
        # [balance, avblBalance]
        self.balance = {}
        self.orders = {}
        self.positions = {}
        
        # INFERRED
        self.books = {}
    
