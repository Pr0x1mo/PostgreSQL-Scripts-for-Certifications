def compute_hash(txt):
    hv = 0
    pos = 0
    for let in txt:
        pos = (pos % 4) + 1
        hv = (hv + (pos * ord(let))) % 1000000
    return hv

# Automated search for a hash collision
from itertools import product

ascii_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
found = False

for length in range(3, 11):  # lengths from 3 to 10
    for s1 in product(ascii_letters, repeat=length):
        string1 = ''.join(s1)
        hash1 = compute_hash(string1)
        for s2 in product(ascii_letters, repeat=length):
            string2 = ''.join(s2)
            if string1 != string2:
                hash2 = compute_hash(string2)
                if hash1 == hash2:
                    print(f"Collision found! String 1: {string1}, String 2: {string2}, Hash: {hash1}")
                    found = True
                    break
        if found:
            break
    if found:
        break

if not found:
    print("No collision found.")
