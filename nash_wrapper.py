
class NMEX_cli:
    def __init__(self, nmex):
        self.market = nmex
        commands = {
            'createaccount':nmex.createAccount, 
            'createaontract':nmex.createContract, 
            'lmt':nmex.placeOrder, 
            'rmvorder':nmex.removeOrder
        }
    
    # syntax:
    def parseCommand()