#!/usr/bin/env python3
"""Steganographic LSB fingerprinting for PNG images.

Embeds a UTF-8 string into the least significant bit of the red channel.
Only LSB is touched — completely imperceptible to the human eye.

Usage:
  python fingerprint.py /path/to/frames/           # Embed in all PNGs
  python fingerprint.py /path/to/image.png --extract  # Extract proof
"""
import argparse, struct, sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Installing Pillow...", file=sys.stderr)
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow", "-q"])
    from PIL import Image

FINGERPRINT = "WhisperCanvas by Emeka Ajufo | github.com/Bladefitness/whisper-canvas"

def _msg_to_bits(msg):
    enc = msg.encode("utf-8")
    data = struct.pack(">I", len(enc)) + enc
    bits = []
    for byte in data:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    return bits

def _bits_to_msg(bits):
    if len(bits) < 32:
        raise ValueError("Not enough data")
    length = 0
    for b in bits[:32]:
        length = (length << 1) | b
    need = 32 + length * 8
    if len(bits) < need:
        raise ValueError(f"Need {need} bits, have {len(bits)}")
    msg_bytes = bytearray()
    for i in range(32, need, 8):
        byte = 0
        for b in bits[i:i+8]:
            byte = (byte << 1) | b
        msg_bytes.append(byte)
    return msg_bytes.decode("utf-8")

def embed(path, msg=FINGERPRINT):
    bits = _msg_to_bits(msg)
    img = Image.open(path).convert("RGBA")
    pixels = list(img.getdata())
    if len(pixels) < len(bits):
        raise ValueError(f"Image too small for fingerprint")
    new = []
    for idx, px in enumerate(pixels):
        if idx < len(bits):
            r, g, b, a = px
            r = (r & 0xFE) | bits[idx]
            new.append((r, g, b, a))
        else:
            new.append(px)
    img.putdata(new)
    img.save(path, format="PNG")

def extract(path):
    img = Image.open(path).convert("RGBA")
    pixels = list(img.getdata())
    bits = [(px[0] & 1) for px in pixels[:32 + 10000 * 8]]
    return _bits_to_msg(bits)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("path", type=Path)
    p.add_argument("--extract", action="store_true")
    args = p.parse_args()
    if args.extract:
        print(f"Extracted: {extract(args.path)!r}")
    elif args.path.is_dir():
        pngs = sorted(args.path.glob("*.png"))
        print(f"Fingerprinting {len(pngs)} images...")
        for png in pngs:
            embed(png)
            print(f"  done: {png.name}")
        print("All done.")
    else:
        embed(args.path)
        print(f"Done: {args.path.name}")
