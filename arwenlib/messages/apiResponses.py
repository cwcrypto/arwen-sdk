from typing import List, Any, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x

def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False

def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class APIHdseedResponse:
    hdseed: List[str]

    def __init__(self, hdseed: List[str]) -> None:
        self.hdseed = hdseed

    @staticmethod
    def from_dict(obj: Any) -> 'APIHdseedResponse':
        assert isinstance(obj, dict)
        hdseed = from_list(from_str, obj.get("hdseed"))
        return APIHdseedResponse(hdseed)


def api_hdseed_response_from_dict(s: Any) -> APIHdseedResponse:
    return APIHdseedResponse.from_dict(s)


class APIOuathResponse:
    oauth_url: str

    def __init__(self, oauth_url: str) -> None:
        self.oauth_url = oauth_url

    @staticmethod
    def from_dict(obj: Any) -> 'APIOuathResponse':
        assert isinstance(obj, dict)
        oauth_url = from_str(obj.get("oauthUrl"))
        return APIOuathResponse(oauth_url)


def api_ouath_response_from_dict(s: Any) -> APIOuathResponse:
    return APIOuathResponse.from_dict(s)


class APIKYCStatusResponse:
    exch_id: str
    kyc_status: str

    def __init__(self, exch_id: str, kyc_status: str) -> None:
        self.exch_id = exch_id
        self.kyc_status = kyc_status

    @staticmethod
    def from_dict(obj: Any) -> 'APIKYCStatusResponse':
        assert isinstance(obj, dict)
        exch_id = from_str(obj.get("exchId"))
        kyc_status = from_str(obj.get("kycStatus"))
        return APIKYCStatusResponse(exch_id, kyc_status)


def api_kyc_status_response(s: Any) -> APIKYCStatusResponse:
    return APIKYCStatusResponse.from_dict(s)


class APIEscrowFeeHistoryResponse:
    user_escrow_id: str
    user_escrow_currency: str
    user_escrow_amount: float
    exch_id: str
    exch_escrow_id: str
    time_paid: int

    def __init__(self, user_escrow_id: str, user_escrow_currency: str, user_escrow_amount: float, exch_id: str, exch_escrow_id: str, time_paid: int) -> None:
        self.user_escrow_id = user_escrow_id
        self.user_escrow_currency = user_escrow_currency
        self.user_escrow_amount = user_escrow_amount
        self.exch_id = exch_id
        self.exch_escrow_id = exch_escrow_id
        self.time_paid = time_paid

    @staticmethod
    def from_dict(obj: Any) -> 'APIEscrowFeeHistoryResponse':
        assert isinstance(obj, dict)
        user_escrow_id = from_str(obj.get("userEscrowId"))
        user_escrow_currency = from_str(obj.get("userEscrowCurrency"))
        user_escrow_amount = from_float(obj.get("userEscrowAmount"))
        exch_id = from_str(obj.get("exchId"))
        exch_escrow_id = from_str(obj.get("exchEscrowId"))
        time_paid = from_int(obj.get("timePaid"))
        return APIEscrowFeeHistoryResponse(user_escrow_id, user_escrow_currency, user_escrow_amount, exch_id, exch_escrow_id, time_paid)


def api_escrow_fee_history_from_dict(s: Any) -> List[APIEscrowFeeHistoryResponse]:
    return from_list(APIEscrowFeeHistoryResponse.from_dict, s)


