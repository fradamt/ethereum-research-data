---
source: magicians
topic_id: 27515
title: "ERC-8128: Signed HTTP Requests with Ethereum"
author: jacopo-eth
date: "2026-01-19"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-8128-signed-http-requests-with-ethereum/27515
views: 82
likes: 2
posts_count: 1
---

# ERC-8128: Signed HTTP Requests with Ethereum

Discussion for ERC-8128: Signed HTTP Requests with Ethereum — a standard for authenticating generic HTTP requests using Ethereum accounts via HTTP Message Signatures.



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/1478)














####


      `master` ← `slice-so:temp-eth-http-message-signatures`




          opened 05:16PM - 16 Jan 26 UTC



          [![](https://avatars.githubusercontent.com/u/39241410?v=4)
            jacopo-eth](https://github.com/jacopo-eth)



          [+516
            -0](https://github.com/ethereum/ERCs/pull/1478/files)













A list of open questions can be found below. Feel free to join the [Telegram group](https://t.me/+oVfVGLx41x45YzE0) for more synchronous discussions.

## Open Questions

### Keyid format

`keyid` is used as the primary identity binding, encoded as `eip8128:<chainId>:<address>`. The eip8128 namespace intentionally reuses the CAIP-10 (eip155) account identifier syntax and semantics, but with a distinct prefix to make signatures explicitly scoped to this specification. A design question remains whether `keyid` alone is sufficient to express the signer’s intent to be verified under this EIP’s rules, or whether an explicit discriminator (e.g., a `tag` field or a dedicated signature parameter) should be standardized to remove ambiguity and make verification semantics opt-in.

An alternative under discussion is adopting `eip155:<chainId>:<address>` as the primary identity binding in order to reuse the existing EIP-155 namespace. This would avoid introducing a new prefix, but at the cost of increased semantic ambiguity, since `eip155` does not inherently scope signatures to this specification.

The second preferred option is `eip8128;eip155:<chainId>:<address>` which avoids ambiguity and reuses the canonical address format, at the cost of a more verbose syntax.

### Future-proofing for alternative EOA signing algorithms

It is plausible that future Ethereum account models may allow EOAs authenticated by algorithms other than ECDSA over secp256k1 (e.g., P-256).

Supporting this in HTTP signatures would require:

1. a standard mechanism to derive or bind an Ethereum address from signatures produced under additional algorithms, and
2. a way for verifiers to determine which algorithm is used, currently inferred from keyid.

The former is out of scope and would require a separate proposal. The latter interacts with algorithm signaling: RFC 9421 requires that any algorithm hints (e.g., `alg`) be consistent with trusted configuration and/or key material, and that verifiers fail verification if conflicting sources are present, in order to prevent algorithm confusion attacks.

The open question is whether potential multi-algorithm EOAs can be supported safely, without weakening the default behavior inferred from `keyid` or requiring out-of-band agreement between signers and verifiers. One option considered is to:

- introduce a dedicated keyid namespace for multi-algorithm EOAs, e.g. eip8128-multi::, which explicitly signals to verifiers that additional parameters must be resolved, and
- standardize the deployment of a smart contract on each  that acts as an on-chain registry, allowing signers to associate signature-related parameters (e.g., alg, public key material) with their keyid, and enabling verifiers to retrieve these parameters as part of the verification process.

### Optional fallback headers

Some HTTP environments make it difficult to preserve Structured Fields exactly (e.g., legacy gateways, restrictive middleware, or limited client stacks).

An open question is whether optional fallback headers (specific to Ethereum-signed HTTP messages) that carry the same information as `Signature-Input` / `Signature` should be defined, in order to improve deployability in constrained environments. The tradeoff is increased surface area, potential duplication, and new normalization rules; if introduced, fallback headers should be strictly optional and must not create multiple authoritative encodings for the same proof.
