# Corrupted File Fixer Using Hierarchical Hash Checking with PoW-Protected API

This Python script is designed to repair a corrupted binary file by comparing local file blocks against corresponding SHA-256 hashes served by a remote API. It uses a hierarchical binary search approach to efficiently identify and fix corrupted regions by fetching correct data chunks from the API.

## Table of Contents

- [Description](#description)  
- [Requirements](#requirements)  
- [Setup](#setup)  
- [Usage](#usage)  
- [How It Works](#how-it-works)  
- [API and Proof-of-Work Requirement](#api-and-proof-of-work-requirement)  
- [Script Functions Overview](#script-functions-overview)  
- [Sample Output](#sample-output)  
- [Notes](#notes)  

## Description

The script repairs a corrupted binary file (e.g., `input_file.bin`) by:

- Comparing blocks of the local file against SHA-256 hashes retrieved from a remote server API.
- Using a dynamic hierarchical binary search method to pinpoint corrupted blocks precisely and fix them in an optimized way.
- Downloading correct 32-byte chunks of the original data from the API to overwrite corrupted parts.
- Running multiple fix tasks in parallel using threading for better performance.
- Handling server-side Proof-of-Work (PoW) challenges to gain authorized access to the API.

## Requirements

- Python 3.6 or newer
- Required Python libraries:
  - `requests`
  - `concurrent.futures` (standard library)
  - `hashlib` (standard library)
  - `os` (standard library)
  - `threading` (standard library)
  - `time` (standard library)

Install `requests` if not available:

```bash
pip install requests
```

## Setup

1. Make sure you have the target corrupted file, e.g., `input_file.bin` in the script folder.
2. Adjust constants as necessary, like the server URL (`SERVER`), number of threads (`THREADS`), or block sizes.

## Usage

Run the script directly from the command line:

```bash
python3 the_annoying_api.py
```

The script will output logs showing progress, detected corrupted regions, and final fixed file saved as `fixed_input_file.bin`.

## How It Works

### Proof-of-Work (PoW)

- The API requires solving a PoW challenge to grant access tokens for each request.
- The script automatically solves the PoW, caching tokens for 100 seconds before re-solving.
- PoW requires finding a nonce such that SHA-256(challenge + nonce) starts with "ffffff".

### Hierarchical Binary Search

- The script starts by scanning the file in large blocks (default 8KB), checking local hash vs server hash.
- If hashes mismatch, the block is divided recursively to locate corrupted sub-blocks.
- When blocks reach 32 bytes (API chunk size), the script replaces corrupted data by fetching correct chunks from the server.

### Multithreaded Fixing

- Corrupted regions are fixed in parallel using a thread pool with configurable thread count.

## API and Proof-of-Work Requirement

- Accessing the API endpoints requires submitting a valid PoW token.
- The script periodically fetches the PoW challenge from the server's `/ex4/get-pow` endpoint.
- Only requests with valid PoW tokens at `/ex4/get-hash` and `/ex4/get-data` endpoints return the correct hash or data.
- This design protects the API from abuse and enforces computational effort to access data.

## Script Functions Overview

- `solve_pow()` — Solves the PoW challenge by brute-forcing a nonce.
- `get_valid_pow()` — Manages PoW token validity and renewal.
- `get_correct_hash(offset, size, pow_token)` — Retrieves a SHA-256 hash of a file fragment from the server.
- `get_correct_chunk(offset, pow_token)` — Gets a correct 32-byte chunk of data from the server.
- `hierarchical_binary_search(original, fixed, start, end)` — Recursively detects and fixes corrupted data blocks.
- `find_corrupted_regions(original)` — Scans file with large blocks to find corrupted regions.
- `fix_corrupted_regions(original, fixed, corrupted_regions)` — Fixes corrupted regions in parallel.
- `fix_file(filename)` — Main function to orchestrate repair.

## Sample Output

```bash
[*] Opening file: input_file.bin
[*] File size: 123456 bytes (120.6 KB)
[*] Estimated blocks to check: 16
[*] Phase 1: Scanning for corrupted regions with 8192 byte blocks...
[*] Getting new PoW token...
[*] Getting PoW challenge...
[*] Solving PoW...
[+] PoW solved after 123456 attempts
[!] Corrupted region found: 0-8192
[*] Scanning progress: 6%
...
[+] Phase 1 complete. Found 3 corrupted regions
[*] Phase 2: Fixing 3 corrupted regions...
[*] Fixing region 1/3: 0-8192
[*] Fixing chunk at offset 0
[+] Fixed 32 bytes at offset 0
...
[+] Region 1 fixed
...
[+] File fixed and saved as ./fixed_input_file.bin
[+] Total time: 350.7 seconds (5.8 minutes)
[+] Hash cache entries: 1234
```

## Notes

- This script was developed for a CTF (Capture The Flag) challenge and depended on access to a **special API** that verifies and provides correct file data using Proof-of-Work.
- Proof-of-Work tokens expire after approximately 100 seconds, so the script manages token renewal.
- Block sizes and threading parameters can be adjusted for different file sizes and performance.
- The hierarchical search drastically reduces the number of server requests compared to naive byte-wise checking.
- Network reliability and API responsiveness affect runtime.
- Ensure network access to the API endpoint configured in `SERVER` constant.
