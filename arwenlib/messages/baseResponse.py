# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = api_base_response_from_dict(json.loads(json_string))

from typing import List, Any, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


class APIBaseResponse:
    code: int
    data: str
    error: str

    def __init__(self, code: int, data: str, error: str) -> None:
        self.code = code
        self.data = data
        self.error = error

    @staticmethod
    def from_dict(obj: Any) -> 'APIBaseResponse':
        assert isinstance(obj, dict)
        code = from_int(obj.get("code"))
        data = from_str(obj.get("data"))
        error = from_str(obj.get("error"))
        return APIBaseResponse(code, data, error)


def api_base_response_from_dict(s: Any) -> APIBaseResponse:
    return APIBaseResponse.from_dict(s)

