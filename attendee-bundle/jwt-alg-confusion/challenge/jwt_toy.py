#!/usr/bin/env python3
"""
Tiny base64url / JWT segment helpers for the algorithm-confusion lab.

A JWT is three base64url parts joined by dots:  header.payload.signature
These helpers build the parts; you assemble the token yourself in client.py.
"""
import base64
import json


def b64u_enc(raw: bytes) -> str:
    """base64url-encode, no padding (JWT style)."""
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()


def b64u_dec(s: str) -> bytes:
    """base64url-decode, tolerating missing padding."""
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


def _part(obj) -> str:
    """Turn a dict into one base64url JWT segment."""
    return b64u_enc(json.dumps(obj, separators=(",", ":")).encode())
