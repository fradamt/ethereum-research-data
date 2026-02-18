---
source: magicians
topic_id: 24530
title: "ERC-7969: DKIM Registry Interface"
author: ernestognw
date: "2025-06-12"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-7969-dkim-registry-interface/24530
views: 284
likes: 16
posts_count: 9
---

# ERC-7969: DKIM Registry Interface

**New ERC: DKIM Registry Interface for Email-Based Account Abstraction**

Hi everyone! ![:wave:](https://ethereum-magicians.org/images/emoji/twitter/wave.png?v=12)

We’re proposing a new ERC for a standardized DKIM Registry Interface that enables on-chain registration and validation of DKIM public key hashes.

**Key Features:**

A simple interface for domain owners to register their DKIM key hashes that adapts well to current account abstraction wallets controlled via email and social recovery mechanisms. Keeps compatibility with ZKEmail infrastructure and presumably with others too

**Use Cases:**

- Email-controlled smart contract wallet and social recovery for account abstraction (e.g. through EIP-7913 and OpenZeppelin’s modules and signers)



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/1084)














####


      `master` ← `0xknon:feature/dkim-registry`




          opened 11:03AM - 12 Jun 25 UTC



          [![](https://avatars.githubusercontent.com/u/30591224?v=4)
            0xknon](https://github.com/0xknon)



          [+261
            -0](https://github.com/ethereum/ERCs/pull/1084/files)







Introduces a standard interface for registering and validating DKIM public key h[…](https://github.com/ethereum/ERCs/pull/1084)ashes on-chain.

This ERC enables email-based account abstraction and recovery by allowing domain owners to register their DKIM keys in a decentralized registry. Key features include domain hash validation, key hash registration/revocation events, and compatibility with ZK Email technology and ERC-4337. The interface provides a crucial building block for trustless email ownership verification, enabling users to create smart contract wallets and implement social recovery mechanisms using email credentials.












**Questions to kickoff the discussion**

- Does it makes sense to specify any form of raw key validation? It would make verification more resilient when infrastructure fails. The case I’m describing:

Email arrives with DKIM signature
- Verifier wants to check if key is valid in registry
- Normal flow: fetch public key from DNS → compute hash → call isKeyHashValid()
- Problem: If domain DNS is down, step 3 fails
- But verifier might have the raw key from other sources (IPFS, backup, email headers, other chains, etc.)
- May the standard could RECOMMEND or reference ERC-7913 (Signature Verifiers) for teams building on top of this registry? Since DKIM keys are address-less keys by nature, ERC-7913’s (verifier, key) model fits perfectly. Teams could:

Use this registry to validate DKIM key hashes
- Use ERC-7913 verifiers to actually verify DKIM signatures
- Build email-based account abstraction without deploying separate contracts per key

This creates a nice composable stack: DKIM Registry (key registration) + [ERC-7913](https://ethereum-magicians.org/t/erc-7913-key-verifiers/23262/1) (signature verification). This is the pattern OpenZeppelin Contracts is following extensively. Is it worth mentioning in the spec as a recommended pattern?

## Replies

**0xknon** (2025-06-12):

Nice work on the ERC for DKIM Registry Interface!

This is a crucial building block for email-based account abstraction and ZK Email technology.

Here are some assumptions on this ERC:

1. Single Authority Registry

Allows a single authority to manage a DKIM Registry
2. An aggregated registry can still follow the interface to serve its purpose.
3. Decentralized Aggregated Registry

Multiple centralized registries could be aggregated into a more decentralized system
4. This could be implemented in two ways:

Equal weighting: All registries have the same authority
5. Weighted aggregation: Different registries have different trust levels
6. This approach would provide:

Better resilience through redundancy
7. Reduced single points of failure
8. More distributed trust model

---

**0xknon** (2025-06-12):

Regarding the raw key validation, I think the steps should be:

1. Email arrives with DKIM signature
2. Verifier wants to check if key is valid in registry
3. Normal flow: fetch public key from DNS → compute hash → setKeyHash()
4. Problem: If domain DNS is down, step 3 fails
5. But verifier might have the raw key from other sources (IPFS, backup, email headers, other chains, etc.)
6. Use the keys from other sources (step 5) → compute hash → setKeyHash()

Then, the the onchain verification can still be performed even the DNS is down.

---

**ernestognw** (2025-06-15):

> Use the keys from other sources (step 5) → compute hash → setKeyHash()

Right this makes sense. My only concern would be that users arguably would prefer using calldata to pass the raw key rather than having the registry updated.

> Decentralized Aggregated Registry

This also makes sense. I think this is more of a consequence of the standard. By not specifying how the registry works, aggregation is not forbidden so I wouldn’t list it explicitly.

> Single Authority Registry

Perhaps it’d be convenient to suggest that the authority of the contract MAY set the public key hash for those whose DNS is down.

Does that make sense?

---

**0xknon** (2025-06-17):

> Right this makes sense. My only concern would be that users arguably would prefer using calldata to pass the raw key rather than having the registry updated.

I would argue that this may not be gas efficient to check the validity of the key.

> This also makes sense. I think this is more of a consequence of the standard. By not specifying how the registry works, aggregation is not forbidden so I wouldn’t list it explicitly.

Agree.

> Perhaps it’d be convenient to suggest that the authority of the contract MAY set the public key hash for those whose DNS is down.

Agree. In the meanwhile, do you think we should also add the requirement of “Performing DNSSEC Check before adding the key hash” on the EIP ? So, with the protection from DNSSEC, probably everyone can help on adding the key hash on the one registry.

---

**bomanaps** (2025-06-18):

Good job guys on this ![:heart:](https://ethereum-magicians.org/images/emoji/twitter/heart.png?v=12), current I feel this  current proposal would benefit from several technical enhancements before implementation.  (1) replacing the centralized ownership model with a decentralized domain verification system, (2) expanding the interface to handle DKIM selectors and multiple concurrent keys per domain, (3) clarifying the key preprocessing specification to ensure consistent implementation across different systems, (4) adding proper event parameters for the revocation mechanism.

Also left some comment on the PR so to pass the current error we have with the bot

---

**ernestognw** (2025-07-09):

Hey [@bomanaps](/u/bomanaps), thanks for the thoughtful feedback! I think we can consider these changes, but it’s perhaps up to [@0xknon](/u/0xknon) since he’s leading the ERC PR. Here’s my take on each point:

On (1), I haven’t seen established patterns for decentralized domain verification in practice yet. I think introducing a `registerKeyHash` function with domain proofs might be too opinionous for this interface standard. So far, the interface is intentionally minimal. It focuses on the core functionality (key validation) while leaving implementation details (like access control) to the implementer. Perhaps this design choice can be explained further in the “Rationale” section.

On (2), I think the main changes would be:

- Adding a bytes32 selector parameter to isKeyHashValid()
- Update events to include selector information
- Change the storage structure from mapping(bytes32 => mapping(bytes32 => bool)) to mapping(bytes32 => mapping(bytes32 => mapping(bytes32 => bool)))

This is a significant change to the current interface, so I’m curious about the reasoning for not including `selector` in the first place [@0xknon](/u/0xknon). Maybe that design decision should be documented in the Rationale section too.

On (3), I think the key encoding/processing is already clearly specified in the current standard, so additional clarification would be redundant.

On (4), I think the current `KeyHashRevoked(bytes32 domainHash)` is sufficient. As you noted, off-chain indexers tracking registrations would already have the `keyHash` from `KeyHashRegistered` events, so including it in revocation events would be redundant.

Thanks again for the detailed review!

---

**zkfriendly** (2025-07-14):

Thank you, nice to see a standard for DKIM key registration.

In the ERC, it notes that *“The keyHash parameter MUST be the keccak256 hash of the DKIM public key.”* One point to consider regarding this is that the DKIM public key hash is output as part of the public signals of zk circuits that prove a given email. In the verification phase, the verifier checks the validity of the outputted public key hash using the registry.

An important point to note here is that the circuits (e.g in the current implementation in zkEmail) output the **Poseidon** hash of the public key, not **keccak256**. This is because Poseidon is zk-friendly and significantly reduces proving time in practice.

For reference, a Keccak256 implementation typically requires 25,000 to 35,000 constraints, whereas Poseidon only requires 500 to 1,500. Given this substantial difference, it may be worth considering relaxing the requirement in the ERC — maybe either by not mandating keccak256 for the key hash, or by allowing the choice of hash function to be implementation-dependent (e.g., supporting Poseidon).

---

**ernestognw** (2025-07-15):

Thanks [@zkfriendly](/u/zkfriendly)!

It makes sense to not enforce `keccak256` exclusively. [I left a review in the PR](https://github.com/ethereum/ERCs/pull/1084#pullrequestreview-3021895420), making the specification more general.

I wonder if it makes sense using different hashing algorithms for the `keyHash` and `domainHash`. Otherwise it would be fine to also specify in the ERC that both MUST be consistent

