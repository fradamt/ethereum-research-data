"""Extract EIP references from any text.

Handles patterns like ``EIP-1559``, ``eip-4844``, ``EIP 7251``, ``EIP1559``.
Filters out false positives inside URLs and fenced code block metadata lines.
"""

from __future__ import annotations

import re

__all__ = ["extract_eip_refs"]

# Matches EIP/ERC followed by optional separator and 1-6 digit number.
# Captures the number in group 1.
_EIP_PATTERN = re.compile(
    r"""
    (?<![/\w])          # not preceded by / or word char (avoids mid-URL matches)
    (?:EIP|ERC|eip|erc) # keyword
    [-–— \t]*           # optional separator: hyphen, dash, or whitespace
    (\d{1,6})           # EIP number (1-6 digits)
    (?!\d)              # not followed by more digits
    """,
    re.VERBOSE,
)

# Fenced code block delimiter (``` or ~~~)
_FENCE_RE = re.compile(r"^(`{3,}|~{3,})")


def extract_eip_refs(text: str) -> list[int]:
    """Return sorted, deduplicated EIP numbers referenced in *text*.

    Skips matches found inside fenced code blocks to avoid false positives
    from code snippets and URLs.
    """
    if not text:
        return []

    eips: set[int] = set()
    in_fence = False
    fence_marker = ""

    for line in text.split("\n"):
        stripped = line.strip()

        # Track fenced code blocks
        fence_match = _FENCE_RE.match(stripped)
        if fence_match:
            marker_char = fence_match.group(1)[0]
            marker_len = len(fence_match.group(1))
            if not in_fence:
                in_fence = True
                fence_marker = marker_char * marker_len
            elif stripped.startswith(fence_marker[0] * len(fence_marker)):
                in_fence = False
                fence_marker = ""
            continue

        if in_fence:
            continue

        for m in _EIP_PATTERN.finditer(line):
            num = int(m.group(1))
            if num > 0:
                eips.add(num)

    return sorted(eips)
