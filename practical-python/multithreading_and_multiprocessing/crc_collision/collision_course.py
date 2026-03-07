import random
import string
import zlib


# Each iteration generates 2 passwords (one digit-only, one letter-only),
# so up to 2 * MAX_ITERATIONS passwords are evaluated in total.
MAX_ITERATIONS = 1_000_000

# Password length range: short enough for a fast search,
# long enough to provide sufficient CRC variety across the 2^32 output space.
MIN_PASSWORD_LENGTH = 4
MAX_PASSWORD_LENGTH = 10

# Caps each lookup dictionary at this many entries.
# At ~100 bytes per entry, each dict uses at most ~50 MB.
MAX_CACHE_SIZE = 500_000


def find_collision(iterations: int) -> tuple[str, str, int] | None:
    """
    Attempt to find a CRC32 collision between a digit-only and a letter-only password.

    Returns (digit_password, letter_password, crc32_value) on success, None otherwise.
    """
    digits_by_crc: dict[int, str] = {}   # crc32 value → digit-only password
    letters_by_crc: dict[int, str] = {}  # crc32 value → letter-only password

    for _ in range(iterations):
        digit_pass = "".join(random.choices(string.digits, k=random.randint(MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH)))
        digit_crc = zlib.crc32(digit_pass.encode())
        if digit_crc not in digits_by_crc and len(digits_by_crc) < MAX_CACHE_SIZE:
            digits_by_crc[digit_crc] = digit_pass
            if digit_crc in letters_by_crc:
                return digit_pass, letters_by_crc[digit_crc], digit_crc

        letter_pass = "".join(random.choices(string.ascii_lowercase, k=random.randint(MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH)))
        letter_crc = zlib.crc32(letter_pass.encode())
        if letter_crc not in letters_by_crc and len(letters_by_crc) < MAX_CACHE_SIZE:
            letters_by_crc[letter_crc] = letter_pass
            if letter_crc in digits_by_crc:
                return digits_by_crc[letter_crc], letter_pass, letter_crc

    return None


def main() -> None:
    result = find_collision(MAX_ITERATIONS)
    if result:
        digit_pass, letter_pass, crc_value = result
        print("✅ CRC32 collision found!")
        print(f"Password with digits:  {digit_pass}")
        print(f"Password with letters: {letter_pass}")
        print(f"CRC32: {crc_value}")
    else:
        print("❌ No collision found – try increasing MAX_ITERATIONS.")


if __name__ == "__main__":
    main()
