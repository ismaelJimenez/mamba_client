import enum


class OperatorLifecycle(enum.Enum):
    no_status = 0
    success = 1
    running = 2
    failed = 3
