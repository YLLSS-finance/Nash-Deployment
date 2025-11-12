from contract import contract
from mutableInt import mutableInt
#hello github!
class account:
    def __init__(self, _master, _initData):
        self.mpid = int(_initData['mpid'])
        self.name = str(_initData['name'])
        self.balance = mutableInt(_initData['balance'])

        self.contracts = {}
        for contractID, contractData in _initData['contracts'].items():
            self.contracts[contractID] = contract(
                _master = self, 
                _initData = contractData
            )
    
    def serialize(self):
        return {
            'mpid':self.mpid, 
            'name':self.name, 
            'balance':self.balance, 
            'contracts':{
                contractID:contract.serialize()
                for contractID, contract in self.contracts.items()
            }
        }
    
    def logChg(self):
        self._master.changedAccts.add(self.mpid)

    def _resolveContract(self, contractID, value):
        if contractID in self.contracts:
            self.contracts[contractID].resolve(value)

    def placeOrder(self, _contractID, _price, _side, _qty):
        try:
            contractID = int(_contractID)
            price = int(_price)
            side = int(_side)
            qty = int(_qty)
        except:
            return {
                'callback':'800',
                'debug':'Contract ID, price, side and quantity must be integers'
            }

        if price < 1 or price > 99:
            return {
                'callback':'802', 
                'debug':'Order price must be between 1 to 99 (inclusive)'               
            }
        if not side in (0, 1):
            return {
                'callback':'803', 
                'debug':'Invaild order side'
            }
        if qty < 1:
            return {
                'callback':'804', 
                'debug':'Order quantity must be positive'
            }

        if not contractID in self.contracts:
            if not contractID in self._master.contracts:
                return {
                    'callback':'000', 
                    'debug': 'Contract does not exist'
                }

            self.contracts[contractID] = contract(
                _master = self, 
                _initData={
                    'contractID':contractID, 
                    'position':[0, 0], 
                    'reducible':[0, 0], 
                    'orders':[0, 0]
                }
            )
        
        return self.contracts[contractID].addOrder(price, side, qty)
    
    def removeOrder(self, orderID):
        try:
            orderID = int(orderID)
        except:
            return {
                'callback':'800', 
                'debug':'The order ID must be a number'
            }

        if orderID in self.orders:
            return self.orders[orderID].remove()
            

        return {
            'callback':'000', 
            'debug':'The order ID does not exist'
        }
    
    def queryContract(self, contractID):
        if not contractID in self.contracts:
            return {
                'callback':'000', 
                'debug': 'This account has not held this contract in the past'
            }
        
        return str(self.contracts[contractID])
