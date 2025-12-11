
class marginManager:
    def __init__(self, _master, mpid, contractID):
        self.userPositions = self._master.userPositions[mpid]
        if not contractID in self.userPositions:
        self.userContractPositions = self.userPositions