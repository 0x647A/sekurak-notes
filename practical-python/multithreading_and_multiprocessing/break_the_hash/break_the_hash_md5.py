import argparse
import hashlib
import string
import sys
from itertools import product


LETTERS = string.ascii_uppercase
DIGITS = string.digits


def find_password(target_hash: str) -> str | None:
    """Brute-force a password in AAA9999 format (3 uppercase + 4 digits) against an MD5 hash."""
    for letter_part in product(LETTERS, repeat=3):
        for digit_part in product(DIGITS, repeat=4):
            candidate = "".join(letter_part) + "".join(digit_part)
            if hashlib.md5(candidate.encode(), usedforsecurity=False).hexdigest() == target_hash:
                return candidate
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Brute-force MD5 hash (password format: AAA9999)")
    parser.add_argument("hash", help="Target MD5 hash to crack")
    args = parser.parse_args()

    result = find_password(args.hash)
    if result:
        print("Password found:", result)
    else:
        print("Password not found.")
        sys.exit(1)


if __name__ == "__main__":
    main()
