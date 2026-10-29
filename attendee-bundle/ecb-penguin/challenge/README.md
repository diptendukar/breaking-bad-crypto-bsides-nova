# Challenge — ECB penguin

This script works on the **raw file bytes** (not decoded pixels), so it teaches three
things with real, openable (or un-openable) output files.

## Setup
```
pip install pycryptodome          # required
pip install pillow                # optional — only for --gray
```

## The three demos
```
# 1) UNCOMPRESSED image, header kept, pixels encrypted -> the penguin LEAKS
python ecb_penguin.py -i tux_clear.bmp
python ecb_penguin.py -i tux_clear.bmp --gray     # cleanest (grayscale, no shear)
python ecb_penguin.py                             # no -i = synthetic BMP, same lesson

# 2) Same file, but --full ENCRYPTS THE HEADER TOO -> nothing renders
python ecb_penguin.py -i tux_clear.bmp --full

# 3) COMPRESSED image (PNG/JPEG) -> NO penguin, even with the header kept
python ecb_penguin.py -i Tux.png
python ecb_penguin.py -i Tux.jpg
```

Flags: `-i/--in <image>` · `-o/--out <dir>` (default `out`) · `--full` · `--gray`.
Outputs are named after the input, in `out/`: e.g. `tux_clear_ecb.bmp`, `tux_clear_cbc.bmp`, `tux_clear_sample.bmp`. For the viewable cases it also writes `tux_clear_ecb.png` / `tux_clear_cbc.png` **previews you can open on any OS** — no PGM/BMP viewer needed. (`--gray` tags its files `tux_clear_grayscale_*`, so it never overwrites the color run.)


## Predict first
- Before demo 1's `out/tux_clear_cbc.png`: will the penguin survive CBC? Why?
- Before demo 2: what happens to a BMP if you scramble its first 54 bytes?
- Before demo 3: your PNG is a picture too — why won't ECB show *its* penguin?

## What each demo shows
1. **Uncompressed + header kept (default):** open `out/tux_clear_ecb.png` (the preview) — the picture still leaks
   through (solid regions visible). Open `out/tux_clear_cbc.png` — noise. *ECB reveals equality:
   identical plaintext blocks → identical ciphertext blocks.* (`--gray` removes the
   diagonal **shear** you see in 24-bit color: 3 bytes/pixel vs 16-byte blocks, `lcm=48`.)
2. **`--full`:** open `out/tux_clear_ecb.bmp` — it **won't open at all**. You encrypted the header,
   so there are no magic bytes/dimensions for a decoder to read. *Headers matter.*
3. **Compressed (PNG/JPEG):** open `out/Tux_ecb.png` — **no penguin, and it won't render**.
   Compression already stripped the block repetition ECB leaks, and the encrypted
   compressed stream no longer decodes. *The trick needs an UNCOMPRESSED format.*



