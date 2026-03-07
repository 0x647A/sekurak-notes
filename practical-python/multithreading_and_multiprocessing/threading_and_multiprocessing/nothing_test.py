import time


ALA_INTERVAL = 0.1    # seconds
MA_INTERVAL = 0.35    # seconds
KOTA_INTERVAL = 0.66  # seconds
LOOP_SLEEP = 0.01     # seconds


def run_event_loop(words: list[tuple[str, float]]) -> None:
    """Run a manual event loop, printing each word at its configured interval."""
    next_times = [time.monotonic() for _ in words]

    while True:
        now = time.monotonic()
        for i, (word, interval) in enumerate(words):
            if now >= next_times[i]:
                print(word)
                next_times[i] += interval
        time.sleep(LOOP_SLEEP)


if __name__ == "__main__":
    words = [
        ("ALA", ALA_INTERVAL),
        ("MA", MA_INTERVAL),
        ("KOTA", KOTA_INTERVAL),
    ]
    run_event_loop(words)
