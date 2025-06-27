import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


def log_event(event_type: str, details: str) -> None:
    logging.info("%s - %s", event_type, details)
