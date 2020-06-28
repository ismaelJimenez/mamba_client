# Mamba client exceptions
from typing import Optional


class MambaFlowException(Exception):
    def __init__(self, msg: Optional[str] = None) -> None:
        super().__init__(msg or "Mamba Flow exception")
