#!/usr/bin/env python3
"""
ECDSA nonce-reuse exploit -- STARTER. Fill in the two algebra lines to recover the key.

Usage:  python client.py                        # 127.0.0.1:5003
        python client.py http://10.0.0.5:5003    # the instructor's server

Deps:   pip install requests   (crypto is ecdsa_toy.py, stdlib only)
"""
import os
import sys

import requests
import ecdsa_toy as ec          # same folder; provides N, inv, sign, pub_from_priv

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:5003"
MAGIC = "i am an authorized firmware update"


def get_sig(msg):
    j = requests.get(f"{BASE}/sign", params={"msg": msg}).json()
    return int(j["r"], 16), int(j["s"], 16), int(j["z"], 16)


# public key (so you can check your recovered d)
pk = requests.get(f"{BASE}/pubkey").json()
Q = (int(pk["Qx"], 16), int(pk["Qy"], 16))

# 1) two signatures on two DIFFERENT messages
r1, s1, z1 = get_sig("unlock my homebrew loader")
r2, s2, z2 = get_sig("please boot my linux")
assert r1 == r2, "r differs -> nonces are unique -> server is patched, attack does not apply"
r = r1

# The signing equation is:  s = k^-1 (z + r*d) mod n   (n is ec.N)
# Both signatures reused the SAME nonce k, so:
#     s1 = k^-1 (z1 + r*d)
#     s2 = k^-1 (z2 + r*d)
#
# TODO 1: subtract the two equations to eliminate d, and solve for k.
#         Hint: s1 - s2 = k^-1 (z1 - z2).  Use ec.inv(x, ec.N) for modular inverse.
# k = ...
#
# TODO 2: plug k back into one equation and solve for the private key d.
#         Hint: s1*k = z1 + r*d.
# d = ...
#
# ---- your two lines here ----

assert ec.pub_from_priv(d) == Q, "recovered d does not match the public key -- check your algebra"
print("[+] recovered private key d =", hex(d))

# 2) you are the signer now: forge a signature on the phrase the server won't sign
kf = int.from_bytes(os.urandom(32), "big") % ec.N
rf, sf = ec.sign(d, MAGIC.encode(), kf)
resp = requests.get(f"{BASE}/flag", params={"msg": MAGIC, "r": hex(rf), "s": hex(sf)}).json()
print(resp)
