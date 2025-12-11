
class orderProperties:
    # Order Format
    # [orderID, timestamp, mpid, instrumentID, price, side, [red, inc]]
    #    0          1       2         3          4     5        6
    
    @staticmethod
    def compareOrder(order):
        # price, time, orderID, mpid
        return (order[4] * [-1, 1][order[5]], order[1], order[0], order[2])
    
    @staticmethod
    def cost(order):
        return order[4] if order[5] == 0 else (100 - order[4])
