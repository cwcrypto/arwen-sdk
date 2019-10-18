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


class APIKeyRegResponse:
    status: bool

    def __init__(self, status: bool) -> None:
        self.status = status

    @staticmethod
    def from_dict(obj: Any) -> 'APIKeyRegResponse':
        assert isinstance(obj, dict)
        status = from_bool(obj.get("status"))
        return APIKeyRegResponse(status)


def api_key_reg_response_from_dict(s: Any) -> APIKeyRegResponse:
    return APIKeyRegResponse.from_dict(s)


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


class ClientRefreshKYCResponse:
    exch_id: str
    kyc_status: str

    def __init__(self, exch_id: str, kyc_status: str) -> None:
        self.exch_id = exch_id
        self.kyc_status = kyc_status

    @staticmethod
    def from_dict(obj: Any) -> 'ClientRefreshKYCResponse':
        assert isinstance(obj, dict)
        exch_id = from_str(obj.get("exchId"))
        kyc_status = from_str(obj.get("kycStatus"))
        return ClientRefreshKYCResponse(exch_id, kyc_status)

def client_refresh_kyc_response_from_dict(s: Any) -> ClientRefreshKYCResponse:
    return ClientRefreshKYCResponse.from_dict(s)


class APIEscrowFeeHistoryResponse:
    user_escrow_id: str
    user_escrow_currency: str
    user_escrow_qty: float
    exch_id: str
    exch_escrow_id: str
    time_paid: int

    def __init__(self, user_escrow_id: str, user_escrow_currency: str, user_escrow_qty: float, exch_id: str, exch_escrow_id: str, time_paid: int) -> None:
        self.user_escrow_id = user_escrow_id
        self.user_escrow_currency = user_escrow_currency
        self.user_escrow_qty = user_escrow_qty
        self.exch_id = exch_id
        self.exch_escrow_id = exch_escrow_id
        self.time_paid = time_paid

    @staticmethod
    def from_dict(obj: Any) -> 'APIEscrowFeeHistoryResponse':
        assert isinstance(obj, dict)
        user_escrow_id = from_str(obj.get("userEscrowId"))
        user_escrow_currency = from_str(obj.get("userEscrowCurrency"))
        user_escrow_qty = from_float(obj.get("userEscrowQty"))
        exch_id = from_str(obj.get("exchId"))
        exch_escrow_id = from_str(obj.get("exchEscrowId"))
        time_paid = from_int(obj.get("timePaid"))
        return APIEscrowFeeHistoryResponse(user_escrow_id, user_escrow_currency, user_escrow_qty, exch_id, exch_escrow_id, time_paid)


def fees_from_dict(s: Any) -> List[APIEscrowFeeHistoryResponse]:
    return from_list(APIEscrowFeeHistoryResponse.from_dict, s)


class APIUserEscrowElement:
    exch_id: str
    user_escrow_id: int
    escrow_address: str
    state: str
    amount: float
    available_to_trade: float
    user_escrow_currency: str
    trades: List[int]
    amount_sent_to_reserve: float
    time_created: int
    time_closed: int

    def __init__(self, exch_id: str, user_escrow_id: int, escrow_address: str, state: str, amount: float, available_to_trade: float, user_escrow_currency: str, trades: List[int], amount_sent_to_reserve: float, time_created: int, time_closed: int) -> None:
        self.exch_id = exch_id
        self.user_escrow_id = user_escrow_id
        self.escrow_address = escrow_address
        self.state = state
        self.amount = amount
        self.available_to_trade = available_to_trade
        self.user_escrow_currency = user_escrow_currency
        self.trades = trades
        self.amount_sent_to_reserve = amount_sent_to_reserve
        self.time_created = time_created
        self.time_closed = time_closed

    @staticmethod
    def from_dict(obj: Any) -> 'APIUserEscrowElement':
        assert isinstance(obj, dict)
        exch_id = from_str(obj.get("exchId"))
        user_escrow_id = int(from_str(obj.get("userEscrowId")))
        escrow_address = from_str(obj.get("escrowAddress"))
        state = from_str(obj.get("state"))
        amount = from_float(obj.get("amount"))
        available_to_trade = from_float(obj.get("availableToTrade"))
        user_escrow_currency = from_str(obj.get("userEscrowCurrency"))
        trades = from_list(lambda x: int(from_str(x)), obj.get("trades"))
        amount_sent_to_reserve = from_float(obj.get("amountSentToReserve"))
        time_created = from_int(obj.get("timeCreated"))
        time_closed = from_int(obj.get("timeClosed"))
        return APIUserEscrowElement(exch_id, user_escrow_id, escrow_address, state, amount, available_to_trade, user_escrow_currency, trades, amount_sent_to_reserve, time_created, time_closed)


def api_user_escrow_details_from_dict(s: Any) -> List[APIUserEscrowElement]:
    return from_list(APIUserEscrowElement.from_dict, s)


