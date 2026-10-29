# JWT Algorithm Confusion — attendee brief

An auth service issues signed JSON Web Tokens. Mint yourself an **admin** token — without the
server's private key.

## Setup
```
pip install requests pycryptodome
```
Point your exploit at the instructor's server: `http://<instructor-ip>:5004`.
The helper `jwt_toy.py` sits next to `client.py` — you `import` it; you don't edit it.

## The service
- `GET /login` -> a signed JWT with `{"role":"user"}`.
- `GET /admin?token=...` -> the flag **if** your token verifies **and** `role == admin`.
- `GET /pubkey` -> the server's RSA public key (only needed for the optional stretch below).

## A JWT in 20 seconds
Three base64url parts joined by dots: `header.payload.signature`.
```
header    = {"alg":"RS256","typ":"JWT"}       # which algorithm signed this
payload   = {"user":"guest","role":"user"}    # the claims
signature = sign(header.payload)              # over the first two parts
```
The signature is what stops you editing `role` to `admin`. So the trick is to make the server
**not check it.**

## The bug
The server's verifier reads the **`alg` header from the token itself** and trusts it. Set `alg`
to the string **`none`** -- the "I don't need a signature" algorithm -- and a naive verifier accepts
the token with **no signature at all.**

## Your task
Fill in the one TODO in `client.py` -- assemble an `alg=none` token from the two segments it already
built for you. (What does a JWT with *no* signature look like? `hints.md` if you're stuck.) The
plumbing -- build the segments, submit -- is written.
```
python client.py http://<instructor-ip>:5004
```
Goal: `{"ok": true, ... "flag": "flag{...}"}`.

## Stretch -- RS256 -> HS256 key confusion
Harder, and it beats a server that blocks `none`. The verifier also accepts `HS256` (HMAC) and uses
the RSA **public** key as the HMAC secret -- and that key is public, served on `/pubkey`. So you HMAC
your own `alg=HS256` / `role=admin` token with the public-key PEM. See `client_hs256_stretch.py`, or
ask the instructor.

> Root cause either way: **the token told the server how to verify the token.** The fix is an
> algorithm allowlist -- `verify(token, algorithms=["RS256"])` -- checked before anything else.
