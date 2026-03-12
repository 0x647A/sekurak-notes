import os
import requests
import hashlib
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading


SERVER = "SECRET_API"
CHUNK_SIZE = 32  # API requirement
INITIAL_BLOCK_SIZE = 8192  # Start with 8KB blocks for optimization
TIME_LIMIT = 100
THREADS = 4

# Global PoW management
pow_lock = threading.Lock()
current_pow = None
pow_timestamp = 0
hash_cache = {}
hash_cache_lock = threading.Lock()

def solve_pow():
    """Solve Proof of Work challenge"""
    print("[*] Getting PoW challenge...")
    res = requests.get(f"{SERVER}/ex4/get-pow")
    res.raise_for_status()
    data = res.json()
    challenge = bytes.fromhex(data["challenge"])

    print("[*] Solving PoW...")
    i = 0
    while True:
        suffix = i.to_bytes(8, "little")
        token = challenge + suffix
        if hashlib.sha256(token).hexdigest().startswith("ffffff"):
            print(f"[+] PoW solved after {i} attempts")
            return token.hex()
        i += 1

def get_valid_pow():
    """Get valid PoW token, renewing if necessary.

    Lock is held during solve_pow() intentionally — prevents multiple threads
    from solving PoW simultaneously when the token expires.
    """
    global current_pow, pow_timestamp

    with pow_lock:
        current_time = time.time()
        if current_pow is None or (current_time - pow_timestamp) > TIME_LIMIT:
            print("[*] Getting new PoW token...")
            current_pow = solve_pow()
            pow_timestamp = current_time
        return current_pow

def get_correct_hash(offset, size, pow_token):
    """Get hash of correct file fragment from server with caching"""
    cache_key = (offset, size)

    with hash_cache_lock:
        if cache_key in hash_cache:
            return hash_cache[cache_key]

    url = f"{SERVER}/ex4/get-hash?offset={offset}&size={size}&pow={pow_token}"
    try:
        res = requests.get(url, timeout=60)
        res.raise_for_status()
        server_hash = res.text.strip()
        with hash_cache_lock:
            hash_cache[cache_key] = server_hash
        return server_hash
    except Exception as e:
        print(f"[!] Failed to get hash at offset {offset}: {e}")
        return None

def get_correct_chunk(offset, pow_token):
    """Get 32 bytes of correct data from server"""
    url = f"{SERVER}/ex4/get-data?offset={offset}&pow={pow_token}"
    try:
        res = requests.get(url, timeout=60)
        res.raise_for_status()
        data = res.json()
        return bytes.fromhex(data["data"])
    except Exception as e:
        print(f"[!] Failed to get data at offset {offset}: {e}")
        return None

def hierarchical_binary_search(original, fixed, start, end, depth=0):
    """Optimized hierarchical binary search for corruption detection"""
    indent = "  " * depth
    size = end - start

    # Base case: if size is small enough, get the data directly
    if size <= CHUNK_SIZE:
        print(f"{indent}[*] Fixing chunk at offset {start}")
        pow_token = get_valid_pow()
        correct_data = get_correct_chunk(start, pow_token)
        if correct_data:
            actual_size = min(len(correct_data), len(fixed) - start)
            fixed[start:start + actual_size] = correct_data[:actual_size]
            print(f"{indent}[+] Fixed {actual_size} bytes at offset {start}")
        return

    # Ensure size is divisible by 32
    size = (size // 32) * 32
    if size == 0:
        return

    # Get hash for this block
    pow_token = get_valid_pow()
    server_hash = get_correct_hash(start, size, pow_token)

    if server_hash is None:
        print(f"{indent}[!] Could not get hash for offset {start}, size {size}")
        return

    # Calculate local hash
    local_hash = hashlib.sha256(original[start:start + size]).hexdigest()

    if local_hash == server_hash:
        print(f"{indent}[+] Block {start}-{start + size} is correct")
        return

    print(f"{indent}[!] Block {start}-{start + size} is corrupted, dividing...")

    # Divide the block in half
    mid = start + size // 2
    mid = (mid // 32) * 32  # Ensure mid is divisible by 32

    # Recursively check both halves
    hierarchical_binary_search(original, fixed, start, mid, depth + 1)
    hierarchical_binary_search(original, fixed, mid, start + size, depth + 1)

def find_corrupted_regions(original):
    """First pass: identify large corrupted regions"""
    size = len(original)
    corrupted_regions = []

    print(f"[*] Phase 1: Scanning for corrupted regions with {INITIAL_BLOCK_SIZE} byte blocks...")

    for offset in range(0, size, INITIAL_BLOCK_SIZE):
        actual_size = min(INITIAL_BLOCK_SIZE, size - offset)
        actual_size = (actual_size // 32) * 32

        if actual_size == 0:
            continue

        pow_token = get_valid_pow()
        server_hash = get_correct_hash(offset, actual_size, pow_token)

        if server_hash:
            local_hash = hashlib.sha256(original[offset:offset + actual_size]).hexdigest()
            if local_hash != server_hash:
                corrupted_regions.append((offset, offset + actual_size))
                print(f"[!] Corrupted region found: {offset}-{offset + actual_size}")

        # Progress indicator
        progress = min((offset + INITIAL_BLOCK_SIZE) * 100 // size, 100)
        print(f"[*] Scanning progress: {progress}%")

    print(f"[+] Phase 1 complete. Found {len(corrupted_regions)} corrupted regions")
    return corrupted_regions

def fix_corrupted_regions(original, fixed, corrupted_regions):
    """Second pass: fix corrupted regions using binary search"""
    print(f"[*] Phase 2: Fixing {len(corrupted_regions)} corrupted regions...")

    def fix_region(region_info):
        region_idx, (start, end) = region_info
        print(f"[*] Fixing region {region_idx + 1}/{len(corrupted_regions)}: {start}-{end}")
        hierarchical_binary_search(original, fixed, start, end)
        print(f"[+] Region {region_idx + 1} fixed")

    # Use threading to fix regions in parallel
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = [executor.submit(fix_region, (i, region))
                  for i, region in enumerate(corrupted_regions)]

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"[!] Error fixing region: {e}")

def fix_file(filename):
    """Main function to fix the corrupted file"""
    print(f"[*] Opening file: {filename}")
    with open(filename, "rb") as f:
        original = bytearray(f.read())

    fixed = bytearray(original)
    size = len(original)

    print(f"[*] File size: {size} bytes ({size / 1024:.1f} KB)")
    print(f"[*] Estimated blocks to check: {(size + INITIAL_BLOCK_SIZE - 1) // INITIAL_BLOCK_SIZE}")

    start_time = time.time()

    # Phase 1: Find corrupted regions
    corrupted_regions = find_corrupted_regions(original)

    if not corrupted_regions:
        print("[+] No corruption detected! File appears to be intact.")
        return

    # Phase 2: Fix corrupted regions
    fix_corrupted_regions(original, fixed, corrupted_regions)

    # Save the fixed file next to the original, regardless of input path
    output_name = "fixed_" + os.path.basename(filename)
    output_path = os.path.join(os.path.dirname(filename) or ".", output_name)
    with open(output_path, "wb") as f:
        f.write(fixed)

    elapsed_time = time.time() - start_time
    print(f"[+] File fixed and saved as {output_path}")
    print(f"[+] Total time: {elapsed_time:.1f} seconds ({elapsed_time / 60:.1f} minutes)")
    print(f"[+] Hash cache entries: {len(hash_cache)}")

if __name__ == "__main__":
    fix_file("input_file.bin")
