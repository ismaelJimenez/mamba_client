import time


def log_info(source: str, msg: str) -> None:
    print(f'[INFO] [{time.strftime("%Y%m%dT%H%M%S")}] [{source}] {msg}')
