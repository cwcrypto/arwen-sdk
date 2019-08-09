import constants as c
import supportFunctions as sf


class orderDetails:
    def __init__(self):
        self.orderId = None
        self.params = dict().fromkeys(['userEscrowId', 'exchEscrowId', 'qty', 'side', 'symbol'])

        self.userEscrowId = None
        self.exchEscrowId = None
        self.type = sf.OrderType.rfq
        self.side = None
        self.symbol = None
        self.buyQty = None
        self.sellQty = None
        self.timeInForce = sf.timeInForce.fok
        self.price = None
        self.timeCreated = None
        self.timeExpiry = None
        self.timeClosed = None

    def createOrder(self, userEscrow, exchEscrow, qty, side):

        if not isinstance(side, sf.Side):
            raise TypeError('Invalid Side')

        self.userEscrowId = userEscrow.userEscrowId
        self.exchEscrowId = exchEscrow.exchEscrowId
        self.qty = str(qty)
        self.side = side
        self.symbol = sf.Symbol(exchEscrow.currency, userEscrow.currency).toString()

    def getRequest(self):
        self.params['userEscrowId'] = self.userEscrowId
        self.params['exchEscrowId'] = self.exchEscrowId
        self.params['qty'] = self.qty
        self.params['side'] = self.side.value # notice enum assignment here
        self.params['symbol'] = self.symbol

        return self.params
        

    # Build this after query endpoint is done
    def setFromQuery(self, resp):
        raise NotImplementedError('Please map resp to self.details')

    def updateOrderFromQuote(self, quote):
        self.orderId = quote['orderId']
        self.timeExpiry = int(quote['quoteExpiry'])
        self.buyQty = float(quote['buyQty'])
        self.sellQty = float(quote['sellQty'])
        self.price = float(self.buyQty / self.sellQty)
        self.buyCurrency = sf.Blockchain.FromString(quote['buyCurrency'])
        self.sellCurrency = sf.Blockchain.FromString(quote['sellCurrency'])


    def getOrderQuery(self, oid = None):
        if(self.orderId == None and oid == None):
            raise AttributeError('self.orderId is not set and no orderId given')
        elif (self.orderId != None and oid == None):
            params = dict()
            params['orderId'] = self.orderId
            return params
        elif (self.orderId == None and oid != None):
            params = dict()
            params['orderId'] = oid
            return params
        else:
            raise Exception('Ambiguous request for order details query')


class orderId():
    def __init__(self, oid):
        self.orderId = oid
        self.params = dict()
        self.params['orderId'] = oid

    def getRequest(self):
        return self.params

class priceInquiry():
    def __init__(self, ue, ee, qty, side):
        self.params = dict().fromkeys(['userEscrowId', 'exchEscrowId', 'qty', 'side'])
        self.params['userEscrowId'] = ue.userEscrowId
        self.params['exchEscrowId'] = ee.exchEscrowId
        self.params['qty'] = str(qty)
        self.params['side'] = side.value

    
    def getRequest(self):
        return self.params

    def setResponse(self, response):
        self.buyCurrency = response['buyCurrency']
        self.sellCurrency = response['sellCurrency']
        self.buyQty = response['buyQty']
        self.sellQty = response['sellQty']


def historyUserEscrows(startTime = None):

    endpoint = '/orders/history'

    queryParams = dict()
    queryParams['startTime'] = startTime

    orderIdList = sf.sendRequest(c.url, endpoint, queryParams)

    return orderIdList

def orderQueryDetails(orderId):

    endpoint = '/orders/details'

    order = orderDetails()
    params = order.getOrderQuery(orderId)

    order.setFromQuery(sf.sendRequest(c.url, endpoint, params))

    return order

def sellTrade(userEscrow, exchEscrow, qty):

    endpoint = '/orders/quote'

    order = orderDetails()
    order.createOrder(userEscrow, exchEscrow, qty, sf.Side.SELL)
    resp = sf.sendRequest(c.url, endpoint, order.getRequest())
    order.updateOrderFromQuote(resp)
    
    return order


def buyTrade(userEscrow, exchEscrow, qty):

    endpoint = '/orders/quote'

    order = orderDetails()
    order.createOrder(userEscrow, exchEscrow, qty, sf.Side.BUY)
    resp = sf.sendRequest(c.url, endpoint, order.getRequest())
    order.updateOrderFromQuote(resp)
    
    return order

def inquirePrice(userEscrow, exchEscrow, qty, side):

    endpoint = '/orders/inquiry'

    inquiry = priceInquiry(userEscrow, exchEscrow, qty, side)
    resp = sf.sendRequest(c.url, endpoint, inquiry.getRequest())
    inquiry.setResponse(resp)
    
    return inquiry

def execute(order):

    endpoint = '/orders/execute'
    
    req = orderId(order.orderId)
    resp = sf.sendRequest(c.url, endpoint, req.getRequest())

    return resp['executed']


def cancel(order):

    endpoint = '/orders/cancel'
    
    req = orderId(order.orderId)
    resp = sf.sendRequest(c.url, endpoint, req.getRequest())

    return resp['canceled']
