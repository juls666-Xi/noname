import itertools
import sys

def brute_force(target_password, charset, max_length):
    for length in range(1, max_length + 1):
        for guess in itertools.product(charset, repeat=length):
            candidate = ''.join(guess)
            if candidate == target_password:
                return candidate
    return None

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python brute.py <target> <charset> <max_len>")
        sys.exit(1)
    target = sys.argv[1]
    charset = sys.argv[2]
    max_len = int(sys.argv[3])
    result = brute_force(target, charset, max_len)
    if result:
        print(f"Found: {result}")
    else:
        print("Not found")