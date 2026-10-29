#!/usr/bin/env python3
"""
CBC padding-oracle exploit -- STARTER. Fill in the one TODO to read the cookie.

Usage:  python client.py                        # defaults to 127.0.0.1:5002
        python client.py http://10.0.0.5:5002    # the instructor's server

Deps:   pip install requests
"""
import base64
import sys

import requests

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:5002"
BS = 16


def get_cookie():
    """GET /token -> the raw bytes IV || ct."""
    tok = requests.get(f"{BASE}/token").json()["token"]
    return base64.urlsafe_b64decode(tok)


def padding_ok(blob: bytes) -> bool:
    """THE ORACLE. Ask the server: does this cookie's padding parse?
    True  = server said 200 {"ok": true}   (valid padding)
    False = server said 400 {"error":"padding"}."""
    tok = base64.urlsafe_b64encode(blob).decode()
    return requests.get(f"{BASE}/decrypt", params={"token": tok}).json().get("ok", False)


def recover_block(prev: bytes, target: bytes) -> bytes:
    """Recover the 16 plaintext bytes of `target`, whose real previous block is `prev`.

    Key idea (same equation as bit-flipping, run backwards):
        decrypted_padded = D_k(target)                # 16 secret "intermediate" bytes
        plaintext        = D_k(target) XOR prev
    We never touch `target`, so D_k(target) never changes. We submit a 2-block cookie
        forged_prev || target
    and the server decrypts it to  D_k(target) XOR forged_prev  and checks *its* padding.
    By choosing forged_prev so the tail looks like valid PKCS#7 (0x01, then 0x02 0x02, ...)
    we learn D_k(target) one byte at a time, then XOR the REAL prev to get the plaintext.
    """
    inter = bytearray(BS)           # D_k(target), recovered right-to-left
    for pad_val in range(1, BS + 1):
        pos = BS - pad_val          # the byte index we are solving this round
        forged = bytearray(BS)
        # bytes to the right of pos are already known: make them decrypt to `pad_val`
        for k in range(pos + 1, BS):
            forged[k] = inter[k] ^ pad_val

        # TODO ---------------------------------------------------------------
        # Sweep forged[pos] over all 256 values. When the oracle says the padding
        # is valid, you've made byte `pos` of the decryption equal `pad_val`, so:
        #     inter[pos] = forged[pos] XOR pad_val
        # Watch out for ONE false positive when pad_val == 1 (see hints.md).
        #
        #   for guess in range(256):
        #       forged[pos] = guess
        #       if padding_ok(bytes(forged) + target):
        #           inter[pos] = guess ^ pad_val
        #           break
        # --------------------------------------------------------------------
        raise NotImplementedError("fill in the byte sweep for forged[pos]")

    return bytes(inter[i] ^ prev[i] for i in range(BS))


def main():
    blob = get_cookie()
    iv, ct = blob[:BS], blob[BS:]
    blocks = [ct[i:i + BS] for i in range(0, len(ct), BS)]
    prevs = [iv] + blocks[:-1]      # the block feeding each ciphertext block's XOR

    recovered = b"".join(recover_block(prevs[i], blocks[i]) for i in range(len(blocks)))
    print("recovered:", recovered)


if __name__ == "__main__":
    main()
