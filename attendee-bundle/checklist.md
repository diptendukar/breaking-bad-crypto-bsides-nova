# Breaking Bad Crypto — the six questions

*A one-page code-review checklist. If the answer to any of these is "yes" — or
"I don't know" — you may have a bug. Run it against any codebase, in any
language, without knowing the math underneath.*

Seven labs today. **Six questions.** (One pillar, "you rolled it wrong," earned
two labs — the penguin and the bit-flip — because rolling your own shows up both
as a leak and as something an attacker can steer.)

---

### 1. Did you reuse it?
*Smell: "you reused the one-time thing."*
Nonces, IVs, keys, salts — anything meant to be used **once**. Sony shipped a
constant ECDSA nonce and lost the PS3 master key to two signatures.
**Fix:** fresh CSPRNG output per use; for ECDSA, RFC 6979 deterministic nonces.

### 2. Did you check it?
*Smell: "you didn't check it."*
Ranges, curve points, signature components, inputs. One missing `1 ≤ r,s < n`
range check turned `(r,s)=(0,0)` into a signature valid for **any** message.
**Fix:** validate every input a verifier trusts; write the negative test (`(0,0)` must fail) *before* you ship.

### 3. Did you let the attacker choose?
*Smell: "you let the attacker choose."*
Algorithms, keys, modes, headers. A JWT verifier that obeys the token's own
`alg` header lets the attacker pick `none` and skip the signature.
**Fix:** the *server* allowlists the algorithm; never let a header pick the verification method.

### 4. Did you leak it?
*Smell: "the code leaks it back."*
Error messages, timing, one-bit answers. "Padding bad" vs "MAC bad" is enough to
read an entire message — the padding oracle.
**Fix:** one indistinguishable, constant-time error for all decryption failures. Authenticate *before* you decrypt.

### 5. Did you roll it yourself?
*Smell: "structure leaks" / "you can steer it."*
Homemade modes and constructions. ECB leaks equality (the penguin). CBC with no
integrity lets an attacker flip ciphertext bytes into chosen plaintext (bit-flip).
**Fix:** use a vetted AEAD mode (AES-GCM, ChaCha20-Poly1305). Never ECB past one block; never encrypt without integrity.

### 6. Did you use a real RNG?
*Smell: "you used a toy RNG."*
LCGs, Mersenne Twister, time-seeded `rand()` — all predictable after a few
outputs. If you can predict the next token, so can they.
**Fix:** `secrets` / `getrandom()` / `CryptGenRandom` for anything security-relevant.

---

**The loop, seven times over:**
**Exploit it → name the invariant it broke → add the missing check → prove it with a negative test.**

*Six questions. Zero math broken. The crypto was never the problem — the code around it was.*
