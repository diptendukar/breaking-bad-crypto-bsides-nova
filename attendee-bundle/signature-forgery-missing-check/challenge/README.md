# The Value of 0 — ECDSA universal forgery — attendee brief

A money-transfer API authorizes every transfer with an ECDSA signature under the sender's key.
To move the **vault's** money you'd need the vault's private key — which you don't have. Move
$1,000,000 to `attacker` anyway. **You will not sign anything. You'll forge with a number the
verifier forgot to reject.**

## Setup
```
pip install requests
```
Point your exploit at the instructor's server: `http://<instructor-ip>:5007`.
`ecdsa_toy.py` sits next to `client.py` — you `import` it (you won't even need it for the forge).

## The service
- `GET /pubkey` → the vault's public key `(Qx, Qy)` on secp256k1.
- `GET /demo_sign?msg=hello` → a *real* signature `(r, s)` (from a throwaway demo key) so you can
  see what a legitimate one looks like — two ~256-bit numbers.
- `GET /transfer?to=..&amount=..&r=..&s=..` → moves money **from the vault**. The signed message is
  `TRANSFER:vault:{to}:{amount}`. Grants the flag once `attacker` holds ≥ $1,000,000.

## The bug
ECDSA verification is supposed to start with a range check: **`1 ≤ r < n` and `1 ≤ s < n`.** This
verifier skips it, so values *outside* that range reach math that was never meant to see them.
Compare a real `(r, s)` from `/demo_sign` with what the verifier actually computes, and ask: what
out-of-range pair makes the whole verification equation collapse to "accept" for *any* message and
*any* key? Work it out, or let `hints.md` walk you to it.

## Your task
Fill in the two lines in `client.py` — the forging `r` and `s`. Then it submits a transfer of
$1,000,000 from the vault to `attacker`.
```
python client.py http://<instructor-ip>:5007
```
Goal: `{"ok": true, ... "flag": "flag{...}"}`.

> This is CVE-2021-43572 in **starkbank-ecdsa 2.0.0** (Python): `Ecdsa.verify()` didn't check that
> `r, s` were in `[1, n-1]`, so an out-of-range pair forged any signature. Same class: gnark / gnark-crypto (Go).
> *You didn't need abstract algebra. You needed a range check.*