class APIUserEscrowElement:
    exch_id: str
    user_escrow_id: str
    escrow_address: str
    state: str
    amount: float
    available_to_trade: float
    user_escrow_currency: str
    trades: List[str]
    amount_sent_to_user_reserve: float
    time_created: int
    time_closed: int
    amount_to_fund: float
    funding_address: str

    def __init__(self, exch_id: str, user_escrow_id: str, escrow_address: str, state: str, amount: float, available_to_trade: float, user_escrow_currency: str, trades: List[str], amount_sent_to_user_reserve: float, time_created: int, time_closed: int, amount_to_fund: float, funding_address: str) -> None:
        self.exch_id = exch_id
        self.user_escrow_id = user_escrow_id
        self.escrow_address = escrow_address
        self.state = state
        self.amount = amount
        self.available_to_trade = available_to_trade
        self.user_escrow_currency = user_escrow_currency
        self.trades = trades
        self.amount_sent_to_user_reserve = amount_sent_to_user_reserve
        self.time_created = time_created
        self.time_closed = time_closed
        self.amount_to_fund = amount_to_fund
        self.funding_address = funding_address

    @staticmethod
    def from_dict(obj: Any) -> 'APIUserEscrowElement':
        assert isinstance(obj, dict)
        exch_id = from_str(obj.get("exchId"))
        user_escrow_id = from_str(obj.get("userEscrowId"))
        escrow_address = from_str(obj.get("escrowAddress"))
        state = from_str(obj.get("state"))
        amount = from_float(obj.get("amount"))
        available_to_trade = from_float(obj.get("availableToTrade"))
        user_escrow_currency = from_str(obj.get("userEscrowCurrency"))
        trades = from_list(from_str, obj.get("trades"))
        amount_sent_to_user_reserve = from_float(obj.get("amountSentToUserReserve"))
        time_created = from_int(obj.get("timeCreated"))
        time_closed = from_int(obj.get("timeClosed"))
        amount_to_fund = from_float(obj.get("amountToFund"))
        funding_address = from_str(obj.get("fundingAddress"))
        return APIUserEscrowElement(exch_id, user_escrow_id, escrow_address, state, amount, available_to_trade, user_escrow_currency, trades, amount_sent_to_user_reserve, time_created, time_closed, amount_to_fund, funding_address)

def api_user_escrow_from_dict(s: Any) -> List[APIUserEscrowElement]:
    return from_list(APIUserEscrowElement.from_dict, s)


class APINewUserEscrowResponse:
    user_escrow_id: str
    funding_address: str
    amount_to_fund: float

    def __init__(self, user_escrow_id: str, funding_address: str, amount_to_fund: float) -> None:
        self.user_escrow_id = user_escrow_id
        self.funding_address = funding_address
        self.amount_to_fund = amount_to_fund

    @staticmethod
    def from_dict(obj: Any) -> 'APINewUserEscrowResponse':
        assert isinstance(obj, dict)
        user_escrow_id = from_str(obj.get("userEscrowId"))
        fundingAddress = from_str(obj.get("fundingAddress"))
        amount_to_fund = from_float(obj.get("amountToFund"))
        return APINewUserEscrowResponse(user_escrow_id, fundingAddress, amount_to_fund)


def api_new_user_escrow_response_from_dict(s: Any) -> APINewUserEscrowResponse:
    return APINewUserEscrowResponse.from_dict(s)

class APICloseEscrowResponse:
    closed: bool

    def __init__(self, closed: bool) -> None:
        self.closed = closed

    @staticmethod
    def from_dict(obj: Any) -> 'APICloseEscrowResponse':
        assert isinstance(obj, dict)
        closed = from_bool(obj.get("closed"))
        return APICloseEscrowResponse(closed)


def api_close_escrow_response_from_dict(s: Any) -> APICloseEscrowResponse:
    return APICloseEscrowResponse.from_dict(s)


class APIEscrowFeeResponse:
    currency: str
    amount: float

    def __init__(self, currency: str, amount: float) -> None:
        self.currency = currency
        self.amount = amount

    @staticmethod
    def from_dict(obj: Any) -> 'APIEscrowFeeResponse':
        assert isinstance(obj, dict)
        currency = from_str(obj.get("currency"))
        amount = from_float(obj.get("amount"))
        return APIEscrowFeeResponse(currency, amount)

    def to_dict(self) -> dict:
        result: dict = {}
        result["currency"] = from_str(self.currency)
        result["amount"] = to_float(self.amount)
        return result


def api_escrow_fee_response_from_dict(s: Any) -> List[APIEscrowFeeResponse]:
    return from_list(APIEscrowFeeResponse.from_dict, s)


