# ECDSA Nonce Reuse — attendee brief

A firmware-signing service uses secp256k1 ECDSA. Recover its private key and forge a signature —
**with school algebra, no lattices, no key search.**

## Setup
```
pip install requests
```
Point your exploit at the instructor's server: `http://<instructor-ip>:5003`.
The crypto helper `ecdsa_toy.py` sits next to `client.py` — you `import` it; you don't edit it.

## The service
- `GET /pubkey` → the server's public key `(Qx, Qy)` on secp256k1.
- `GET /sign?msg=hello` → a signature `(r, s)` on your message, plus the message hash `z`.
- `GET /flag?msg=...&r=...&s=...` → the flag, **if** `msg` is the magic phrase
  `i am an authorized firmware update` and `(r, s)` verifies under the server's key.

The catch: `/sign` refuses to sign the magic phrase. So you can't just ask for it — you have to
*forge* a valid signature on it, which means you need the private key.

## The bug
ECDSA signs with a per-signature random nonce `k`: `r = (k·G).x`, `s = k⁻¹(z + r·d) mod n`. **The
security of your key depends on `k` being unique and unpredictable every time.** This server reuses
the *same* `k` on every signature. Ask for two signatures and look at their `r` values.

## Work it out
Two signatures with the same `k` share the same `r` — and from the signing equation
`s = k⁻¹(z + r·d)`, a couple of lines of modular algebra fall out that recover `k`, then the private
key `d`. Derive them yourself (division mod n is a modular inverse: `ecdsa_toy.inv(x, ecdsa_toy.N)`),
or see `hints.md` if you get stuck.

## Your task
Fill in the two TODO lines in `client.py` — recover `k`, then `d`. The plumbing (fetch signatures,
check your key against the public key, forge the magic-phrase signature, submit) is written.

```
python client.py http://<instructor-ip>:5003
```
Goal: print the recovered private key, then `{"ok": true, ... "flag": "flag{...}"}`.

> This is exactly how the PlayStation 3 was jailbroken (2010): Sony signed code with a constant
> nonce, and fail0verflow recovered the master signing key.
