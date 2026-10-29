#!/usr/bin/env python3
"""
ECB penguin  --  Pillar 5, "You rolled it wrong" (deterministic-mode leakage).

Works on the raw FILE BYTES (not decoded pixels), so it teaches three things
honestly:

  1. Uncompressed image (BMP/PPM/PGM), header kept, body ECB-encrypted
     -> the picture STILL LEAKS through (the classic penguin).
  2. The same with --full (encrypt the header too)
     -> the file no longer has a valid header, so NOTHING renders. Headers matter.
  3. A COMPRESSED image (PNG/JPEG), header kept, body encrypted
     -> NO penguin: compression already removed the block repetition ECB leaks,
        and the encrypted compressed stream won't decode. (This is why the trick
        needs an uncompressed format -- your PNG demonstrates the compressed case;
        no JPG required.)

Deps:      pip install pycryptodome
Optional:  pip install pillow      (only for --gray, which converts to grayscale)

Usage:
  python ecb_penguin.py                          # synthetic uncompressed BMP -> penguin
  python ecb_penguin.py -i tux_clear.bmp         # penguin (uncompressed BMP)
  python ecb_penguin.py -i tux_clear.bmp --gray  # cleanest penguin (grayscale, no shear)
  python ecb_penguin.py -i tux_clear.bmp --full  # encrypt header too -> won't open
  python ecb_penguin.py -i Tux.png               # compressed -> no penguin (the lesson)
  python ecb_penguin.py -i tux_clear.bmp -o mydir

Outputs (into --out, default ./out) are named after the input file:
  <name>_sample.<ext>, <name>_ecb.<ext>, <name>_cbc.<ext>
Plus, for the viewable cases, <name>_ecb.png / <name>_cbc.png previews you can
open on any OS (so you never need a PGM/BMP viewer).
"""
import argparse
import os
import struct
import sys

from Crypto.Cipher import AES

W, H = 384, 256                 # synthetic image size
KEY = b"YELLOW SUBMARINE"       # classic 16-byte AES demo key -- NOT a secret


# --------------------------------------------------------------------------- #
# size-preserving ECB / CBC  (encrypt the whole 16-byte-aligned prefix, keep the
# short tail as-is so the output file stays exactly the same length)
# --------------------------------------------------------------------------- #
def ecb_stream(buf: bytes) -> bytes:
    n = len(buf) - (len(buf) % 16)
    return AES.new(KEY, AES.MODE_ECB).encrypt(buf[:n]) + buf[n:]


def cbc_stream(buf: bytes) -> bytes:
    n = len(buf) - (len(buf) % 16)
    return AES.new(KEY, AES.MODE_CBC, iv=b"\x00" * 16).encrypt(buf[:n]) + buf[n:]


def count_repeats(buf: bytes) -> int:
    n = len(buf) - (len(buf) % 16)
    blocks = [buf[i:i + 16] for i in range(0, n, 16)]
    return len(blocks) - len(set(blocks))


# --------------------------------------------------------------------------- #
# format sniffing -> (name, uncompressed?, header_len)
# --------------------------------------------------------------------------- #
def _netpbm_header_len(data: bytes) -> int:
    """Length of a binary PPM/PGM (P6/P5) header: magic + 3 tokens + 1 whitespace."""
    i, tokens = 2, 0
    while tokens < 3 and i < len(data):
        while i < len(data) and data[i:i + 1].isspace():
            i += 1
        if i < len(data) and data[i:i + 1] == b"#":          # comment line
            while i < len(data) and data[i:i + 1] != b"\n":
                i += 1
            continue
        while i < len(data) and not data[i:i + 1].isspace():
            i += 1
        tokens += 1
    return i + 1


def sniff(data: bytes):
    if data[:2] == b"BM":
        (offbits,) = struct.unpack_from("<I", data, 10)
        return "BMP", True, offbits
    if data[:2] == b"P6":
        return "PPM", True, _netpbm_header_len(data)
    if data[:2] == b"P5":
        return "PGM", True, _netpbm_header_len(data)
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return "PNG", False, 0
    if data[:2] == b"\xff\xd8":
        return "JPEG", False, 0
    return "RAW", False, 0


# --------------------------------------------------------------------------- #
# synthetic uncompressed image (no image library needed -- the offline default)
# --------------------------------------------------------------------------- #
def make_synthetic_bmp() -> bytes:
    rows = []
    for y in range(H):
        row = bytearray()
        for x in range(W):
            if x < W // 3:
                r, g, b = 25, 25, 30
            elif x < 2 * W // 3:
                r, g, b = 240, 200, 40
            else:
                v = (x * 7 + y * 13) % 256
                r, g, b = v, (v * 2) % 256, (v * 3) % 256
            row += bytes((b, g, r))
        row += b"\x00" * ((-len(row)) % 4)
        rows.append(bytes(row))
    pixels = b"".join(reversed(rows))
    header = (b"BM" + struct.pack("<IHHI", 54 + len(pixels), 0, 0, 54)
              + struct.pack("<IiiHHIIiiII", 40, W, H, 1, 24, 0,
                            len(pixels), 2835, 2835, 0, 0))
    return header + pixels


