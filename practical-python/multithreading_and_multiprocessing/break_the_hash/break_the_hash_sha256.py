import argparse
import hashlib
import string
import sys
from itertools import product


MAX_LENGTH = 8


def find_password(target_hash: str) -> str | None:
    """Brute-force a numeric password up to MAX_LENGTH digits against a SHA-256 hash."""
    for length in range(1, MAX_LENGTH + 1):
        for combo in product(string.digits, repeat=length):
            candidate = "".join(combo)
            if hashlib.sha256(candidate.encode(), usedforsecurity=False).hexdigest() == target_hash:
                return candidate
    return None


def main() -> None:
    parser = argparse.ArgumentParser(
        description=f"Brute-force SHA-256 hash (digits 0-9, length 1-{MAX_LENGTH})"
    )
    parser.add_argument("hash", help="Target SHA-256 hash to crack")
    args = parser.parse_args()

    result = find_password(args.hash)
    if result:
        print("Password found:", result)
    else:
        print("Password not found.")
        sys.exit(1)


if __name__ == "__main__":
    main()
