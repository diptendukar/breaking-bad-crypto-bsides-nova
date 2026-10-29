#!/usr/bin/env python3
"""
Pre-flight check for the crypto-attacks workshop.

Run this BEFORE the workshop (and again at the start if you like):

    python labcheck.py

All [ OK ] = you're ready. Any [FAIL] = see README.md "Setup", or grab a helper
at the start of the session. ASCII-only output so it's safe on every terminal.
"""
import sys


def check(name, fn, required=True):
    try:
        fn()
        print(f"  [ OK ] {name}")
        return True
    except Exception as e:  # noqa: BLE001 - we want to report any failure plainly
        tag = "[FAIL]" if required else "[warn]"
        print(f"  {tag} {name}  ->  {e}")
        return not required


def main():
    print("Crypto-attacks workshop -- environment check")
    print("-" * 48)
    ok = True

    v = sys.version_info
    if v >= (3, 9):
        print(f"  [ OK ] Python {v.major}.{v.minor}.{v.micro}")
    else:
        print(f"  [FAIL] Python {v.major}.{v.minor} -- need 3.9 or newer")
        ok = False

    ok &= check("pycryptodome (import Crypto.Cipher.AES)",
                lambda: __import__("Crypto.Cipher", fromlist=["AES"]))
    ok &= check("requests", lambda: __import__("requests"))
    # Pillow is only needed for the image modules -> warn, don't fail.
    ok &= check("pillow (optional -- image modules)",
                lambda: __import__("PIL"), required=False)

    def aes_roundtrip():
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import pad, unpad
        key = b"YELLOW SUBMARINE"
        ct = AES.new(key, AES.MODE_ECB).encrypt(pad(b"hello workshop", 16))
        assert unpad(AES.new(key, AES.MODE_ECB).decrypt(ct), 16) == b"hello workshop"

    ok &= check("AES encrypt/decrypt actually works", aes_roundtrip)

    print("-" * 48)
    if ok:
        print("All good -- you're ready for the workshop. See you there!")
        sys.exit(0)
    print("Something's missing. Fix per README.md 'Setup', or ask a helper at the start.")
    sys.exit(1)


if __name__ == "__main__":
    main()
