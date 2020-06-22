# Mamba client exceptions
from typing import Optional


class MambaClientException(Exception):
    def __init__(self, msg: Optional[str] = None) -> None:
        super(MambaClientException,
              self).__init__(msg or "Mamba client command exception")
