---
source: magicians
topic_id: 27360
title: "ERC-8117: Compressed Display Format for (EVM) Addresses"
author: xinbenlv
date: "2025-12-30"
category: ERCs
tags: [erc, wallet, address-space]
url: https://ethereum-magicians.org/t/erc-8117-compressed-display-format-for-evm-addresses/27360
views: 137
likes: 11
posts_count: 6
---

# ERC-8117: Compressed Display Format for (EVM) Addresses

Github PR: https://github.com/ethereum/ERCs/pull/1438

## ERC: 8117

title: Compressed Display Format for EVM Addresses

description: A display format for abbreviating consecutive identical hex characters in EVM addresses using run-length encoding for UI and logging.

author: Zainan Victor Zhou ([@xinbenlv](/u/xinbenlv))

discussions-to: [ERC-8117: Compressed Display Format for (EVM) Addresses](https://ethereum-magicians.org/t/erc-compressed-display-format-for-evm-addresses/27360)

status: Draft

type: Standards Track

category: ERC

created: 2025-12-30

requires: 55

## Abstract

This ERC proposes a standard presentation layer transformation for Ethereum addresses containing long sequences of identical hexadecimal digits. It defines two representation formats: a Unicode-based format using superscripts for graphical user interfaces (UI), and an ASCII-safe fallback format using bracket notation for logs and terminals. This standard aims to improve human readability and safety verification without altering the underlying address data.

## Motivation

As the Ethereum ecosystem matures, addresses with long repeating sequences are becoming increasingly common due to several factors:

**Vanity Addresses & CREATE2:** Factories and developers frequently generate “vanity” addresses with specific prefixes or suffixes for branding or identification.

**Gas Optimization (EIP-7939):** With proposals like EIP-7939 aiming to reduce gas costs for zero bytes in calldata, there is an economic incentive to deploy contracts at addresses containing large sequences of zeros to optimize cross-contract call costs.

**Security Risks:** The human eye struggles to distinguish between long sequences of identical characters (e.g., counting 10 zeros vs. 11 zeros). This creates a “homoglyph-like” vulnerability where users may skim over the middle of an address, missing subtle differences in a phishing scam.

Current truncation methods (e.g., `0x1234...5678`) obscure the internal structure of the address. A standardized compression format allows users to verify the magnitude of the repeated sequence (e.g., “exactly 11 zeros”) at a glance.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

The compression transformation applies only to the visual representation of the address.

### 1. Trigger Condition

Compression SHOULD be applied if a sequence of identical hexadecimal nibbles has a length $L$, where $L \geq 6$.

### 2. Formatting Rules

The standard defines two modes of display. Implementations must preserve the first character of the repeating sequence to indicate which character is being repeated, followed by a count of the total length of the sequence.

#### Mode A: Unicode Display (UI/Frontend)

Recommended for Wallets, Block Explorers, and Mobile Apps.

**Syntax:** `0x` + `[repeating_char]` + `[superscript_count]` + `[remainder]`

**Encoding:** The count integer is converted to Unicode Superscript characters (U+2070 to U+2079).

**Example:**

- Raw: 0x00000000000000000044... (Eighteen 0s)
- Display: 0x0¹⁸44...

#### Mode B: ASCII Fallback (CLI/Logs)

Recommended for Developer Consoles, Logs, and Copy-Paste operations.

**Syntax:** `0x` + `[repeating_char]` + `{` + `[count]` + `}` + `[remainder]`

**Example:**

- Raw: 0x00000000000000000044...
- Display: 0x0{18}44...

### 3. Case Sensitivity and

To preserve the checksum integrity defined in EIP-55 and EIP-1191:

- The compression MUST strictly match identical ASCII characters.
- The compression MUST NOT be applied to mixed-case sequences (e.g., aAaA cannot be compressed).
- All non-compressed characters MUST retain their original casing.

## Rationale

### Industry Precedents & Alignment

**Regex Alignment (ASCII Mode):** We selected the curly brace syntax `Byte{n}` (e.g., `0{8}`) because it aligns with the universal Regular Expression standard for quantification. Developers intuitively understand `{n}` as “repeat n times.”

**Divergence from IPv6:** Unlike IPv6, which uses `::` to represent “fill the gap with zeros,” EVM vanity addresses rely on the specific count of characters for identity. Therefore, an explicit count (`{8}`) is safer than an implicit gap (`::`).

### Superscript vs. Subscript (UI Mode)

While subscript notation (e.g., $H_2O$) implies component count in chemistry, this ERC selects Superscript (`0⁸`) for the following reasons:

**Legibility:** Superscripts generally render more clearly on digital displays and do not conflict with text underlines (hyperlinks) or font baselines.

**Metaphor:** Superscripts serve as a visual metaphor for Scientific Notation, indicating the magnitude or length of the sequence, rather than a mathematical power operation.

### Gas Optimization Context

With the introduction of logic similar to EIP-7939 (scaling gas costs based on calldata zeros), the ecosystem will see a proliferation of addresses engineered to have maximum zero bytes. A display format that handles these specific addresses gracefully is a necessary proactive measure for user experience.

## Backwards Compatibility

This ERC is strictly a presentation layer standard.

**Wallets:** Must strip the compression formatting (convert back to full hex) before signing or broadcasting transactions.

**Safety:** The characters `{`, `}`, and Unicode superscripts are not valid hexadecimal characters. If a user blindly copies a compressed address into a legacy system, the system will reject the input as invalid rather than processing a wrong address. This acts as a fail-safe mechanism.

## Reference Implementation

The following Python implementation demonstrates the logic for both Unicode and ASCII modes, covering full display and truncated variations.

```python
import re

class AddressCompressor:
    SUPERSCRIPTS = {
        '0': '\u2070', '1': '\u00B9', '2': '\u00B2', '3': '\u00B3', '4': '\u2074',
        '5': '\u2075', '6': '\u2076', '7': '\u2077', '8': '\u2078', '9': '\u2079'
    }

    def __init__(self, address):
        self.full_address = address
        # Remove 0x for processing
        self.clean_address = address[2:] if address.startswith("0x") else address

    def _to_superscript(self, number):
        """Converts an integer to a string of unicode superscripts."""
        return "".join(self.SUPERSCRIPTS.get(digit, digit) for digit in str(number))

    def format(self, mode='unicode', truncate=False):
        """
        Modes: 'unicode' (0⁸) or 'ascii' (0{8})
        Truncate: If True, keeps start/end context only.
        """

        def replacer(match):
            seq = match.group(0)
            length = len(seq)
            char = seq[0]

            # Trigger threshold >= 6
            if length CC0.

## Replies

**wjmelements** (2025-12-31):

> Syntax: 0x + [repeating_char] + [superscript_count] + [remainder]

I have encountered a situation where it was important for the last few chars to be zero; it saved some gas and weakened certain transaction substitution attacks. Suffix mining might also be a trend in the future; for example, Uniswap V4 hooks use the trailing bits as flags. Also, the UniswapV3 factory used a mined address for both the prefix and the suffix. Therefore, instead of `remainder`, the repeating compression should be applied for *all* repeating characters in the entire address, not only at the beginning.

---

**xinbenlv** (2025-12-31):

Thanks [@wjmelements](/u/wjmelements)

In additional to what you suggest prefix or suffix, do you think it’s worth adding that “anywhere in the address is eligible, as long as more than 6 digits are identical”?

---

**wjmelements** (2025-12-31):

Yes.

I proposed another compression scheme last year. It cuts address text width slightly by using base256emoji and makes addresses more memorable. It might save more space on average if the address domain has few repeating characters.


      ![](https://eips.ethereum.org/assets/images/favicon.png)

      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-7673)





###



Depict Account Addresses As A String of Emoji

---

**xinbenlv** (2025-12-31):

That’s an interesting idea haha

---

**Vectorized** (2026-01-03):

Like the overall idea.

Agree on extending the scheme to allow both leading and trailing repeated characters.

Thinking of having a *suggested* minimum number of consecutive characters before this formatting is applied. If so, 5 or more repeating consecutive characters feels like a good threshold (long enough to prevent UI cluttering, short enough to make it feasible for CPU based mining).

