import zipfile
import itertools
import sys

def brute_force_zip(zip_path, charset, max_length):
    """Try all combinations from charset up to max_length to open zip file."""
    with zipfile.ZipFile(zip_path, 'r') as zf:
        for length in range(1, max_length + 1):
            for combo in itertools.product(charset, repeat=length):
                password = ''.join(combo)
                try:
                    zf.extractall(pwd=password.encode('utf-8'))
                    return password
                except (RuntimeError, zipfile.BadZipFile, zipfile.LargeZipFile):
                    continue
                except Exception:
                    continue
    return None

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python zip_brute.py <zipfile> <charset> <max_len>")
        print("Example: python zip_brute.py secret.zip abc123 4")
        sys.exit(1)
    zip_path = sys.argv[1]
    charset = sys.argv[2]
    max_len = int(sys.argv[3])
    found = brute_force_zip(zip_path, charset, max_len)
    if found:
        print(f"Password found: {found}")
    else:
        print("Password not found")