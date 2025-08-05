import addresses
import multiprocessing
import sys
import os
from concurrent.futures import ProcessPoolExecutor
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'lib')) 
import bitcoin

CPU_HALF = False
MIN_WORKERS = 1

def generate_key_pair():
    try:
        private_key = bitcoin.random_key()
        public_key = bitcoin.privtopub(private_key)
        address = bitcoin.pubtoaddr(public_key)
        # print(f'Generating key: {private_key}-{public_key}-{address}')
        return private_key, public_key, address
    except Exception as e:
        print(f'Error generating key pair: {e}')
        return None, None, None

def check_and_save(key_pair):
    private_key, public_key, address = key_pair
    if address in addresses.TARGET_ADDRESSES:
        save_key(private_key, public_key, address)
    return False

def save_key(private_key, public_key, address):
    try:
        with open('btcganker.txt', 'a') as f:
            f.write(f"{private_key}-{public_key}-{address}\n")
    except Exception as e:
        print(f'Error saving key: {e}')

def worker():
    while True:
        key_pair = generate_key_pair()
        if key_pair[0]:
            if check_and_save(key_pair):
                break

def main():
    print('Starting Bitcoin address generator')
    
    num_cores = multiprocessing.cpu_count()
    if CPU_HALF:
        num_workers = max(int(num_cores / 2), MIN_WORKERS)
        print('Running in low power mode')
    else:
        num_workers = max(num_cores - 1, MIN_WORKERS)
        print('Running in high performance mode')
    
    print(f'Using {num_workers} worker processes')
    print(f'Target addresses: {len(addresses.TARGET_ADDRESSES)}')
    
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(worker) for _ in range(num_workers)]
        for future in futures:
            future.result()

if __name__ == '__main__':
    main()
