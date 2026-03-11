import argparse
import hashlib
import sys
from pathlib import Path


def find_password(target_hash: str, wordlist_path: Path) -> str | None:
    """Find a password from a wordlist that matches the given SHA-384 hash."""
    with open(wordlist_path, "r", encoding="utf-8") as f:
        for line in f:
            word = line.strip()
            if hashlib.sha384(word.encode(), usedforsecurity=False).hexdigest() == target_hash:
                return word
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Crack a SHA-384 hash using a wordlist")
    parser.add_argument("hash", help="Target SHA-384 hash to crack")
    parser.add_argument(
        "--wordlist",
        type=Path,
        default=Path("wordlist.txt"),
        help="Path to the wordlist file (default: wordlist.txt)",
    )
    args = parser.parse_args()

    try:
        result = find_password(args.hash, args.wordlist)
    except FileNotFoundError:
        print(f"Error: wordlist file '{args.wordlist}' not found.")
        sys.exit(1)

    if result:
        print("Password found:", result)
    else:
        print("Password not found.")
        sys.exit(1)


if __name__ == "__main__":
    main()
