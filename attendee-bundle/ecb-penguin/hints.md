# Hints — ECB penguin (optional hands-on)

## Count-the-repeats
- **Hint 1:** ECB encrypts each 16-byte block independently and deterministically. What does that mean for two identical plaintext blocks?
- **Hint 2:** Slice the ciphertext into 16-byte blocks and count how many are duplicates. Many duplicates → ECB.
- **Hint 3:** The repeated blocks cluster wherever the plaintext had a solid/repeated region.

## Image-reveal
- **Hint 1:** The file won't open because its header is broken, not because the pixels are unrecoverable. What does a valid BMP (or PPM) header look like?
- **Hint 2:** Take a known-good image of the same dimensions, keep its header, and splice the encrypted pixel bytes after it.
- **Hint 3:** In a viewer you don't need to *decrypt* anything — ECB has already leaked the shape of the flag as a pattern of repeated blocks. Read it with your eyes.
- **Hint 4 (BMP specifics):** BMP header is 54 bytes for 24-bit; scanlines are bottom-up and row-padded to 4 bytes. Use the `<input>_sample.bmp` the script wrote (its first 54 bytes) as the donor header.