class APIExchangeEscrowElement:
    exch_id: str
    exch_escrow_id: str
    escrow_address: str
    state: str
    amount: float
    available_to_trade: float
    exch_escrow_currency: str
    trades: List[int]
    amount_sent_to_user_reserve: float
    time_created: int
    time_closed: int

    def __init__(self, exch_id: str, exch_escrow_id: str, escrow_address: str, state: str, amount: float, available_to_trade: float, exch_escrow_currency: str, trades: List[int], amount_sent_to_user_reserve: float, time_created: int, time_closed: int) -> None:
        self.exch_id = exch_id
        self.exch_escrow_id = exch_escrow_id
        self.escrow_address = escrow_address
        self.state = state
        self.amount = amount
        self.available_to_trade = available_to_trade
        self.exch_escrow_currency = exch_escrow_currency
        self.trades = trades
        self.amount_sent_to_user_reserve = amount_sent_to_user_reserve
        self.time_created = time_created
        self.time_closed = time_closed

    @staticmethod
    def from_dict(obj: Any) -> 'APIExchangeEscrowElement':
        assert isinstance(obj, dict)
        exch_id = from_str(obj.get("exchId"))
        exch_escrow_id = from_str(obj.get("exchEscrowId"))
        escrow_address = from_union([from_str, from_none], obj.get("escrowAddress"))
        state = from_str(obj.get("state"))
        amount = from_float(obj.get("amount"))
        available_to_trade = from_float(obj.get("availableToTrade"))
        exch_escrow_currency = from_str(obj.get("exchEscrowCurrency"))
        trades = from_list(lambda x: from_str(x), obj.get("trades"))
        amount_sent_to_user_reserve = from_float(obj.get("amountSentToUserReserve"))
        time_created = from_int(obj.get("timeCreated"))
        time_closed = from_int(obj.get("timeClosed"))
        return APIExchangeEscrowElement(exch_id, exch_escrow_id, escrow_address, state, amount, available_to_trade, exch_escrow_currency, trades, amount_sent_to_user_reserve, time_created, time_closed)


def api_exchange_escrow_from_dict(s: Any) -> List[APIExchangeEscrowElement]:
    return from_list(APIExchangeEscrowElement.from_dict, s)


class APINewExchangeEscrowResponse:
    exch_escrow_id: str
    escrow_address: str
    escrow_fee_paid: float

    def __init__(self, exch_escrow_id: str, escrow_address: str, escrow_fee_paid: float) -> None:
        self.exch_escrow_id = exch_escrow_id
        self.escrow_address = escrow_address
        self.escrow_fee_paid = escrow_fee_paid

    @staticmethod
    def from_dict(obj: Any) -> 'APINewExchangeEscrowResponse':
        assert isinstance(obj, dict)
        exch_escrow_id = from_str(obj.get("exchEscrowId"))
        escrow_address = from_union([from_str, from_none], obj.get("escrowAddress"))
        escrow_fee_paid = from_float(obj.get("escrowFeePaid"))
        return APINewExchangeEscrowResponse(exch_escrow_id, escrow_address, escrow_fee_paid)


def api_new_exchange_escrow_response_from_dict(s: Any) -> APINewExchangeEscrowResponse:
    return APINewExchangeEscrowResponse.from_dict(s)



class ApiOrderExecutedResponse:
    executed: bool

    def __init__(self, executed: bool) -> None:
        self.executed = executed

    @staticmethod
    def from_dict(obj: Any) -> 'APINewExchangeEscrowRequest':
        assert isinstance(obj, dict)
        executed = from_bool(obj.get("executed"))
        return ApiOrderExecutedResponse(executed)


def api_order_executed_response_from_dict(s: Any) -> ApiOrderExecutedResponse:
    return ApiOrderExecutedResponse.from_dict(s)

class ApiOrderCanceledResponse:
    canceled: bool

    def __init__(self, canceled: bool) -> None:
        self.canceled = canceled

    @staticmethod
    def from_dict(obj: Any) -> 'ApiOrderCanceledResponse':
        assert isinstance(obj, dict)
        canceled = from_bool(obj.get("canceled"))
        return ApiOrderCanceledResponse(canceled)


def api_order_canceled_response_from_dict(s: Any) -> ApiOrderCanceledResponse:
    return ApiOrderCanceledResponse.from_dict(s)


