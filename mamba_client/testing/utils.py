from typing import Optional, Any, List


class CallbackTestClass:
    """ Common class to test Subject callbacks """
    def __init__(self) -> None:
        self.func_1_calls: List[Any] = []
        self.func_2_calls: List[Any] = []

    def test_func_1(self, value: Optional[Any] = None) -> None:
        self.func_1_calls.append(value)

    def test_func_2(self, value: Optional[Any] = None) -> None:
        self.func_2_calls.append(value)
