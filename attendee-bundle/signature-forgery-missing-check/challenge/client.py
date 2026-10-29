#!/usr/bin/env python3
"""
Signature-forgery exploit -- STARTER. Forge a signature the vault never authorized.

Usage:  python client.py                        # 127.0.0.1:5007
        python client.py http://10.0.0.5:5007    # the instructor's server

Deps:   pip install requests   (crypto is ecdsa_toy.py, stdlib only)
"""
import sys

import requests

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:5007"

# 1) look at what a REAL signature looks like (signed with a throwaway demo key)
demo = requests.get(f"{BASE}/demo_sign", params={"msg": "hello"}).json()
print("[*] a legitimate signature:")
print("    r =", demo["r"])
print("    s =", demo["s"])
print("    (both are ~256-bit numbers, safely in [1, n-1])")

# 2) You do NOT have the vault's private key, so you can't sign honestly.
#    But the server's verifier never checks that r and s are in range [1, n-1].
#    ECDSA verify computes  w = s^-1,  u1 = z*w,  u2 = r*w,  X = u1*G + u2*Q,
#    then accepts if  X.x == r.  Find an (r, s) that makes that check pass for ANY
#    message and ANY public key -- WITHOUT knowing the private key.
#
#    TODO: set r and s to the forging values.
#    Hint: what value of s makes w collapse, and what value of r then matches X.x?
# r = ...
# s = ...

to, amount = "attacker", 1_000_000
resp = requests.get(f"{BASE}/transfer",
                    params={"to": to, "amount": amount, "r": r, "s": s}).json()
print(f"\n[*] submitting forged transfer: vault -> {to}, ${amount:,}  with (r={r}, s={s})")
print(resp)
