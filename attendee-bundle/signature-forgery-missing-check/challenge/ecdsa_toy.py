#!/usr/bin/env python3
"""
Tiny, transparent secp256k1 ECDSA  --  shared by the server, the starter, and the solver.

Hand-rolled ON PURPOSE. The vulnerability in this module lives in the VERIFIER, so the
verifier has to be code you can read -- a real library would defend against it. Two verify
functions sit side by side and differ by exactly ONE line (the range check). That single
line is the whole lesson.

secp256k1: y^2 = x^3 + 7 over F_p. No dependencies beyond the standard library.
"""
import hashlib

# --- curve parameters (public constants) ---------------------------------- #
P  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
A  = 0
B  = 7
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
N  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
G  = (Gx, Gy)


# --- elliptic-curve group law (affine, point at infinity = None) ----------- #
def inv(x, m):
    return pow(x % m, -1, m)


def point_add(Pt, Qt):
    if Pt is None:
        return Qt
    if Qt is None:
        return Pt
    x1, y1 = Pt
    x2, y2 = Qt
    if x1 == x2 and (y1 + y2) % P == 0:
        return None
    if Pt == Qt:
        m = (3 * x1 * x1 + A) * inv(2 * y1, P) % P
    else:
        m = (y2 - y1) * inv(x2 - x1, P) % P
    x3 = (m * m - x1 - x2) % P
    y3 = (m * (x1 - x3) - y1) % P
    return (x3, y3)


def scalar_mult(k, Pt):
    r, addend = None, Pt
    k %= N
    while k:
        if k & 1:
            r = point_add(r, addend)
        addend = point_add(addend, addend)
        k >>= 1
    return r


# --- ECDSA ----------------------------------------------------------------- #
def hash_msg(msg: bytes) -> int:
    return int.from_bytes(hashlib.sha256(msg).digest(), "big") % N


def sign(d: int, msg: bytes, k: int):
    z = hash_msg(msg)
    R = scalar_mult(k, G)
    r = R[0] % N
    s = inv(k, N) * (z + r * d) % N
    if r == 0 or s == 0:
        raise ValueError("degenerate signature; pick another k")
    return r, s


def pub_from_priv(d: int):
    return scalar_mult(d, G)


def _inv_or_zero(x, m):
    """Modular inverse -- but returns 0 for 0 instead of raising.

    This is the exact flaw behind CVE-2021-43572 (starkbank-ecdsa): the library's
    modular inverse of 0 returned 0 rather than erroring, so s=0 didn't blow up -- it
    quietly produced w=0 and the whole verification collapsed to 0 == 0.
    """
    if x % m == 0:
        return 0
    return pow(x % m, -1, m)


def naive_verify(Q, msg: bytes, r: int, s: int) -> bool:
    """VULNERABLE verifier: NO range check on (r, s). CVE-2021-43572 in miniature.

    With r=0, s=0:  w=inv(0)=0  ->  u1=u2=0  ->  X = 0*G + 0*Q = infinity  ->
    the code compares r == 0, which is True. A valid signature on ANY message under
    ANY public key.
    """
    z = hash_msg(msg)
    w = _inv_or_zero(s, N)
    u1, u2 = z * w % N, r * w % N
    X = point_add(scalar_mult(u1, G), scalar_mult(u2, Q))
    if X is None:                       # point at infinity: x-coord "is" 0
        return r % N == 0
    return X[0] % N == r % N


def strict_verify(Q, msg: bytes, r: int, s: int) -> bool:
    """The FIX = naive_verify + the one line the vulnerable library skipped."""
    if not (1 <= r < N and 1 <= s < N):     # <-- the missing check
        return False
    return naive_verify(Q, msg, r, s)


# `verify` is the correct one, used by the self-test.
verify = strict_verify
