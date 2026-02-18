---
source: magicians
topic_id: 27661
title: "ERC Proposal: GitHub Actions Attestation Verification"
author: amiller
date: "2026-02-05"
category: EIPs
tags: [erc, zkp, attestation, github]
url: https://ethereum-magicians.org/t/erc-proposal-github-actions-attestation-verification/27661
views: 8
likes: 1
posts_count: 1
---

# ERC Proposal: GitHub Actions Attestation Verification

Hi eth magicians, I’m writing to propose a standard interface for verifying GitHub Actions attestations on-chain. The idea is that GitHub workflows produce Sigstore-signed artifacts, and we can verify those signatures in a smart contract via ZK proofs.

## Abstract

This specification defines functions for verifying that an artifact was produced by a specific GitHub repository at a specific commit. The proof guarantees a valid Sigstore certificate chain binding repo, commit, and artifact hash together.

```solidity
interface IGitHubAttestation {
    struct Attestation {
        bytes32 artifactHash;  // SHA-256 of the attested artifact
        bytes32 repoHash;      // SHA-256 of "owner/repo"
        bytes20 commitSha;     // Git commit that ran the workflow
    }

    function verify(bytes calldata proof, bytes32[] calldata publicInputs)
        external view returns (bool valid);

    function verifyAndDecode(bytes calldata proof, bytes32[] calldata publicInputs)
        external view returns (Attestation memory);
}
```

## Motivation

Oracles and zkTLS remain an unsolved problem, when we want flexible like API responses and what a website showed you. The main approaches are zkTLS projects (TLSNotary, Opacity, Reclaim, zkPass, Pluto) which use MPC or proxy-based attestation.

These work, but they require new infrastructure beyond a blockchain and ZKP, specifically notary networks, MPC coordination, or trusted proxies

GitHub Actions offers a different tradeoff. Developers often already trust GitHub with their code and secrets. Why not use repurpose this for something else? A Github Actions workflow can:

1. Run a headless browser with session cookies (stored as GitHub Secrets)
2. Capture authenticated content
3. Output an artifact that GitHub signs via Sigstore

The workflow code is visible at the attested commit, so verifiers can audit exactly what ran. No new trust assumptions beyond GitHub.

## How it works

GitHub Actions uses Sigstore to sign workflow artifacts:

1. Workflow requests OIDC token from GitHub
2. Sigstore’s Fulcio CA issues ephemeral certificate with GitHub claims (repo, commit, workflow)
3. Workflow signs artifact with this key

The attestation is ~4KB of JSON + X.509 certificates. Direct on-chain verification would cost millions of gas. The ZK circuit compresses this to ~300k gas by verifying:

- P-384 ECDSA: Fulcio intermediate CA signed the leaf cert
- P-256 ECDSA: Leaf cert signed the DSSE envelope
- Claim extraction: repo, commit, artifact hash from certificate extensions

## Reference Implementation

Deployed on Base Sepolia:

- Verifier: 0x0Af922925AE3602b0dC23c4cFCf54FABe2F54725
- Example faucet: 0xf31768d4E42d5e80aE95415309D7908ae730Fb41

The example faucet lets you claim Base Sepolia once per day per unique github account, but it does so without any other third parties involved (you use your own github repo to run the action and compute the ZKP locally and upload directly to the smart contract).

Source: [GitHub - amiller/github-zktls](https://github.com/amiller/github-zktls)

### Circuit details

Written in Noir, uses UltraHonk (Barretenberg). Key dependencies from [zkpassport](https://github.com/zkpassport):

- noir-bignum / noir-ecdsa for P-384 ECDSA (certificate chain)
- P-256 uses Noir stdlib

Design choices:

- Hardcoded CA key: Fulcio intermediate pubkey is a circuit constant (avoids passing cert chain, but requires update for CA rotation)
- Witness-provided offsets: Prover provides byte offsets for pubkey/OIDC claims in certificate. Circuit validates data at those offsets. Avoids expensive DER parsing in-circuit.
- Low-s normalization: Witness generator normalizes ECDSA signatures to low-s form

Formats:

- DSSE (Dead Simple Signing Envelope) with PAE encoding
- In-toto statement for artifact provenance
- X.509 OIDC extensions (OID 1.3.6.1.4.1.57264.1.*) for GitHub claims

### Prover costs

| Metric | Value |
| --- | --- |
| Circuit size | ~256k ACIR opcodes |
| Proof generation | ~7 seconds (16 threads) |
| Peak RAM | 1.6 GB |
| Proof size | 11 KB |
| Public inputs | 2.7 KB (84 field elements) |
| On-chain verification | ~300k gas |

The prover is packaged as a Docker image (1.4 GB) containing Nargo 1.0.0-beta.17 and Barretenberg v3.0.3. Circuit and VK are pre-compiled in the image; witness generation runs in JavaScript (<1s).

## Use cases

- Identity: Prove GitHub/Twitter account ownership via authenticated profile capture
- Web proofs: Prove what a website showed you (balances, receipts)
- AI-judged escrow: Run an LLM judge in a workflow, attest the verdict
- Verifiable builds: Prove bytecode matches a build from a known repo

## Comparison to other approaches

| Approach | Trust model | New infra needed | Privacy |
| --- | --- | --- | --- |
| TLSNotary | MPC (2PC) | Notary coordination | Strong |
| Opacity | MPC + Eigenlayer AVS | Notary network | Strong |
| Reclaim | HTTPS proxy | Proxy servers | Medium |
| zkPass | 3P-TLS + MPC | Node network | Strong |
| Chainlink Functions | DON operators | Subscription | Operator sees data |
| GitHub Actions | GitHub | None (existing CI) | GitHub sees session |

## Open questions

1. Should the struct include an issuerHash field to potentially support GitLab/CircleCI later? Or keep it GitHub-specific?
2. ERC-165 support?
3. The Fulcio intermediate CA expires 2031. How should contracts handle CA rotation?

## Related work

- Sigstore: https://sigstore.dev
- npm provenance (same trust model): Generating provenance statements | npm Docs
- TLSNotary: https://tlsnotary.org
- Opacity: https://opacity.network
- Reclaim: https://reclaimprotocol.org
- zkPass: https://zkpass.org
