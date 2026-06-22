import logging
import sys
from pathlib import Path
from datetime import datetime

_LOG_DIR = Path(__file__).parent.parent / "logs"
_LOG_DIR.mkdir(exist_ok=True)

_loggers: dict = {}

_FORMATTER = logging.Formatter(
    fmt="[%(asctime)s] [%(levelname)-8s] [%(filename)s | %(funcName)s | line %(lineno)d]  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def get_logger(name: str) -> logging.Logger:
    if name in _loggers:
        return _loggers[name]

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    log_file = _LOG_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.log"
    fh = logging.FileHandler(log_file, mode="a", encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(_FORMATTER)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(_FORMATTER)

    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.propagate = False

    _loggers[name] = logger
    return logger
