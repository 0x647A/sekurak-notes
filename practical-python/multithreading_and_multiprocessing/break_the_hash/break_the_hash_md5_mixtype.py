import argparse
import hashlib
import sys
from pathlib import Path


def load_wordlist(wordlist_path: Path) -> list[str]:
    """Load and return non-empty words from the wordlist file."""
    with open(wordlist_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def find_password(target_hash: str, words: list[str]) -> str | None:
    """Find a password in word1+word2+NN format that matches the given MD5 hash."""
    for word1 in words:
        for word2 in words:
            for suffix in range(100):
                candidate = f"{word1}{word2}{suffix:02d}"
                if hashlib.md5(candidate.encode(), usedforsecurity=False).hexdigest() == target_hash:
                    return candidate
    return None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Crack an MD5 hash (password format: word1+word2+NN)"
    )
    parser.add_argument("hash", help="Target MD5 hash to crack")
    parser.add_argument(
        "--wordlist",
        type=Path,
        default=Path("wordlist.txt"),
        help="Path to the wordlist file (default: wordlist.txt)",
    )
    args = parser.parse_args()

    try:
        words = load_wordlist(args.wordlist)
    except FileNotFoundError:
        print(f"Error: wordlist file '{args.wordlist}' not found.")
        sys.exit(1)

    result = find_password(args.hash, words)
    if result:
        print("Password found:", result)
    else:
        print("Password not found.")
        sys.exit(1)


if __name__ == "__main__":
    main()
