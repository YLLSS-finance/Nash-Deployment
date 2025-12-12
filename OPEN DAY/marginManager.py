
class marginManager:
    def __init__(self, _master, mpid, contractID):
        self.userPositions = self._master.userPositions[mpid]
        if not contractID in self.userPositions: self.userPositions[contractID] = [[0, 0], [0, 0]]
        
        self.position, self.reducible = self.userPositions[contractID]
        # This has to be done as we are going to establish the reducible position manually for integrity
        self.reducible = self.position
        
        for order in _master.orders.items():
            if order[3] == contractID:
                self.reducible[1 - order[5]] -= order[6][0]
        