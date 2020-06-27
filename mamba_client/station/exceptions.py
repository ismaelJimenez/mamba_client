# Mamba client exceptions
from typing import Optional


class MambaClientException(Exception):
    def __init__(self, msg: Optional[str] = None) -> None:
        super().__init__(msg or "Mamba client command exception")


class ParameterGetException(Exception):
    def __init__(self, msg: Optional[str] = None) -> None:
        super().__init__(msg or "Mamba client parameter get exception")


class ParameterSetException(Exception):
    def __init__(self, msg: Optional[str] = None) -> None:
        super().__init__(msg or "Mamba client parameter set exception")
