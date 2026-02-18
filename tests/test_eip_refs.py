"""Tests for erd_index.enrich.eip_refs — EIP reference extraction."""

from __future__ import annotations

from erd_index.enrich.eip_refs import extract_eip_refs

# ---------------------------------------------------------------------------
# Basic patterns
# ---------------------------------------------------------------------------


class TestBasicPatterns:
    def test_eip_hyphen(self):
        assert extract_eip_refs("Implements EIP-1559") == [1559]

    def test_eip_lowercase(self):
        assert extract_eip_refs("See eip-4844 for blobs") == [4844]

    def test_erc_hyphen(self):
        assert extract_eip_refs("Token follows ERC-20 standard") == [20]

    def test_erc_lowercase(self):
        assert extract_eip_refs("erc-721 NFTs") == [721]

    def test_eip_space(self):
        assert extract_eip_refs("Proposed in EIP 7251") == [7251]

    def test_eip_no_separator(self):
        assert extract_eip_refs("EIP1559 changed gas") == [1559]

    def test_eip_tab_separator(self):
        assert extract_eip_refs("EIP\t4844") == [4844]

    def test_eip_en_dash(self):
        assert extract_eip_refs("EIP\u20131559") == [1559]

    def test_eip_em_dash(self):
        assert extract_eip_refs("EIP\u20144844") == [4844]


# ---------------------------------------------------------------------------
# No-match cases
# ---------------------------------------------------------------------------


class TestNoMatch:
    def test_bare_eip_no_number(self):
        assert extract_eip_refs("The EIP process is important") == []

    def test_eip_in_word(self):
        assert extract_eip_refs("RECEIPT or recipe") == []

    def test_empty_string(self):
        assert extract_eip_refs("") == []

    def test_no_eip_mentions(self):
        assert extract_eip_refs("Ethereum is a blockchain platform") == []

    def test_zero_eip_number(self):
        assert extract_eip_refs("EIP-0 is not valid") == []


# ---------------------------------------------------------------------------
# Deduplication and sorting
# ---------------------------------------------------------------------------


class TestDedupAndSorting:
    def test_dedup_same_format(self):
        assert extract_eip_refs("EIP-1559 EIP-1559 EIP-1559") == [1559]

    def test_dedup_different_formats(self):
        assert extract_eip_refs("EIP-1559 and eip-1559 and EIP 1559") == [1559]

    def test_sorted_output(self):
        refs = extract_eip_refs("EIP-4844, EIP-1559, EIP-20, EIP-7251")
        assert refs == [20, 1559, 4844, 7251]

    def test_mixed_eip_erc(self):
        refs = extract_eip_refs("EIP-1559 and ERC-20 and eip-4844")
        assert refs == [20, 1559, 4844]


# ---------------------------------------------------------------------------
# Fenced code block filtering
# ---------------------------------------------------------------------------


class TestCodeBlockFiltering:
    def test_backtick_fence(self):
        text = "EIP-100 outside\n```\nEIP-9999 inside fence\n```\nEIP-200 outside"
        refs = extract_eip_refs(text)
        assert 100 in refs
        assert 200 in refs
        assert 9999 not in refs

    def test_tilde_fence(self):
        text = "EIP-100\n~~~\nEIP-9999\n~~~\nEIP-200"
        refs = extract_eip_refs(text)
        assert 100 in refs
        assert 200 in refs
        assert 9999 not in refs

    def test_fence_with_language_tag(self):
        text = "EIP-100\n```python\nEIP-9999\n```\nEIP-200"
        refs = extract_eip_refs(text)
        assert 100 in refs
        assert 200 in refs
        assert 9999 not in refs

    def test_nested_fence_longer_marker(self):
        text = "EIP-100\n````\nEIP-9999\n````\nEIP-200"
        refs = extract_eip_refs(text)
        assert 100 in refs
        assert 200 in refs
        assert 9999 not in refs

    def test_unclosed_fence_skips_rest(self):
        text = "EIP-100\n```\nEIP-9999"
        refs = extract_eip_refs(text)
        assert 100 in refs
        assert 9999 not in refs


# ---------------------------------------------------------------------------
# URL and context filtering
# ---------------------------------------------------------------------------


class TestURLFiltering:
    def test_eip_preceded_by_slash(self):
        # /eip-1234 should not match due to negative lookbehind on /
        assert extract_eip_refs("/eip-1234") == []

    def test_url_path_segment(self):
        assert extract_eip_refs("https://eips.ethereum.org/EIPS/eip-1234") == []

    def test_eip_preceded_by_word_char(self):
        # xEIP-1234 should not match due to negative lookbehind on \w
        assert extract_eip_refs("xEIP-1234") == []


# ---------------------------------------------------------------------------
# Mixed realistic content
# ---------------------------------------------------------------------------


class TestMixedContent:
    def test_realistic_forum_post(self):
        text = """
# Blob Gas Market Analysis

EIP-4844 introduced blob transactions. The fee market follows EIP-1559
mechanics but with a separate base fee. See also ERC-4337 for account
abstraction which interacts with blob transactions.

```python
# EIP-9999 is referenced in this code comment but should be ignored
GAS_PER_BLOB = 131072  # 2**17
```

For more context, see eip-7251 (MaxEB) and EIP 7002 (EL exits).
"""
        refs = extract_eip_refs(text)
        assert refs == [1559, 4337, 4844, 7002, 7251]
        assert 9999 not in refs

    def test_multiple_eips_on_one_line(self):
        refs = extract_eip_refs("Requires EIP-1559, EIP-4844, and EIP-7251")
        assert refs == [1559, 4844, 7251]

    def test_six_digit_eip(self):
        assert extract_eip_refs("EIP-100000") == [100000]

    def test_seven_digit_rejected(self):
        # Pattern allows 1-6 digits only
        assert extract_eip_refs("EIP-1234567") == []
