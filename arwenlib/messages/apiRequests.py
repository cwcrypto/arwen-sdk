from typing import List, Any, TypeVar, Callable, Type, cast, Optional


T = TypeVar("T")


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x

def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]

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


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class APIOuathRequest:
    exch_id: str

    def __init__(self, exch_id: str) -> None:
        self.exch_id = exch_id

    def to_dict(self) -> dict:
        result: dict = {}
        result["exchId"] = from_str(self.exch_id)
        return result


def api_ouath_request_from_dict(x: APIOuathRequest) -> Any:
    return to_class(APIOuathRequest, x)


class APIKYCStatusRequest:
    exch_id: str

    def __init__(self, exch_id: str) -> None:
        self.exch_id = exch_id

    def to_dict(self) -> dict:
        result: dict = {}
        result["exchId"] = from_str(self.exch_id)
        return result


def client_refresh_kyc_response_to_dict(x: APIKYCStatusRequest) -> Any:
    return to_class(APIKYCStatusRequest, x)


class APIRegisterKeys:
    exch_id: str
    api_key: str
    api_secret: str

    def __init__(self, exch_id: str, api_key: str, api_secret: str) -> None:
        self.exch_id = exch_id
        self.api_key = api_key
        self.api_secret = api_secret
    
    def to_dict(self) -> dict:
        result: dict = {}
        result["exch_id"] = from_str(self.exch_id)
        result["api_key"] = from_str(self.api_key)
        result["api_secret"] = from_str(self.api_secret)
        return result


def api_register_keys_to_dict(x: APIRegisterKeys) -> Any:
    return to_class(APIRegisterKeys, x)


class APIHistoryRequest:
    from_time: int

    def __init__(self, from_time: int) -> None:
        self.from_time = from_time

    def to_dict(self) -> dict:
        result: dict = {}
        result["startTime"] = from_int(self.from_time)
        return result


def api_history_request_to_dict(x: APIHistoryRequest) -> Any:
    return to_class(APIHistoryRequest, x)


class APIFilterRequest:
    id: Optional[str]
    from_time: Optional[int]
    limit: Optional[int]
    exch_id: Optional[str]
    is_final: Optional[bool]

    def __init__(self, id: Optional[str], from_time: Optional[int], limit: Optional[int], exch_id: Optional[str], is_final: Optional[bool]) -> None:
        self.id = id
        self.from_time = from_time
        self.limit = limit
        self.exch_id = exch_id
        self.is_final = is_final

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_union([from_str, from_none], self.id)
        result["fromTime"] = from_union([from_int, from_none], self.from_time)
        result["limit"] = from_union([from_int, from_none], self.limit)
        result["exchId"] = from_union([from_str, from_none], self.exch_id)
        result["isFinal"] = from_union([from_bool, from_none], self.is_final)
        return result


def api_filter_request_to_dict(x: APIFilterRequest) -> Any:
    return to_class(APIFilterRequest, x)


class APINewUserEscrowRequest:
    exch_id: str
    user_escrow_currency: str
    amount: float
    reserve_address: str
    expiry_time: int

    def __init__(self, exch_id: str, user_escrow_currency: str, qty: float, reserve_address: str, expiry_time: int) -> None:
        self.exch_id = exch_id
        self.user_escrow_currency = user_escrow_currency
        self.amount = qty
        self.reserve_address = reserve_address
        self.expiry_time = expiry_time

    def to_dict(self) -> dict:
        result: dict = {}
        result["exchId"] = from_str(self.exch_id)
        result["userEscrowCurrency"] = from_str(self.user_escrow_currency)
        result["amount"] = from_float(self.amount)
        result["reserveAddress"] = from_str(self.reserve_address)
        result["expiryTime"] = from_int(self.expiry_time)
        return result


def api_new_user_escrow_request_to_dict(x: APINewUserEscrowRequest) -> Any:
    return to_class(APINewUserEscrowRequest, x)


class APICloseUserEscrowRequest:
    user_escrow_id: int

    def __init__(self, user_escrow_id: int) -> None:
        self.user_escrow_id = user_escrow_id

    def to_dict(self) -> dict:
        result: dict = {}
        result["userEscrowId"] = from_str(str(self.user_escrow_id))
        return result


