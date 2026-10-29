#!/usr/bin/env python3
"""
Tiny, transparent secp256k1 ECDSA  --  shared by the server, the starter, and the solver.

Hand-rolled ON PURPOSE. The whole point of this module is that the attack is *school
algebra*, so the signing code is plain arithmetic you can read, not a library black box.
No dependencies beyond the standard library.

secp256k1 is the Bitcoin / PS3-era curve. y^2 = x^3 + 7 over F_p.
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
    """Message hash mapped into Z_n (both SHA-256 and n are 256-bit here)."""
    return int.from_bytes(hashlib.sha256(msg).digest(), "big") % N


def sign(d: int, msg: bytes, k: int):
    """Return (r, s). NOTE: caller supplies k so we can (mis)use it deliberately."""
    z = hash_msg(msg)
    R = scalar_mult(k, G)
    r = R[0] % N
    s = inv(k, N) * (z + r * d) % N
    if r == 0 or s == 0:
        raise ValueError("degenerate signature; pick another k")
    return r, s


def verify(Q, msg: bytes, r: int, s: int) -> bool:
    if not (1 <= r < N and 1 <= s < N):
        return False
    z = hash_msg(msg)
    w = inv(s, N)
    u1, u2 = z * w % N, r * w % N
    X = point_add(scalar_mult(u1, G), scalar_mult(u2, Q))
    if X is None:
        return False
    return X[0] % N == r


def pub_from_priv(d: int):
    return scalar_mult(d, G)
