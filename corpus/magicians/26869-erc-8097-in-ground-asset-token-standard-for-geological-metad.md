---
source: magicians
topic_id: 26869
title: "ERC-8097: In-Ground Asset Token — Standard for Geological Metadata, Compliance & Extraction-Aware Token Models"
author: solomon
date: "2025-12-03"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-8097-in-ground-asset-token-standard-for-geological-metadata-compliance-extraction-aware-token-models/26869
views: 57
likes: 1
posts_count: 1
---

# ERC-8097: In-Ground Asset Token — Standard for Geological Metadata, Compliance & Extraction-Aware Token Models

Hello everyone,

This thread is for community discussion of **ERC-8097**, a proposed Ethereum standard that defines how **in-ground natural resources** (minerals, metals, subsurface materials) can be represented as **structured, machine-verifiable metadata**.

PR: [Add ERC: In-Ground Asset Token by solomonashok · Pull Request #1387 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/1387)

# Summary

**ERC-8097** introduces a metadata structure and lifecycle model for **in-ground mineral assets**, including:

- Geological & resource metadata
- Compliance metadata (JORC / NI 43-101 / SAMREC / PERC)
- Tenure & jurisdiction metadata
- ESG & rehabilitation requirements
- Extraction & depletion events
- Competent Person (CP/QP) digital attestations (EIP-712)

The goal is to provide a **common, open, interoperable metadata standard** for the global mining sector, enabling:

- Machine-verifiable geological truth
- Automated compliance validation
- Auditable resource lifecycle updates
- Optional tokenization of verified reserves

This is **NOT** a financial instrument standard.

It is a **data and compliance standard** for mineral assets.

---

# Motivation

Geological data today lives in PDFs, unstructured text, tables, and scattered reports.

There is no unified way to represent:

- JORC resource statements
- NI 43-101 technical data
- Competent Person sign-off
- Reserve classification (Measured / Indicated / Inferred / Proven / Probable)
- ESG obligations
- Extraction & depletion events

ERC-8097 aims to create a **structured metadata framework**, similar in spirit to ERC-721 and ERC-1155, but specialized for geological assets and compliant with global reporting standards.

---

# Key Metadata Objects

ERC-8097 defines a set of metadata objects:

- IRO – In-Ground Resource Object
- IGO – Geology Object
- ICO – Compliance Object (CP/QP attestation)
- ITO – Tenure & Jurisdiction Object
- IEXO – Extraction & Depletion Object
- IEO – ESG & Rehabilitation Object

These objects can be stored off-chain, with **on-chain hashing** and version control for immutability.

---

# Compliance & Attestation

Competent Persons (CP/QP) can digitally sign metadata using:

- EIP-712 typed signatures
- Identity frameworks (EIP-780 / EIP-735)

This allows regulators, auditors, and institutions to verify that geological data was approved by qualified experts.

---

# Optional Token Extensions

ERC-8097 supports optional token models:

### IGA-T (Fixed Supply)

Represents a set quantity of in-ground reserves.

### IGA-X (Extraction-Linked)

Token supply adjusts based on validated extraction events recorded through **IEXO**.

### IGA-C (Compliance / ESG Instruments)

For rehabilitation bonds, environmental commitments, sustainability-linked instruments.

These extensions are optional and built on top of the metadata standard.

---

# Use Cases

- Mapping JORC/NI 43-101 data to structured metadata
- Institution-grade mineral asset verification
- Digital reporting for auditors and regulators
- Lifecycle tracking of extraction
- Bonding, ESG, and rehabilitation accountability
- Optional tokenization for financing (RWA)
- Streaming / royalty / pre-pay instruments

---

# Request for Feedback

We are seeking feedback on:

- Metadata structure
- Compatibility with mineral reporting codes
- Approaches to CP/QP identity verification
- Extraction update logic
- ESG modeling
- Optional token extensions

Any comments, criticisms, or contributions are welcome.

Thank you!

— Solomon

Author, ERC-8097
