#!/usr/bin/env python3
"""
CBC bit-flip exploit -- STARTER. Fill in the one TODO to become root.

Usage:  python client.py                       # defaults to 127.0.0.1:5001
        python client.py http://10.0.0.5:5001   # the instructor's server

Deps:   pip install requests
"""
import base64
import sys

import requests

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:5001"

# 1) get a token (you are role=user)
tok = requests.get(f"{BASE}/token").json()["token"]
blob = bytearray(base64.urlsafe_b64decode(tok))
iv, ct = blob[:16], blob[16:]

# The plaintext of block 0 is:  role=user&uid=42
# index:                        0123456789...
#                                    ^^^^  'user' is at indices 5,6,7,8
#
# In CBC:  P0 = decrypt(C0) XOR IV
# So if you flip IV[j], plaintext byte P0[j] flips by the SAME amount:
#     P0'[j] = P0[j] XOR (IV'[j] XOR IV[j])
# To change byte P0[j] from `old` to `new`, set:  IV[j] ^= (old ^ new)
#
# TODO: turn "user" (indices 5..8) into "root" by editing `iv` in place.
#       Hint: for j, (old, new) in zip(range(5,9), zip(b"user", b"root")): ...

# ---- your code here ----

# 2) submit the modified token
new_token = base64.urlsafe_b64encode(bytes(iv) + bytes(ct)).decode()
resp = requests.get(f"{BASE}/flag", params={"token": new_token}).json()
print(resp)
