# Python Concurrency & Hashing — CTF Practice Scripts

A collection of Python scripts written for CTF (Capture The Flag) challenges, demonstrating hash cracking techniques, CRC collision discovery, system diagnostics, and three different concurrency models.

All scripts use the Python standard library only (Python 3.10+).

## Repository Structure

```
.
├── break_the_hash/          # Hash cracking scripts (MD5, SHA-1, SHA-256, SHA-384)
├── cpu_cores/               # macOS CPU information via sysctl
├── crc_collision/           # CRC32 hash collision demonstration
└── threading_and_multiprocessing/  # Concurrency comparison (threading vs multiprocessing vs event loop)
```

## Modules

### break_the_hash
Password recovery scripts using brute force and wordlist methods.

| Script | Algorithm | Method | Password Format |
|---|---|---|---|
| `break_the_hash_md5.py` | MD5 | Brute force | `AAA9999` (3 uppercase + 4 digits) |
| `break_the_hash_sha1.py` | SHA-1 | Brute force | lowercase a-z, length 1-5 |
| `break_the_hash_sha256.py` | SHA-256 | Brute force | digits 0-9, length 1-8 |
| `break_the_hash_sha384.py` | SHA-384 | Wordlist | single word from file |
| `break_the_hash_md5_mixtype.py` | MD5 | Wordlist + brute force | `word1word2NN` |

All scripts accept the target hash as a CLI argument:
```bash
python3 break_the_hash_sha256.py <hash>
python3 break_the_hash_sha384.py <hash> --wordlist rockyou.txt
```

### cpu_cores
Retrieves CPU model and core counts on macOS using `sysctl`.
```bash
python3 cpu_cores/cpu_physical_and_logical_cores.py
```

### crc_collision
Demonstrates that CRC32 is not collision-resistant by finding two different passwords (one digit-only, one letter-only) that produce the same checksum.
```bash
python3 crc_collision/collision_course.py
```

### threading_and_multiprocessing
Three implementations of the same timed-print task — useful for comparing concurrency approaches:

| Script | Approach | GIL impact |
|---|---|---|
| `threading_test.py` | `threading.Thread` | Yes |
| `multiprocessing_test.py` | `multiprocessing.Process` | No (separate processes) |
| `nothing_test.py` | Single-thread event loop | N/A |

```bash
python3 threading_and_multiprocessing/threading_test.py
python3 threading_and_multiprocessing/multiprocessing_test.py
python3 threading_and_multiprocessing/nothing_test.py
```

## Requirements

- Python 3.10+
- No external dependencies

## Legal Notice

These scripts are for **educational purposes and authorized CTF challenges only**. Cracking hashes without permission is illegal and unethical.
