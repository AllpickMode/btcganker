import multiprocessing
from concurrent.futures import ProcessPoolExecutor
# import time
from typing import Set
import hashlib
import addresses
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, "lib"))
import ecdsa
import base58

TARGET_ADDRESSES: Set[str] = set(addresses.TARGET_ADDRESSES)
CPU_HALF = False
MIN_WORKERS = 1
BATCH_SIZE = 1000
TARGET_HASHES = {hashlib.sha256(hashlib.sha256(base58.b58decode(address)).digest()).digest()[:4] 
                for address in TARGET_ADDRESSES}

def generate_key_pair():
    private_key=os.urandom(32)
    # private_key = bytes.fromhex('e7331a4ce57158415cc81fc98140d9fec0293984417bf12f04947b32161f6166')
    sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    public_key = b'\x04' + vk.to_string()
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(hashlib.sha256(public_key).digest())
    address_hash = b'\x00' + ripemd160.digest()
    checksum = hashlib.sha256(hashlib.sha256(address_hash).digest()).digest()[:4]
    address = base58.b58encode(address_hash + checksum).decode('utf-8')
    return private_key.hex(), public_key.hex(), address

def generate_key_pairs_batch():
    return [generate_key_pair() for _ in range(BATCH_SIZE)]

def check_and_save_batch(key_pairs):
    found = False
    with open("checklist.txt", "a") as f:
        for private_key, public_key, address in key_pairs:
            address_hash = hashlib.sha256(hashlib.sha256(base58.b58decode(address)).digest()).digest()[:4]
            if address_hash in TARGET_HASHES:
                f.write(f"{private_key}-{public_key}-{address}\n")
                found = True
    return found

def worker():
    # timestart = time.perf_counter()
    # last_report = time.perf_counter()
    # total_generated = 0
    while True:
        key_pairs = generate_key_pairs_batch()
        # total_generated += len(key_pairs)
        if check_and_save_batch(key_pairs):
            print(f"Found matching address in batch")
            break
        # if time.perf_counter() - last_report > 10:
        #     elapsed = time.perf_counter() - timestart
        #     rate = total_generated / elapsed
        #     print(f"Generated: {total_generated} | Rate: {rate:.0f} keys/sec")
        #     last_report = time.perf_counter()
        #     total_generated = 0
        #     timestart = time.perf_counter()

def main():
    print("Starting optimized Bitcoin address generator")
    num_cores = multiprocessing.cpu_count()
    if CPU_HALF:
        num_workers = max(int(num_cores / 2), MIN_WORKERS)
        print("Running in low power mode")
    else:
        num_workers = max(num_cores - 1, MIN_WORKERS)
        print("Running in high performance mode")
    print(f"Using {num_workers} worker processes")
    print(f"Target addresses: {len(TARGET_ADDRESSES)}")
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(worker) for _ in range(num_workers)]
        for future in futures:
            future.result()

if __name__ == "__main__":
    main()