class APINewUserEscrowResponse:
    user_escrow_id: int
    escrow_address: str
    amount_to_fund: float

    def __init__(self, user_escrow_id: int, escrow_address: str, amount_to_fund: float) -> None:
        self.user_escrow_id = user_escrow_id
        self.escrow_address = escrow_address
        self.amount_to_fund = amount_to_fund

    @staticmethod
    def from_dict(obj: Any) -> 'APINewUserEscrowResponse':
        assert isinstance(obj, dict)
        user_escrow_id = int(from_str(obj.get("userEscrowId")))
        escrow_address = from_str(obj.get("escrowAddress"))
        amount_to_fund = from_float(obj.get("amountToFund"))
        return APINewUserEscrowResponse(user_escrow_id, escrow_address, amount_to_fund)


def api_new_user_escrow_response_from_dict(s: Any) -> APINewUserEscrowResponse:
    return APINewUserEscrowResponse.from_dict(s)

class APICloseEscrowResponse:
    close: bool

    def __init__(self, close: bool) -> None:
        self.close = close

    @staticmethod
    def from_dict(obj: Any) -> 'APICloseEscrowResponse':
        assert isinstance(obj, dict)
        close = from_bool(obj.get("close"))
        return APICloseEscrowResponse(close)


def api_close_user_escrow_rsponse_from_dict(s: Any) -> APICloseEscrowResponse:
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
    exch_escrow_id: int
    escrow_address: str
    state: str
    amount: float
    available_to_trade: float
    exch_escrow_currency: str
    trades: List[int]
    amount_sent_to_reserve: float
    time_created: int
    time_closed: int

    def __init__(self, exch_id: str, exch_escrow_id: int, escrow_address: str, state: str, amount: float, available_to_trade: float, exch_escrow_currency: str, trades: List[int], amount_sent_to_reserve: float, time_created: int, time_closed: int) -> None:
        self.exch_id = exch_id
        self.exch_escrow_id = exch_escrow_id
        self.escrow_address = escrow_address
        self.state = state
        self.amount = amount
        self.available_to_trade = available_to_trade
        self.exch_escrow_currency = exch_escrow_currency
        self.trades = trades
        self.amount_sent_to_reserve = amount_sent_to_reserve
        self.time_created = time_created
        self.time_closed = time_closed

    @staticmethod
    def from_dict(obj: Any) -> 'APIExchangeEscrowElement':
        assert isinstance(obj, dict)
        exch_id = from_str(obj.get("exchId"))
        exch_escrow_id = int(from_str(obj.get("exchEscrowId")))
        escrow_address = from_str(obj.get("escrowAddress"))
        state = from_str(obj.get("state"))
        amount = from_float(obj.get("amount"))
        available_to_trade = from_float(obj.get("availableToTrade"))
        exch_escrow_currency = from_str(obj.get("exchEscrowCurrency"))
        trades = from_list(lambda x: int(from_str(x)), obj.get("trades"))
        amount_sent_to_reserve = from_float(obj.get("amountSentToReserve"))
        time_created = from_int(obj.get("timeCreated"))
        time_closed = from_int(obj.get("timeClosed"))
        return APIExchangeEscrowElement(exch_id, exch_escrow_id, escrow_address, state, amount, available_to_trade, exch_escrow_currency, trades, amount_sent_to_reserve, time_created, time_closed)


def api_exchange_escrow_from_dict(s: Any) -> List[APIExchangeEscrowElement]:
    return from_list(APIExchangeEscrowElement.from_dict, s)


class ApiOrderExecutedResponse:
    executed: bool

    def __init__(self, executed: bool) -> None:
        self.executed = executed

    @staticmethod
    def from_dict(obj: Any) -> 'APINewExchangeEscrowRequest':
        assert isinstance(obj, dict)
        executed = from_bool(obj.get("executed"))
        return ApiOrderExecutedResponse(executed)


def api_new_exchange_escrow_request_from_dict(s: Any) -> ApiOrderExecutedResponse:
    return ApiOrderExecutedResponse.from_dict(s)


class APIOrderResponseElement:
    order_id: str
    type: str
    state: str
    symbol: str
    price: float
    user_escrow_amount: float
    exch_escrow_amount: float
    side: str
    user_escrow_id: str
    exch_escrow_id: str
    time_created: int
    time_closed: float

    def __init__(self, order_id: str, type: str, state: str, symbol: str, price: float, user_escrow_amount: float, exch_escrow_amount: float, side: str, user_escrow_id: str, exch_escrow_id: str, time_created: int, time_closed: float) -> None:
        self.order_id = order_id
        self.type = type
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
        type = from_str(obj.get("type"))
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
        return APIOrderResponseElement(order_id, type, state, symbol, price, user_escrow_amount, exch_escrow_amount, side, user_escrow_id, exch_escrow_id, time_created, time_closed)


def api_order_response_from_dict(s: Any) -> List[APIOrderResponseElement]:
    return from_list(APIOrderResponseElement.from_dict, s)