def api_close_user_escrow_request_to_dict(x: APICloseUserEscrowRequest) -> Any:
    return to_class(APICloseUserEscrowRequest, x)


class APIPriceExchangeEscrowRequest:
    exch_id: str
    exch_currency: str
    amount: float
    expiry_time: int
    user_currency: List[str]

    def __init__(self, exch_id: str, exch_currency: str, amount: int, expiry_time: int, user_currency: List[str]) -> None:
        self.exch_id = exch_id
        self.exch_currency = exch_currency
        self.amount = amount
        self.expiry_time = expiry_time
        self.user_currency = user_currency

    def to_dict(self) -> dict:
        result: dict = {}
        result["exchId"] = from_str(self.exch_id)
        result["exchCurrency"] = from_str(self.exch_currency)
        result["amount"] = from_int(self.amount)
        result["expiryTime"] = from_int(self.expiry_time)
        result["userCurrency"] = from_list(from_str, self.user_currency)
        return result

def api_price_exchange_escrow_request_to_dict(x: APIPriceExchangeEscrowRequest) -> Any:
    return to_class(APIPriceExchangeEscrowRequest, x)


class APIEscrowFeeRequest:
    exch_id: str
    exch_currency: str
    amount: float
    expiry_time: int
    user_currency: List[str]

    def __init__(self, exch_id: str, exch_currency: str, amount: float, expiry_time: int, user_currency: List[str]) -> None:
        self.exch_id = exch_id
        self.exch_currency = exch_currency
        self.amount = amount
        self.expiry_time = expiry_time
        self.user_currency = user_currency

    def to_dict(self) -> dict:
        result: dict = {}
        result["exchId"] = from_str(self.exch_id)
        result["exchCurrency"] = from_str(self.exch_currency)
        result["amount"] = from_float(self.amount)
        result["expiryTime"] = from_int(self.expiry_time)
        result["userCurrency"] = from_list(from_str, self.user_currency)
        return result


def api_escrow_fee_response_to_dict(x: APIEscrowFeeRequest) -> Any:
    return to_class(APIEscrowFeeRequest, x)

class APINewExchangeEscrowRequest:
    exch_id: str
    exch_currency: str
    amount: int
    expiry_time: int
    reserve_address: str
    user_escrow_id: int

    def __init__(self, exch_id: str, exch_currency: str, amount: int, expiry_time: int, reserve_address: str, user_escrow_id: int) -> None:
        self.exch_id = exch_id
        self.exch_currency = exch_currency
        self.amount = amount
        self.expiry_time = expiry_time
        self.reserve_address = reserve_address
        self.user_escrow_id = user_escrow_id

    def to_dict(self) -> dict:
        result: dict = {}
        result["exchId"] = from_str(self.exch_id)
        result["exchCurrency"] = from_str(self.exch_currency)
        result["amount"] = from_int(self.amount)
        result["expiryTime"] = from_int(self.expiry_time)
        result["reserveAddress"] = from_str(self.reserve_address)
        result["userEscrowId"] = from_str(str(self.user_escrow_id))
        return result


def api_new_exchange_escrow_request_to_dict(x: APINewExchangeEscrowRequest) -> Any:
    return to_class(APINewExchangeEscrowRequest, x)


class APICloseExchangeEscrowRequest:
    exch_escrow_id: int

    def __init__(self, exch_escrow_id: int) -> None:
        self.exch_escrow_id = exch_escrow_id


    def to_dict(self) -> dict:
        result: dict = {}
        result["exchEscrowId"] = from_str(str(self.exch_escrow_id))
        return result


def api_close_exchange_escrow_request_to_dict(x: APICloseExchangeEscrowRequest) -> Any:
    return to_class(APICloseExchangeEscrowRequest, x)


class APIOrderIDRequest:
    order_id: int

    def __init__(self, order_id: int) -> None:
        self.order_id = order_id

    def to_dict(self) -> dict:
        result: dict = {}
        result["orderId"] = from_str(str(self.order_id))
        return result


def api_order_id_request_to_dict(x: APIOrderIDRequest) -> Any:
    return to_class(APIOrderIDRequest, x)