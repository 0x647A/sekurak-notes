import multiprocessing
import time


ALA_INTERVAL = 0.1    # seconds
MA_INTERVAL = 0.35    # seconds
KOTA_INTERVAL = 0.66  # seconds


def print_word(word: str, interval: float) -> None:
    """Print a word repeatedly at the given interval."""
    while True:
        print(word)
        time.sleep(interval)


if __name__ == "__main__":
    words = [
        ("ALA", ALA_INTERVAL),
        ("MA", MA_INTERVAL),
        ("KOTA", KOTA_INTERVAL),
    ]
    for word, interval in words:
        multiprocessing.Process(target=print_word, args=(word, interval), daemon=True).start()

    while True:
        time.sleep(1)
