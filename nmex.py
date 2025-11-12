from book import orderBook
from account import account

class NMEX:
    def __init__(self, _initData=None):
        if _initData is None:
            self.contracts = {}
            self.accounts = {}
        else:
            self.contracts = {
                contractID:orderBook(
                    _master = self, 
                    _initData = contractData)
                for contractID, contractData in _initData['contracts'].items()        
            }
        

            self.accounts = {
                accountID:account(
                    _master = self, 
                    _initData = acctData
                )
                for accountID, acctData in _initData['accounts'].items()
            }
        
        self.contractNameIDs = {}
        self.acctNameIDReferances = {}
        self.changedAccts = set()
    
    def serialize(self):
        accts = {
            acctID:acct.serialize()
            for acctID, acct in self.accounts.items()
        }

        contracts = {
            contractID:contract.serialize()
            for contractID, contract in self.contracts
        }
    
        return {
            'accounts':accts, 
            'contracts':contracts
        }
    
    def getAvblContractID(self):
        for i in range(0, 100):
            if not i in self.contracts:
                return i
        else:
            return False
        
    def checkAccount(self, mpid):
        try:
            mpid = int(mpid)
        except:
            return {
                'callback':'800', 
                'debug':'MPID Must be an integer'
            }
        
        if not mpid in self.accounts:
            return {
                'callback':'000', 
                'debug':'Account does not exist'
            }
        return None
    
    def checkAdmin(self, _mpid):
        try:
            mpid = int(_mpid)
        except:
            return {
                'callback':'800', 
                'debug':'MPID must be an integer'
            }
        
        if mpid == '-1':
            return None
        else:
            return {
                'callback':'998', 
                'debug':'Unauthorised - root access required.'
            }
    
    def createAccount(self, sudoMPID, accountID, acctName):
        adminCheck = self.checkAdmin(sudoMPID)
        if not adminCheck is None:
            return adminChecck
            
        try:
            acctID = int(accountID)
        except:
            return {
                'callback':'800', 
                'debug':'MPID must be an integer'
            }
        
        if acctID in self.accounts:
            return {
                'callback':'001'
            }

        self.accounts[acctID] = account(
            _master = self,
            _initData = {
                'mpid':acctID, 
                'acctName':str(acctName), 
                'contracts':{}
            }
        )

        return {
            'callback':'100', 
            'debug':'Account has been created successfully'
        }

    def createContract(self, acct, contractName):
        contractID = self.getAvblContractID()
        if contractID is False:
            return {
                'callback':000,
                'debug':'All contract slots has been taken'
            }
        
        if contractName in self.contractNameIDs:
            return {
                'callback':'001', 
                'debug':'The contract name is taken'
            }
        
        self.contracts[contractID] = orderBook(
            _master = self, 
            _initData = {
                'contractID':contractID, 
                'contractName':contractName
            }
        )
        
        return {
            'callback':100, 
            'debug':'contract creation successful'
        }

    def resolveContract(self, contrr):
        if 
    
    def addOrder(self, mpid, contractID, price, side, qty):
        callback = self.checkAccount(mpid)
        if callback is not None:
            return callback

        return self.accounts[int(mpid)].placeOrder(contractID, price, side, qty)
    
    def addOrderByContractName(self, mpid, contractName)

    def removeOrder(self, mpid, orderID):
        callback = self.checkAccount(mpid)
        if callback is not None:
            return callback
        
        return self.accounts[int(mpid)].removeOrder(orderID)
    
    