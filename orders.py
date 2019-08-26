import constants as c
import supportFunctions as sf


class orderDetails:
    def __init__(self):
        self.orderId = None
        self.params = dict().fromkeys(['userEscrowId', 'exchEscrowId', 'qty', 'side', 'symbol'])

        self.userEscrowId = None
        self.exchEscrowId = None
        self.type = sf.OrderType.RFQ
        self.side = None
        self.symbol = None
        self.exchEscrowQty = None
        self.userEscrowQty = None
        self.timeInForce = sf.timeInForce.FOK
        self.price = None           # Not used at the moment
        self.timeCreated = None
        self.timeExpiry = None
        self.timeClosed = None

    def setupOrder(self, userEscrow, exchEscrow, qty, side):

        if not isinstance(side, sf.Side):
            raise TypeError('Invalid Side')

        self.userEscrowId = userEscrow.escrowId
        self.exchEscrowId = exchEscrow.escrowId
        self.qty = qty
        self.side = side
        self.symbol = sf.Symbol(exchEscrow.currency, userEscrow.currency)

    def setFromOrderEscrowId(self, orderId):
        self.orderId = orderId
        self.updateOrderDetails()
        return self

    def getRequest(self):
        self.params['userEscrowId'] = self.userEscrowId
        self.params['exchEscrowId'] = self.exchEscrowId
        self.params['qty'] = str(self.qty)
        self.params['side'] = self.side.value
        self.params['symbol'] = self.symbol.toString()

        return self.params
        
    def updateOrderFromQuote(self, quote):
        self.orderId = quote['orderId']
        self.timeExpiry = int(quote['quoteExpiry'])
        self.exchEscrowQty = float(quote['buyQty'])
        self.userEscrowQty = float(quote['sellQty'])
        self.price = float(self.exchEscrowQty / self.userEscrowQty)
        self.buyCurrency = sf.Blockchain(quote['buyCurrency'])
        self.sellCurrency = sf.Blockchain(quote['sellCurrency'])

    def updateFromQuery(self, query):
        self.type = sf.OrderType(query['type'])
        self.state = sf.OrderState(query['state'])
        self.symbol = sf.Symbol('','').fromString(query['symbol'])
        self.exchEscrowQty = float(query['exchEscrowQty'])
        self.userEscrowQty = float(query['userEscrowQty'])
        self.price = float(self.exchEscrowQty / self.userEscrowQty)
        self.exchEscrowId = query['exchEscrowId']
        self.userEscrowId = query['userEscrowId']
        self.side = sf.Side(query['side'])
        self.timeCreated = int(query['timeCreated'])
        self.timeClosed = int(query['timeClosed'])

    def updateOrderDetails(self):
        orderUpdate = queryOrderDetails(self)
        self.updateFromQuery(orderUpdate)


class priceInquiry():
    def __init__(self, ue, ee, qty, side):
        self.params = dict().fromkeys(['userEscrowId', 'exchEscrowId', 'qty', 'side'])
        self.params['userEscrowId'] = ue.userEscrowId
        self.params['exchEscrowId'] = ee.exchEscrowId
        self.params['qty'] = str(qty)
        self.params['side'] = side.value
    
    def getRequest(self):
        return self.params

    def setFromInquiry(self, response):
        self.buyCurrency = response['buyCurrency']
        self.sellCurrency = response['sellCurrency']
        self.buyQty = response['buyQty']
        self.sellQty = response['sellQty']


def ordersHistory(startTime = None):

    endpoint = '/orders/history'

    queryParams = dict()
    queryParams['startTime'] = startTime

    orderIdList = sf.sendRequest(c.url, endpoint, queryParams)

    return orderIdList

def queryOrderDetails(order):

    endpoint = '/orders/details'

    params = dict()
    params['orderId'] = order.orderId

    order.updateFromQuery(sf.sendRequest(c.url, endpoint, params))

    return order

def sellTrade(userEscrow, exchEscrow, qty):

    endpoint = '/orders/quote'

    order = orderDetails()
    order.setupOrder(userEscrow, exchEscrow, qty, sf.Side.SELL)
    resp = sf.sendRequest(c.url, endpoint, order.getRequest())
    order.updateOrderFromQuote(resp)
    
    return order


def buyTrade(userEscrow, exchEscrow, qty):

    endpoint = '/orders/quote'

    order = orderDetails()
    order.setupOrder(userEscrow, exchEscrow, qty, sf.Side.BUY)
    resp = sf.sendRequest(c.url, endpoint, order.getRequest())
    order.updateOrderFromQuote(resp)
    
    return order

def inquirePrice(userEscrow, exchEscrow, qty, side):

    endpoint = '/orders/inquiry'

    inquiry = priceInquiry(userEscrow, exchEscrow, qty, side)
    resp = sf.sendRequest(c.url, endpoint, inquiry.getRequest())
    inquiry.setFromInquiry(resp)
    
    return inquiry

def execute(order):

    endpoint = '/orders/execute'
    
    params = dict()
    params['orderId'] = order.orderId

    resp = sf.sendRequest(c.url, endpoint, params)

    return resp['executed']


def cancel(order):

    endpoint = '/orders/cancel'
    
    params = dict()
    params['orderId'] = order.orderId

    resp = sf.sendRequest(c.url, endpoint, params)

    return resp['canceled']
