import argparse
import hashlib
import string
import sys
from itertools import product


MAX_LENGTH = 5


def find_password(target_hash: str) -> str | None:
    """Brute-force a lowercase password up to MAX_LENGTH characters against a SHA-1 hash."""
    for length in range(1, MAX_LENGTH + 1):
        for combo in product(string.ascii_lowercase, repeat=length):
            candidate = "".join(combo)
            if hashlib.sha1(candidate.encode(), usedforsecurity=False).hexdigest() == target_hash:
                return candidate
    return None


def main() -> None:
    parser = argparse.ArgumentParser(
        description=f"Brute-force SHA-1 hash (lowercase a-z, length 1-{MAX_LENGTH})"
    )
    parser.add_argument("hash", help="Target SHA-1 hash to crack")
    args = parser.parse_args()

    result = find_password(args.hash)
    if result:
        print("Password found:", result)
    else:
        print("Password not found.")
        sys.exit(1)


if __name__ == "__main__":
    main()
