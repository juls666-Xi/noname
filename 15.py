#!/usr/bin/env python3
"""
Secure Password Generator – CLI version.
Generates strong, customizable passwords with ease.
"""

import argparse
import random
import string
import sys

# Character sets
LOWERCASE = string.ascii_lowercase
UPPERCASE = string.ascii_uppercase
DIGITS = string.digits
SYMBOLS = "!@#$%^&*()-_=+[]{}|;:,.<>?/"

# Ambiguous characters to avoid if --no-ambiguous is used
AMBIGUOUS = "0OIl1|"

def generate_password(length=16, use_lower=True, use_upper=True,
                      use_digits=True, use_symbols=True,
                      no_ambiguous=False):
    """Generate a random password from the selected character sets."""
    chars = ""
    if use_lower:
        chars += LOWERCASE
    if use_upper:
        chars += UPPERCASE
    if use_digits:
        chars += DIGITS
    if use_symbols:
        chars += SYMBOLS

    if not chars:
        raise ValueError("At least one character set must be selected.")

    if no_ambiguous:
        # Remove ambiguous characters from the pool
        chars = ''.join(c for c in chars if c not in AMBIGUOUS)

    # Ensure password contains at least one from each selected set (optional)
    # For simplicity, we just random choose; most sets are large enough.
    return ''.join(random.choice(chars) for _ in range(length))

def main():
    parser = argparse.ArgumentParser(
        description="Generate secure passwords.",
        epilog="Example: password_gen.py -l 20 -s -c 3"
    )
    parser.add_argument("-l", "--length", type=int, default=16,
                        help="Password length (default: 16)")
    parser.add_argument("-c", "--count", type=int, default=1,
                        help="Number of passwords to generate (default: 1)")
    parser.add_argument("--no-lower", action="store_true",
                        help="Exclude lowercase letters")
    parser.add_argument("--no-upper", action="store_true",
                        help="Exclude uppercase letters")
    parser.add_argument("--no-digits", action="store_true",
                        help="Exclude digits")
    parser.add_argument("--no-symbols", action="store_true",
                        help="Exclude symbols")
    parser.add_argument("--no-ambiguous", action="store_true",
                        help="Remove ambiguous characters (0, O, I, l, etc.)")
    parser.add_argument("--copy", action="store_true",
                        help="Copy the first generated password to clipboard")
    args = parser.parse_args()

    # Determine which sets to use
    use_lower = not args.no_lower
    use_upper = not args.no_upper
    use_digits = not args.no_digits
    use_symbols = not args.no_symbols

    if not (use_lower or use_upper or use_digits or use_symbols):
        print("Error: You must include at least one character set.", file=sys.stderr)
        sys.exit(1)

    passwords = []
    try:
        for _ in range(args.count):
            pwd = generate_password(
                length=args.length,
                use_lower=use_lower,
                use_upper=use_upper,
                use_digits=use_digits,
                use_symbols=use_symbols,
                no_ambiguous=args.no_ambiguous
            )
            passwords.append(pwd)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Output passwords
    for i, pwd in enumerate(passwords, start=1):
        print(f"{i}: {pwd}" if args.count > 1 else pwd)

    # Copy first password to clipboard if requested
    if args.copy and passwords:
        try:
            import pyperclip
            pyperclip.copy(passwords[0])
            print("\n(First password copied to clipboard)")
        except ImportError:
            print("\n(Clipboard copy requires 'pyperclip'. Install with: pip install pyperclip)")

if __name__ == "__main__":
    main()