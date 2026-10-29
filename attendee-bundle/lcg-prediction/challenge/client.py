#!/usr/bin/env python3
"""
LCG token-prediction exploit -- STARTER. Fill in the two lines that recover a and c.

Usage:  python client.py                        # 127.0.0.1:5005
        python client.py http://10.0.0.5:5005    # the instructor's server

Deps:   pip install requests
"""
import os
import sys
from functools import reduce
from math import gcd

import requests

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:5005"
SID = "me-" + os.urandom(4).hex()        # your own private stream; keep it unique
N_SAMPLES = 16


def get_token():
    j = requests.get(f"{BASE}/token", params={"sid": SID}).json()
    return int(j["token"])


# 1) collect a run of "random" reset tokens on your own stream
s = [get_token() for _ in range(N_SAMPLES)]
print("[*] first few tokens:", s[:3])

# 2) recover the modulus m (this part is done for you -- it's the least obvious step).
#    Differences d_i = s[i+1]-s[i] obey d_{i+1} = a*d_i (mod m), so
#    z_i = d_{i+2}*d_i - d_{i+1}^2 is always 0 (mod m) -> a multiple of m.
#    gcd a few of them and you get m.
d = [b - a for a, b in zip(s, s[1:])]
z = [d[i + 2] * d[i] - d[i + 1] ** 2 for i in range(len(d) - 2)]
m = abs(reduce(gcd, z))
print("[+] recovered modulus m =", m)

# The generator is  s[i+1] = (a*s[i] + c) mod m.  You know m and the outputs s[].
#
# TODO 1: recover the multiplier a.
#         Two consecutive steps give  s[2]-s[1] = a*(s[1]-s[0]) (mod m).
#         Solve for a. "Division mod m" is a modular inverse: pow(x, -1, m).
# a = ...
#
# TODO 2: recover the increment c.
#         From  s[1] = a*s[0] + c (mod m),  solve for c.
# c = ...
#
# ---- your two lines here ----

# sanity check: your a, c, m must regenerate the sequence you already saw
assert all((a * s[i] + c) % m == s[i + 1] for i in range(len(s) - 1)), \
    "recovered params do not reproduce the sequence -- re-check your two lines"
print(f"[+] recovered a = {a}, c = {c}")

# 3) predict the next output -- the admin reset token the server is about to mint
prediction = (a * s[-1] + c) % m
resp = requests.get(f"{BASE}/flag", params={"sid": SID, "guess": str(prediction)}).json()
print(resp)
