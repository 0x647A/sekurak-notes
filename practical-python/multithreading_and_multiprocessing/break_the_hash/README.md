# Password Cracking Scripts Using Hash Matching in Python

This directory contains Python scripts demonstrating how to recover passwords by comparing candidate hashes against a known target hash. Each script targets a specific hash algorithm and password format.

## Table of Contents

- [Overview](#overview)
- [Scripts Description](#scripts-description)
- [Requirements](#requirements)
- [Usage](#usage)
- [Notes & Recommendations](#notes--recommendations)

## Overview

All scripts accept a target hash as a command-line argument, generate candidate passwords, hash each one with the appropriate algorithm, and compare the result against the target. When a match is found, the original password is printed.

The scripts cover:

1. **Brute force lowercase passwords (length 1-5) with SHA-1**
2. **Brute force passwords in AAA9999 format (3 uppercase letters + 4 digits) with MD5**
3. **Wordlist-based combination: (word1 + word2 + two-digit suffix) passwords with MD5**
4. **Wordlist-based hash matching with SHA-384**
5. **Brute force numeric passwords (length 1-8) with SHA-256**

## Scripts Description

### 1. Brute Force Lowercase Passwords (SHA-1)

- **Target hash**: SHA-1
- **Password charset**: lowercase letters `[a-z]`
- **Password length**: 1 to 5 characters
- **Method**: Attempts all combinations using `itertools.product`.

### 2. Brute Force AAA9999 Format (MD5)

- **Target hash**: MD5
- **Password format**: 3 uppercase letters (`[A-Z]`) followed by 4 digits (`[0-9]`)
- **Method**: Iterates over all letter and digit combinations, hashes each candidate, and compares against the target.

### 3. Wordlist Combinations With Digit Suffix (MD5)

- **Target hash**: MD5
- **Password format**: two words from a wordlist concatenated with a two-digit suffix (`00`–`99`)
- **Method**: Reads a wordlist file, tries all word pairs plus suffixes, hashes each candidate, and compares.
- **Complexity warning**: The search space grows as O(n² × 100), where n is the number of words in the wordlist. Use a small, targeted wordlist (hundreds of words). Large wordlists such as `rockyou.txt` (~14 million words) will produce a search space too large to complete in any reasonable time.

### 4. Wordlist Hash Matching (SHA-384)

- **Target hash**: SHA-384
- **Password format**: single word from a wordlist file
- **Method**: Hashes each word from the list and compares against the target.

### 5. Brute Force Numeric Passwords (SHA-256)

- **Target hash**: SHA-256
- **Password charset**: digits (`0-9`)
- **Password length**: 1 to 8 digits
- **Method**: Tries all numeric combinations using `itertools.product`.

## Requirements

- Python 3.10 or newer
- No external libraries needed; all scripts use standard Python modules (`hashlib`, `itertools`, `string`, `argparse`).
- Scripts 3 and 4 require a wordlist file (one password candidate per line).

## Usage

All scripts accept the target hash as a positional argument:

```bash
python3 break_the_hash_sha256.py <hash>
python3 break_the_hash_md5.py <hash>
python3 break_the_hash_sha1.py <hash>
```

Scripts that require a wordlist accept an optional `--wordlist` flag (defaults to `wordlist.txt`):

```bash
python3 break_the_hash_sha384.py <hash>
python3 break_the_hash_sha384.py <hash> --wordlist /path/to/rockyou.txt

python3 break_the_hash_md5_mixtype.py <hash>
python3 break_the_hash_md5_mixtype.py <hash> --wordlist /path/to/rockyou.txt
```

**Output:**

If a password is found:
```
Password found: <password>
```

If the search space is exhausted without a match:
```
Password not found.
```
Exit code `1` is returned when no password is found, making the scripts composable in shell pipelines.

## Notes & Recommendations

- **Runtime:** Brute-force over large search spaces can be slow. Adjust `MAX_LENGTH` or the character set to match the expected password complexity.
- **Wordlist quality:** The success of wordlist-based scripts depends entirely on whether the target password appears in the wordlist.
- **Hash algorithm:** Ensure the script's algorithm matches the algorithm used to produce the target hash.
- **Shell history:** The target hash is passed as a CLI argument and will be recorded in shell history (`.bash_history`, `.zsh_history`). If the hash is sensitive, consider passing it via a file or environment variable instead.
- **Security note:** This code is for educational purposes and authorized CTF challenges only. Cracking hashes without permission is illegal and unethical.
- **Optimization:** For large-scale cracking, consider GPU-accelerated tools such as Hashcat or John the Ripper.
