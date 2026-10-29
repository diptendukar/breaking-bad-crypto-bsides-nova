# CBC Padding Oracle — attendee brief

The server is holding an encrypted session cookie. Your job: **read it without the key.**

## Setup
```
pip install requests
```
Point your exploit at the instructor's server: `http://<instructor-ip>:5002`.

## The target
- `GET /token` → the cookie, `base64(IV[16] || ciphertext)`. Same value every time.
- It decrypts (server-side) to `user=guest&role=user&note=flag{...}`. You never see that.
- `GET /decrypt?token=...` → the server decrypts your cookie and tells you **one thing only**:
  - `200 {"ok": true}` — the PKCS#7 padding was valid.
  - `400 {"error": "padding"}` — the padding was invalid.

  It never echoes the cookie contents. Just: *did the padding parse?*

## The idea
CBC decryption is `P[i] = decrypt(C[i]) XOR C[i-1]` — the same equation you used to **write** in the
bit-flip lab, run here to **read**. A single valid/invalid padding bit per query is enough to peel a
block apart one byte at a time. Work out how (what two blocks do you send, and what are you forcing
the padding to be?), or let `hints.md` walk you through it byte by byte.

## Your task
Fill in the one TODO in `client.py` — the 256-value byte sweep. The plumbing (fetch the cookie,
split it into blocks, call the oracle, walk the blocks) is written.

```
python client.py http://<instructor-ip>:5002
```
Goal: print the recovered cookie, including `note=flag{...}`.

## Stretch (CBC-R)
The same oracle also lets you **forge**. Build a cookie that decrypts to `role=admin` and
`/decrypt` returns a second flag. Ask the instructor for the stretch handout.

> Watch out: there is exactly one false-positive trap in the last-byte sweep. If your first block
> comes back with one wrong byte, that's it. `hints.md` explains the fix.
