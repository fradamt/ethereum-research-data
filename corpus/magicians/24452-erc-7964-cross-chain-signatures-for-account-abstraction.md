---
source: magicians
topic_id: 24452
title: "ERC-7964: Cross-Chain Signatures for Account Abstraction"
author: ernestognw
date: "2025-06-05"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-7964-cross-chain-signatures-for-account-abstraction/24452
views: 329
likes: 4
posts_count: 8
---

# ERC-7964: Cross-Chain Signatures for Account Abstraction

Hi everyone! ![:waving_hand:](https://ethereum-magicians.org/images/emoji/twitter/waving_hand.png?v=15)

Following up on [ERC-7803](https://ethereum-magicians.org/t/erc-7803-eip-712-extensions-for-account-abstraction/21436/2), I’ve drafted **ERC-7964: Universal Cross-Chain Signatures for Account Abstraction** - a simple extension that enables cross-chain signatures using `chainId: 0`.

## Concept

One rule: **`chainId: 0` in signing domains = valid on any chain**

This allows users to sign once and authorize operations across multiple networks - perfect for cross-chain intents, multi-chain DAO voting, and unified account management.

## ERC



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/1069)














####


      `master` ← `ernestognw:feat/universal-cross-chain-signatures`




          opened 06:39AM - 05 Jun 25 UTC



          [![](https://avatars.githubusercontent.com/u/33379285?v=4)
            ernestognw](https://github.com/ernestognw)



          [+415
            -0](https://github.com/ethereum/ERCs/pull/1069/files)







When opening a pull request to submit a new EIP, please use the suggested templa[…](https://github.com/ethereum/ERCs/pull/1069)te: https://github.com/ethereum/EIPs/blob/master/eip-template.md

We have a GitHub bot that automatically merges some PRs. It will merge yours immediately if certain criteria are met:

 - The PR edits only existing draft PRs.
 - The build passes.
 - Your GitHub username or email address is listed in the 'author' header of all affected PRs, inside <triangular brackets>.
 - If matching on email address, the email address is the one publicly listed on your GitHub profile.

## Replies

**codebyMoh** (2025-06-06):

Thanks [@ernestognw](/u/ernestognw) — really cool proposal!

One important consideration I’d like to raise:

While `chainId: 0` for universal signatures simplifies UX, things may get tricky with **Smart Contract Accounts (SCAs)** or **custom wallet logic**.

For example:

- Contract code may differ across chains (even if the interface is similar).
- A signature that passes isValidSignature() on one chain might fail or behave differently on another.
- If contract state (e.g. owner, nonce, or permissions) has diverged across chains, security assumptions break down.

So I’m wondering:

How do we mitigate risks where **same signature = valid on one chain but unsafe on another**?

Would love to hear thoughts on whether:

- A checksum of the deployed bytecode should be embedded in the domain separator?
- We need chain-specific overrides for contracts with isChainAware() logic?

Really appreciate the simplicity this introduces for users, AA kits, Devs.

---

**ernestognw** (2025-06-06):

Hey [@codebyMoh](/u/codebymoh)! Thanks for the the thoughtful feedback!

**On scope**: You’re absolutely right about the complexity with SCAs. This ERC intentionally focuses on being a **simple building block** rather than solving cross-chain authentication holistically. The `chainId: 0` pattern gives us universal signature validity, but the verification semantics are left to the implementation layer.

**On your specific concerns**:

- Code differences: This feels like wallet/dapp responsibility to me. Wallets should warn users when signing for contracts with different bytecode across chains, and dapps should validate contract compatibility before accepting signatures. The standard can’t enforce this on already-deployed implementations, but we should definitely call it out in Security Considerations.
- State divergence: Similar reasoning - this is where higher-level coordination mechanisms come into play. Things like keystore rollups or dedicated state sync protocols could address this, but probably warrant their own ERCs.

**On “unsafe” signatures**: I’d love to hear your definition here. In my view, a signature is “unsafe” when it authorizes unintended actions. But with proper wallet UX (showing exactly what’s being signed on each chain) and dapp validation (checking contract compatibility), the risk becomes manageable.

**On your solutions**: The bytecode checksum idea is elegant! But I lean toward leaving these patterns to implementations rather than standardizing them here. Different use cases might want different safety mechanisms - some might prefer your checksum approach, others might want state synchronization, etc.

Hope this framing makes sense! Curious to hear your thoughts

---

**codebyMoh** (2025-06-07):

[@ernestognw](/u/ernestognw) Your framing makes a lot of sense — especially treating this as a foundational primitive rather than a full authentication framework. I agree that universal signature validity is a powerful enabler, and implementation-level flexibility is key.

**On “unsafe” signatures**:

Yes, totally agree with your definition — signatures are “unsafe” when they authorize unintended actions. I think the risk amplifies in scenarios where contracts diverge in state or logic but remain address-aligned across chains. So UX + validation are *critical* — maybe the standard could recommend (non-mandate) checksum practices or at least link to best practices in Security Considerations?

**On state divergence**:

Right, it’s out of this ERC’s scope, but might be worth noting that coordination layers (e.g., keystore rollups, state pinning, chain-specific guards) become almost essential in high-stakes use cases like governance or treasury control.

**On modular safety**:

Totally fair to defer specific safety patterns to use case–specific implementations. Maybe we could treat the `chainId: 0` concept as an interface layer and publish optional “safety modules” alongside it — like a checksum utility, signer attestations, or bytecode validation hooks?

All in all, loving the direction — this could become a key building block for cross-chain AA architecture. Happy to brainstorm or co-contribute to supporting standards or tooling around it if useful.

---

**ernestognw** (2025-06-07):

Thanks for the feedback, [@codebyMoh](/u/codebymoh)!

> maybe the standard could recommend (non-mandate) checksum practices or at least link to best practices in Security Considerations?

I’m hesitant to recommend unproven patterns, and I’m not sure if I would recommend this approach. I think it’s preferable to see real-world usage to inform safety practices rather than speculating upfront.

> but might be worth noting that coordination layers (e.g., keystore rollups, state pinning, chain-specific guards) become almost essential in high-stakes use cases like governance or treasury control.

Absolutely agree these become essential for high-stakes use cases. However, I see this as a natural architectural consequence rather than something this ERC should prescribe. Imo, different use cases will have vastly different coordination requirements.

> publish optional “safety modules” alongside it — like a checksum utility, signer attestations, or bytecode validation hooks?

While I appreciate the modular thinking, I’m concerned about scope creep. The strength of chainId: 0 is its simplicity. I’d rather see future ERCs build specialized safety frameworks on this foundation if demand emerges. Also happy to provide feedback if such standards appear

---

**ernestognw** (2025-09-03):

[@frangio](/u/frangio) pointed out (accurately) that all domains fields are optional. Citing from EIP-712

> Protocol designers only need to include the fields that make sense for their signing domain.

So it may be clever to rework this ERC as just omitting the chainId field.

---

**ernestognw** (2025-12-01):

Hey everyone! Thanks for the feedback so far, especially [@frangio](/u/frangio)’s point about omitting `chainId` instead of using `0`. I’ve substantially reworked ERC-7964 based on this and other considerations.



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/1386)














####


      `master` ← `ernestognw:chore/erc7964-standard712`




          opened 09:11PM - 01 Dec 25 UTC



          [![](https://avatars.githubusercontent.com/u/33379285?v=4)
            ernestognw](https://github.com/ernestognw)



          [+418
            -249](https://github.com/ethereum/ERCs/pull/1386/files)







This PR simplifies ERC-7964 by removing dependencies on draft standards and usin[…](https://github.com/ethereum/ERCs/pull/1386)g only standard EIP-712 encoding, making it immediately adoptable by existing wallets.

## Key Changes

1. **Removed ERC-7803 dependency** - No longer requires draft standard support
2. **Omit `chainId` instead of using `0`** - Cleaner semantics, fully EIP-712 compliant
3. **Array-based encoding** - Cross-chain operations as standard EIP-712 arrays instead of Merkle trees
   - Provides full transparency in wallet UIs
   - For 2-5 chains (typical case), Merkle trees save only 32-64 bytes
   - No custom wallet logic required
4. **Introduced `EIP712ChainDomain` pattern** - Nested domain struct for proper chain/contract binding
   - Flexible: supports both same-address and different-address deployments
   - Follows EIP-712's recursive encoding

## Benefits

- Works with any EIP-712 wallet immediately
- Full operation transparency for users
- Minimal overhead (32-64 bytes vs Merkle trees)
- Handles real-world deployment scenarios

All examples updated to demonstrate both deterministic (same address) and non-deterministic (different addresses) contract deployments.












### Key Changes

**1. Omit `chainId` instead of using `0`**

Following [@frangio](/u/frangio)’s suggestion, the ERC now simply omits `chainId` from the root `EIP712Domain` since all fields are optional per EIP-712. Much cleaner semantics!

**2. Dropped ERC-7803 dependency**

The proposal now uses only standard EIP-712 encoding - no draft standards required. This means existing wallets can support it immediately without implementing custom logic.

**3. Array-based encoding over Merkle trees**

Cross-chain operations are encoded as standard EIP-712 arrays. While [proposals like EIL](https://ethresear.ch/t/eil-trust-minimized-cross-l2-interop/23437) use Merkle trees, I’ve opted for arrays because:

- For 2-5 chains (typical case), Merkle trees save only 32-64 bytes
- Arrays provide full transparency in standard wallet UIs - users see all operations
- Merkle trees require custom wallet logic to verify leaves aren’t malicious

**4. Introduced `EIP712ChainDomain` pattern**

Each chain-specific operation includes a nested domain with `chainId` and optionally `verifyingContract`. This handles both:

- Same address deployments (CREATE2) → root domain has verifyingContract
- Different address deployments → nested domains have verifyingContract

### Updated Examples

All four reference implementations now demonstrate both deployment patterns and include reference on-chain verification code.

Would love feedback on this simplified approach! Does the array encoding trade-off (transparency vs. minimal extra overhead) make sense for the typical 2-5 chain use case?

---

**fmc** (2026-01-28):

great proposal

here’s something we developed couple of years ago, which may be helpful



      [github.com/erc7579/smartsessions](https://github.com/erc7579/smartsessions/blob/f5aaf867f7e22f3b9d746ce6f404f3a56833757f/contracts/lib/HashLib.sol#L84-L139)





####

  [f5aaf867f](https://github.com/erc7579/smartsessions/blob/f5aaf867f7e22f3b9d746ce6f404f3a56833757f/contracts/lib/HashLib.sol#L84-L139)



```sol


1. // keccak256(abi.encode(_MULTICHAIN_DOMAIN_TYPEHASH, keccak256("SmartSession"), keccak256("1")));
2. bytes32 constant _MULTICHAIN_DOMAIN_SEPARATOR = 0x057501e891776d1482927e5f094ae44049a4d893ba2d7b334dd7db8d38d3a0e1;
3.
4. library HashLib {
5. error ChainIdMismatch(uint64 providedChainId);
6. error HashMismatch(bytes32 providedHash, bytes32 computedHash);
7.
8. using EfficientHashLib for bytes32;
9. using HashLib for *;
10. using EfficientHashLib for *;
11.
12. /**
13. * Mimics SignTypedData() behavior
14. * 1. hashStruct(Session)
15. * 2. hashStruct(ChainSession)
16. * 3. abi.encodePacked hashStruct's for 2) together
17. * 4. Hash it together with MULTI_CHAIN_SESSION_TYPEHASH
18. * as it was MultiChainSession struct
19. * 5. Add multichain domain separator
20. * This method doest same, just w/o 1. as it is already provided to us as a digest


```

  This file has been truncated. [show original](https://github.com/erc7579/smartsessions/blob/f5aaf867f7e22f3b9d746ce6f404f3a56833757f/contracts/lib/HashLib.sol#L84-L139)












      [github.com/erc7579/smartsessions](https://github.com/erc7579/smartsessions/blob/f5aaf867f7e22f3b9d746ce6f404f3a56833757f/contracts/DataTypes.sol#L66-L73)





####

  [f5aaf867f](https://github.com/erc7579/smartsessions/blob/f5aaf867f7e22f3b9d746ce6f404f3a56833757f/contracts/DataTypes.sol#L66-L73)



```sol


1. struct MultiChainSession {
2. ChainSession[] sessionsAndChainIds;
3. }
4.
5. struct ChainSession {
6. uint64 chainId;
7. Session session;
8. }


```

