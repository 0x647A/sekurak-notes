# CRC32 Collision Finder for Digit and Letter Passwords

This Python script demonstrates a CRC32 hash collision between two different types of randomly generated passwords:

- Passwords composed exclusively of digits (0-9)
- Passwords composed exclusively of lowercase letters (a-z)

It generates random passwords of varying lengths (4 to 10 characters) for both types, computes their CRC32 checksums using the `zlib` module, and searches for a pair (one digit-only, one letter-only) that produces the same CRC32 value.

## Table of Contents

- [Description](#description)
- [Requirements](#requirements)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Sample Output](#sample-output)
- [Notes](#notes)

## Description

CRC32 is a checksum algorithm producing a 32-bit integer, commonly used for error detection in file transfers and network protocols. Because its output space is limited to 2³² ≈ 4 billion values, collisions are practically achievable: by the birthday paradox, after generating roughly 77,000 unique values there is already a ~50% probability of a collision within a single set (n ≈ 1.177 × √2³² ≈ 77,163). This script searches for a collision *across* two distinct character sets (digits vs. letters), which is slightly harder but still reliably found within one million attempts.

The script maintains two dictionaries of generated passwords keyed by their CRC32 value. Each new password is checked for a cross-set collision at insertion time, so no redundant comparisons are made.

## Requirements

- Python 3.10 or newer
- No external libraries required (uses standard `zlib`, `random`, and `string` modules)

## Usage

```bash
python3 collision_course.py
```

To increase the number of iterations, change the `MAX_ITERATIONS` constant at the top of the script. Note that each iteration generates two passwords (one digit-only, one letter-only), so the total number of evaluated passwords is `2 * MAX_ITERATIONS`.

## How It Works

- A random digit-only password (length 4–10) is generated and its CRC32 is computed.
- If its CRC32 has not been seen before, it is stored and immediately checked against the letter-password dictionary.
- The same process is repeated for a random letter-only password.
- If a CRC32 value appears in both dictionaries, a collision is found and the script exits.
- If no collision is found after `MAX_ITERATIONS` iterations, the user is notified.

## Sample Output

If a collision is found:

```
✅ CRC32 collision found!
Password with digits:  6715065347
Password with letters: hrsgekxb
CRC32: 3076497709
```

If no collision is found within the attempt limit:

```
❌ No collision found – try increasing MAX_ITERATIONS.
```

## Notes

- CRC32 is **not** a cryptographic hash function and must never be used for password hashing or integrity verification in security contexts.
- Collisions are practically achievable due to CRC32's small 32-bit output space — this is a feature of the demo, not a lucky outcome.
- Increasing `MAX_ITERATIONS` improves the probability of finding a collision but also increases runtime. Memory usage is bounded by `MAX_CACHE_SIZE` (default: 500,000 entries per dictionary, ~50 MB each).
- This script is a demonstration of checksum collision properties for educational purposes.