class APIOrderResponseElement:
    order_id: str
    orderType: str
    state: str
    symbol: str
    price: float
    user_escrow_amount: float
    exch_escrow_amount: float
    side: str
    user_escrow_id: str
    exch_escrow_id: str
    time_created: int
    time_closed: int

    def __init__(self, order_id: str, orderType: str, state: str, symbol: str, price: float, user_escrow_amount: float, exch_escrow_amount: float, side: str, user_escrow_id: str, exch_escrow_id: str, time_created: int, time_closed: int) -> None:
        self.order_id = order_id
        self.orderType = orderType
        self.state = state
        self.symbol = symbol
        self.price = price
        self.user_escrow_amount = user_escrow_amount
        self.exch_escrow_amount = exch_escrow_amount
        self.side = side
        self.user_escrow_id = user_escrow_id
        self.exch_escrow_id = exch_escrow_id
        self.time_created = time_created
        self.time_closed = time_closed

    @staticmethod
    def from_dict(obj: Any) -> 'APIOrderResponseElement':
        assert isinstance(obj, dict)
        order_id = from_str(obj.get("orderId"))
        orderType = from_str(obj.get("type"))
        state = from_str(obj.get("state"))
        symbol = from_str(obj.get("symbol"))
        price = from_float(obj.get("price"))
        user_escrow_amount = from_float(obj.get("userEscrowAmount"))
        exch_escrow_amount = from_float(obj.get("exchEscrowAmount"))
        side = from_str(obj.get("side"))
        user_escrow_id = from_str(obj.get("userEscrowId"))
        exch_escrow_id = from_str(obj.get("exchEscrowId"))
        time_created = from_int(obj.get("timeCreated"))
        time_closed = from_float(obj.get("timeClosed"))
        return APIOrderResponseElement(order_id, orderType, state, symbol, price, user_escrow_amount, exch_escrow_amount, side, user_escrow_id, exch_escrow_id, time_created, time_closed)


def api_order_query_response_from_dict(s: Any) -> List[APIOrderResponseElement]:
    return from_list(APIOrderResponseElement.from_dict, s)


class APIPlaceOrderResponse:
    order_id: str
    user_escrow_id: str
    exch_escrow_id: str
    buy_currency: str
    sell_currency: str
    price: float
    buy_amount: float
    sell_amount: float
    quote_expiry: int

    def __init__(self, order_id: str, user_escrow_id: str, exch_escrow_id: str, buy_currency: str, sell_currency: str, price: float, buy_amount: float, sell_amount: float, quote_expiry: int) -> None:
        self.order_id = order_id
        self.user_escrow_id = user_escrow_id
        self.exch_escrow_id = exch_escrow_id
        self.buy_currency = buy_currency
        self.sell_currency = sell_currency
        self.price = price
        self.buy_amount = buy_amount
        self.sell_amount = sell_amount
        self.quote_expiry = quote_expiry

    @staticmethod
    def from_dict(obj: Any) -> 'APIPlaceOrderResponse':
        assert isinstance(obj, dict)
        order_id = from_str(obj.get("orderId"))
        user_escrow_id = from_str(obj.get("userEscrowId"))
        exch_escrow_id = from_str(obj.get("exchEscrowId"))
        buy_currency = from_str(obj.get("buyCurrency"))
        sell_currency = from_str(obj.get("sellCurrency"))
        price = from_union([from_float, from_none], obj.get("price"))
        buy_amount = from_float(obj.get("buyAmount"))
        sell_amount = from_float(obj.get("sellAmount"))
        quote_expiry = from_int(obj.get("quoteExpiry"))
        return APIPlaceOrderResponse(order_id, user_escrow_id, exch_escrow_id, buy_currency, sell_currency, price, buy_amount, sell_amount, quote_expiry)


def api_place_order_response_from_dict(s: Any) -> APIPlaceOrderResponse:
    return APIPlaceOrderResponse.from_dict(s)


class APIOrderInquiryResponse:
    buy_currency: str
    sell_currency: str
    buy_amount: float
    sell_amount: float

    def __init__(self, buy_currency: str, sell_currency: str, buy_amount: float, sell_amount: float) -> None:
        self.buy_currency = buy_currency
        self.sell_currency = sell_currency
        self.buy_amount = buy_amount
        self.sell_amount = sell_amount

    @staticmethod
    def from_dict(obj: Any) -> 'APIOrderInquiryResponse':
        assert isinstance(obj, dict)
        buy_currency = from_str(obj.get("buyCurrency"))
        sell_currency = from_str(obj.get("sellCurrency"))
        buy_amount = from_float(obj.get("buyAmount"))
        sell_amount = from_float(obj.get("sellAmount"))
        return APIOrderInquiryResponse(buy_currency, sell_currency, buy_amount, sell_amount)


def api_order_inquiry_response_from_dict(s: Any) -> APIOrderInquiryResponse:
    return APIOrderInquiryResponse.from_dict(s)