def to_grayscale_pgm(data: bytes) -> bytes:
    """Convert any image to an uncompressed 8-bit PGM (cleanest penguin, no shear)."""
    from PIL import Image
    import io
    img = Image.open(io.BytesIO(data)).convert("L")
    out = io.BytesIO()
    img.save(out, format="PPM")          # Pillow writes P5 (PGM) for mode 'L'
    return out.getvalue()


# --------------------------------------------------------------------------- #
def main() -> None:
    ap = argparse.ArgumentParser(description="ECB penguin (works on file bytes).")
    ap.add_argument("-i", "--in", dest="inp", help="input image (omit = synthetic BMP)")
    ap.add_argument("-o", "--out", dest="out", default="out", help="output dir (default: out)")
    ap.add_argument("--full", action="store_true",
                    help="encrypt the ENTIRE file incl. header (output won't render)")
    ap.add_argument("--gray", action="store_true",
                    help="convert to grayscale PGM first (cleanest penguin; needs Pillow)")
    args = ap.parse_args()

    # 1) load bytes
    if args.inp:
        with open(args.inp, "rb") as f:
            data = f.read()
        src = os.path.basename(args.inp)
    else:
        data = make_synthetic_bmp()
        src = "synthetic.bmp"

    # 2) optional grayscale conversion (makes it an uncompressed PGM)
    if args.gray:
        try:
            data = to_grayscale_pgm(data)
            src = os.path.splitext(src)[0] + ".pgm"
        except ImportError:
            sys.exit("--gray needs Pillow:  pip install pillow")

    name, uncompressed, hlen = sniff(data)
    ext = os.path.splitext(src)[1] or ".bin"
    stem = os.path.splitext(src)[0]          # name every output after the INPUT file
    if args.gray:
        stem += "_grayscale"                 # so a --gray run never overwrites the color run
    os.makedirs(args.out, exist_ok=True)

    def w(fname, blob):
        path = os.path.join(args.out, fname)
        with open(path, "wb") as f:
            f.write(blob)
        return path

    # 3) split header / body according to mode
    hdr_len = 0 if args.full else hlen
    header, body = data[:hdr_len], data[hdr_len:]
    eb, cb = ecb_stream(body), cbc_stream(body)

    sp = w(f"{stem}_sample{ext}", data)
    ep = w(f"{stem}_ecb{ext}", header + eb)
    cp = w(f"{stem}_cbc{ext}", header + cb)

    # 3b) PNG previews for the viewable cases, so you can just double-click instead of
    #     hunting for a PGM/BMP viewer. Skipped when --full (won't render) or compressed.
    previews = []
    if uncompressed and not args.full:
        try:
            from PIL import Image
            import io
            for tag, blob in (("ecb", header + eb), ("cbc", header + cb)):
                pv = os.path.join(args.out, f"{stem}_{tag}.png")
                Image.open(io.BytesIO(blob)).save(pv)
                previews.append(pv)
        except Exception:
            pass  # Pillow missing or bytes unreadable; the native files are still written

    # 4) explain what just happened
    print(f"[+] input: {src}  ({name}, {'uncompressed' if uncompressed else 'COMPRESSED'})")
    print(f"[+] wrote {ep}, {cp}, {sp}  (in {args.out}/)")
    if previews:
        print(f"[+] PNG previews (open these on any OS): {', '.join(previews)}")
    print(f"[+] duplicated 16-byte blocks in body   ECB: {count_repeats(eb):6d}"
          f"    CBC: {count_repeats(cb):6d}    (plaintext body: {count_repeats(body)})")

    if not uncompressed:
        # PNG/JPEG/RAW: there's no cleanly-separable header to keep, so the WHOLE file
        # was encrypted. --full vs plain -i make no difference on a compressed input.
        print(f"[x] COMPRESSED format ({name}): the whole file was ECB-encrypted, so {ep}")
        print("    won't open -- but that is NOT the point. The duplicated-block count was")
        print("    already ~0 BEFORE encrypting: compression had already stripped the byte")
        print("    repetition ECB leaks. (--full changes nothing here -- the whole file is")
        print("    encrypted either way.) The trick needs an UNCOMPRESSED image (BMP/PPM/PGM).")
    elif args.full:
        print(f"[!] --full: the HEADER was encrypted too. open {ep} -> it will NOT")
        print("    render: no valid magic bytes / dimensions, so no decoder can read it.")
        print("    Lesson: destroy the header and even an uncompressed image is unviewable.")
    else:
        print(f"[=] header kept, pixels ECB-encrypted. open {ep} -> the picture")
        print(f"    STILL LEAKS (solid regions visible). open {cp} -> noise.")
        print("    Lesson: ECB reveals equality; identical plaintext blocks -> identical ciphertext.")


if __name__ == "__main__":
    main()
