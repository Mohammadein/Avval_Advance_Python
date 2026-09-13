import logging


def setup_logging() -> None:
    logging.basicConfig(
        filename="note_manager.log",
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        encoding="utf-8",
    )