# Hints — JWT algorithm confusion

- **Hint 1 (unlock ~5 min):** You are not breaking RSA. You're changing *which algorithm the server
  uses to check the token*, by editing the `alg` field in the header. The server trusts whatever
  `alg` says.

- **Hint 2 (the idea):** What should a signature check do when `alg` is the string `none`? A careful
  server rejects it. A naive one decides "unsigned token, nothing to check" and **skips the signature
  entirely.** So hand it `alg:none` and no signature.

- **Hint 3 (build the token):** `client.py` already builds the two segments for you -- header
  `{"alg":"none","typ":"JWT"}` and payload `{"user":"guest","role":"admin"}`. Assemble them with an
  **empty** third part:
  ```python
  token = f"{header_seg}.{payload_seg}."    # note the trailing dot = empty signature
  ```

- **Hint 4 (if the flag doesn't come):** Check your payload has `role` set to `admin` (the server
  checks `role`), and don't drop the trailing dot -- the token still has three dot-separated parts
  even though the third is empty.

- **Hint 5 (stretch: RS256 -> HS256 confusion):** Harder, and it beats a server that blocks `none`.
  The verifier also accepts `HS256` and reuses the RSA **public** key (on `/pubkey`, not secret) as
  the HMAC secret. So you HMAC your own token:
  ```python
  sig = hmac.new(pub_pem, signing_input, hashlib.sha256).digest()   # pub_pem = exact /pubkey bytes
  ```
  Full version in `client_hs256_stretch.py`.
