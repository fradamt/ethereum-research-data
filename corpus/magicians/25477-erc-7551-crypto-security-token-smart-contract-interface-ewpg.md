---
source: magicians
topic_id: 25477
title: "ERC-7551: Crypto Security Token Smart Contract Interface (eWpG) – reworked"
author: MarkusKluge
date: "2025-09-16"
category: ERCs
tags: [erc, security, security-token]
url: https://ethereum-magicians.org/t/erc-7551-crypto-security-token-smart-contract-interface-ewpg-reworked/25477
views: 249
likes: 11
posts_count: 11
---

# ERC-7551: Crypto Security Token Smart Contract Interface (eWpG) – reworked

This proposal supersedes the earlier Magicians discussion:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/hagen/48/9104_2.png)

      [ERC-7551: Crypto Security Token Smart Contract Interface ("eWpG")](https://ethereum-magicians.org/t/erc-7551-crypto-security-token-smart-contract-interface-ewpg/16416) [ERCs](/c/ercs/57)




> Abstract
> The compliant representation of securities on a distributed ledger network (“crypto securities”) remains one the most prominent use cases for distributed ledger systems. Up until recent developments such activities were not always fully recognized by local securities laws. This led to different views on what information and functionality they should provide. Germany, as one of the first countries in the world, has enhanced its legal framework to fully cover the issuance of securities in…

Dear community,

We would like to share an update on ERC-7551 (“eWpG”). Over the past months, we have revised the standard. From discussions during implementations and especially in the context of exchange integrations, it has become clear that interoperability with other standards is essential.

This standard and its update is the result of the standardization working group of the German Federal Association of Crypto Registrars. It’s based on the smart contract implementations of its members. It contains terminology and abstract ideas also published in ERC-1400 and ERC-3643. We would like to thank the initiators of these standards for their work. Both proposals were considered as alternatives to drafting this standard, but we decided to propose an alternative standard instead of using them directly.

In the ongoing debate, ERC-3643 has often been referenced. We take the criticism from its authors seriously and would like to emphasize that ERC-7551 deliberately follows a more open approach. While ERC-3643 strongly relies on OnchainID, our design aims to allow greater flexibility in how compliance mechanisms can be implemented.

The reasons include:

- Mandatory identity layer (onchainID): ERC-3643 tightly couples transfer compliance with a specific decentralized identity framework. This limits flexibility and imposes implementation constraints not aligned with the regulatory environment in certain jurisdictions, such as Germany.
- Access control model: ERC-3643 introduces constraints through the Agent role, which reduces flexibility for implementing alternative RBAC systems.
- Completeness: Some of the features of ERC-1400 and ERC-3643 address very specific use cases that are not common to all association members. To support compatibility, we deliberately kept the same function names as ERC-3643 whenever possible. In contrast, ERC-7551 aims to define a minimal and flexible foundational interface that can be combined with the underlying token standard (e.g. ERC-20 or ERC-1155), operator permission management, and compliance modules.

### Our approach

- Interoperability: The core objective is to ensure that ERC-7551-based deployments can work seamlessly with eWpG requirements without being rejected by exchanges that already rely on ERC-3643 or implementations like CMTAT and may not wish to deal with technical discrepancies.
- Modularity: Functions such as mint, freezePartialTokens, forcedTransfer, or canTransfer can be integrated and combined flexibly.
- Openness to integration: ERC-7551 does not prescribe a specific rule engine. Instead, it is designed to be open for modular solutions—including rule engines or identity frameworks—that can reflect specific use cases or enable smooth integration with existing compliance systems and their rules.
- Nature of the changes: The recent revisions mainly consist of adaptations to method and function names in order to improve clarity and alignment with other standards. A detailed overview of these changes can be found in the updated repository: Add ERC: Crypto Security Token Interface by tokenforge · Pull Request #1211 · ethereum/ERCs · GitHub.

### Why this matters

- More choice for implementers: Institutions and projects are not locked into a single identity infrastructure but can tailor compliance to their specific needs.
- Practical alignment with the market and the community: By aligning with established standards such as ERC-3643 and widely used implementations like CMTAT, we increase the likelihood that ERC-7551-based tokens will be accepted by exchanges.
- Bridging law and technology: Combining eWpG requirements with a modular concept creates a robust standard that addresses both regulatory and practical needs.

## Replies

**mihaic195** (2025-09-19):

Hey [@MarkusKluge](/u/markuskluge),

Have you had a look at [ERC-7943: Universal RWA Interface (uRWA)](https://ethereum-magicians.org/t/erc-7943-universal-rwa-interface-urwa/23972)? It aimed to solve all your points regarding interoperability, identities, extension, access control, and modularity. Quite a few companies are already backing it.

I’m curious to see what you think.

---

**xaler** (2025-09-22):

[@mihaic195](/u/mihaic195) I agree with this.

[@MarkusKluge](/u/markuskluge) we have been trying to onboard as many companies as possible into defining an universal interface through 7943, would love to see our efforts combined in order to bring something that can serve and be useful to everyone.

Do you see anything that 7943 doesn’t cover ?

---

**MarkusKluge** (2025-09-22):

Hey [@mihaic195](/u/mihaic195), [@xaler](/u/xaler)

Thanks a lot for your comments ![:pray:](https://ethereum-magicians.org/images/emoji/twitter/pray.png?v=12)

I see **ERC-7551** and **ERC-7943** as pursuing different but complementary goals: 7551 focuses on mapping the German *eWpG* into concrete smart contract functions, while 7943 provides a minimalist, universal baseline for RWAs. Personally I support the idea behind **ERC-7943**, but in my role for the association I currently need to ensure that the legal requirements of the *eWpG* are reflected in a standard.

We’ll run a gap analysis between **ERC-7551** and **ERC-7943** to identify overlaps and explore additional ways to improve interoperability. And I’d also like to highlight my respect for the work on **ERC-3643**, **ERC-1400**, and **ERC-7943** — each contributes an important perspective, and the ecosystem benefits from combining these strengths.  Our work should build on this collective progress.

---

**xaler** (2025-09-22):

That’s great to know.

I wonder whether 7943 can serve as interface layer for 7551 even if 7551 expand on it. Would be great to unify interoperability across several compliance frameworks all using the same interface.

Let me know if I can help with anything about it, definetely keen to make it happen!

---

**MarkusKluge** (2025-09-23):

We really appreciate the work on a minimal and universal compliance layer for RWAs. With ERC-7551 our focus is a bit different: we capture explicit legal requirements under the German eWpG, which is why we standardize features like pause/unpause tied to a non-zero termsHash, machine-readable metaData, standardized mint/burn, and a clear split between active and frozen balances. These elements are essential for security tokens to be usable in regulated markets and for exchanges and custodians to safely integrate them.

From our first analysis, it seems possible to build an adapter layer that exposes the 7943 interface while delegating to a 7551 token and emitting the required 7943 events in the right order. This would keep all 7551 MUSTs intact, while still giving integrators that expect 7943 a compatible surface.

This is just an initial exploration – we’d be happy to discuss and challenge this idea together, as we think both standards address important but different layers of the RWA / securities stack.

| Area | ERC-7551 requirement | ERC-7943 requirement | Adapter feasibility |
| --- | --- | --- | --- |
| Pause / Terms | unpause() gated by non-zero termsHash | not defined | adapter implements paused state paused() → isTransferAllowed=false |
| Compliance views | canTransfer, canTransferFrom | isTransferAllowed, isUserAllowed must not revert | map 1:1, never revert |
| Frozen balances | freezePartialTokens / unfreezePartialTokens + getActiveBalanceOf / getFrozenTokens | single setFrozen / getFrozen | adapter has to compute delta + emits 7943 Frozen |
| Forced transfers | forcedTransfer + Transfer (+ optional TokensUnfrozen) | forceTransfer + ForcedTransfer (+ unfreeze event before transfer) | adapter adds required events / order |
| Public transfers | MUST revert if non-compliant | MUST revert if isTransferAllowed=false | ensured by 7551 core |
| Mint | MUST emit Mint + Transfer | MUST NOT mint to disallowed accounts | if enforced in the 7551 implementation (e.g. separate permission contract like in CMTAT) |
| Burn | MUST emit Burn + Transfer | Allowed regardless of compliance | handled by 7551 core |
| ERC-165 | not defined | MUST support 7943 interface ID | adapter signals support |

What do you guys think? [@xaler](/u/xaler) [@mihaic195](/u/mihaic195)

---

**mihaic195** (2025-09-23):

Hey [@MarkusKluge](/u/markuskluge), Thanks for the analysis. I have some remarks:

**1. Pause/Terms:**

Pausing/unpausing and document handling were intentionally left out of ERC7943 because their implementation is highly dependent on the jurisdiction and use case, precisely as your example highlights. Therefore, it would be a good candidate to introduce this as an extension to ERC7943. However, I think you can still achieve pausing behaviour by adapting the `canTransfer`.

**2. Compliance/Views:**

ERC7943 defines this through non-reverting `canTransfer` and `isUserAllowed`, which seems to cover what you want to achieve. I don’t see a strong reason to duplicate this logic.

**3. Frozen balances:**

ERC7943 works in absolute values `setFrozenTokens` instead of calculating deltas. If you need to compute the delta, you can compare the old value through `getFrozenTokens` and the new frozen value when emitting events.

**4. Forced transfers:**

I’m seeing overlap here. In ERC7943, a forced transfer automatically requires frozen tokens to be unfrozen first, and the correct events are already in place. I don’t see a need for adaptation.

**5. Public transfers:**

There also seems to be an overlap here, as ERC7943 handles this through `isUserAllowed` and `canTransfer`, which map to your requirements.

**6. Mint / Burn:**

I don’t understand why `Mint` / `Burn` events would be necessary. In ERC20 semantics, a `Transfer` from the zero address already signals a mint, and a `Transfer` to the zero address signals a burn. That pattern is widely adopted and easy to recognize.

Overall, ERC7943 can handle most of the cases you mentioned, besides things like pausing and document management under eWpG. So, I think these things can be modeled as modular extensions on top of ERC7943. I’d be open to exploring options with you on this and curious to see what you think.

PS. Here is an examples repo you can take a look at: [GitHub - xaler5/uRWA](https://github.com/xaler5/uRWA)

---

**xaler** (2025-09-23):

I believe everything mentioned here is pretty much compatible with 7943 ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

What I’d suggest is something like

```auto
contract ERC7551Token is IERC7943 {
 ...
}
```

And anything that falls outside 7943 should be in there.

Little note is that 7943 recently underwent some changes and the repository mentioned by [@mihaic195](/u/mihaic195) is still behind those changes. I’d suggest to revisit the analysis using the latest state of 7943: [ERC-7943: uRWA - Universal Real World Asset Interface](https://eips.ethereum.org/EIPS/eip-7943)

- pausability is already expected as extension of 7943 as described in the EIP (mentioned in the extensibility section of 7943)
- delta changes in freezing amounts are also compatible with 7943 (mentioned in the security considerations of 7943)
- mint/burn are also not a problem

Another important thing is that 7943 has a “notes no maning” section that justify why those names have been used, expecially to be backward compatible with things like 3643 or 1400

---

**xaler** (2025-09-26):

I did a quick analysis.

Based on [latest](https://github.com/ethereum/ERCs/blob/master/ERCS/erc-7943.md#specification) state of 7943 and using as a reference only the ERC-20 (fungible) interface of it `IERC7943Fungible`, your ERC7551 can indeed be defined as:

```auto
interface IERC7551 is IERC7943Fungible {
    // Additional events for ERC-7551
    event Mint(address indexed minter, address indexed account, uint256 value, bytes data);
    event Burn(address indexed burner, address indexed account, uint256 value, bytes data);
    event Enforcement(address indexed enforcer, address indexed account, uint256 amount, bytes data);
    event Terms(bytes32 hash, string uri);
    event MetaData(string newMetaData);

    // Extended frozen token management with data parameter
    function freezePartialTokens(address account, uint256 amount, bytes calldata data) external;
    function unfreezePartialTokens(address account, uint256 amount, bytes calldata data) external;

    // Additional view functions
    function getActiveBalanceOf(address tokenHolder) external view returns (uint256);
    function paused() external view returns (bool);
    function termsHash() external view returns (bytes32);
    function metaData() external view returns (string memory);
    function canTransferFrom(address spender, address from, address to, uint256 value) external view returns (bool);

    // Supply management
    function mint(address to, uint256 amount, bytes calldata data) external;
    function burn(address tokenHolder, uint256 amount, bytes calldata data) external;

    // Enhanced forced transfer with data
    function forcedTransfer(address account, address to, uint256 value, bytes calldata data) external returns (bool);

    // Pause functionality
    function pause() external;
    function unpause() external;

    // Document and metadata management
    function setTerms(bytes32 _hash, string calldata _uri) external;
    function setMetaData(string calldata _metadata) external;
}
```

With the following considerations.

1. The ERC-7943 functions would need to be implemented as wrappers:

```auto
// ERC-7943 setFrozenTokens wraps ERC-7551 functionality
function setFrozenTokens(address user, uint256 amount) external override {
    uint256 currentFrozen = getFrozenTokens(user);
    if (amount > currentFrozen) {
        freezePartialTokens(user, amount - currentFrozen, "");
    } else if (amount < currentFrozen) {
        unfreezePartialTokens(user, currentFrozen - amount, "");
    }
}

// ERC-7943 forcedTransfer wraps ERC-7551 functionality
function forcedTransfer(address from, address to, uint256 amount) external override {
    return forcedTransfer(from, to, amount, "");
}
```

1. ERC-7551’s canTransfer would need to incorporate pause state:

```auto
function canTransfer(address from, address to, uint256 amount) external view override returns (bool) {
    if (paused()) return false;
    // ... rest of ERC-7943 compliance logic
    return super.canTransfer(from, to, amount);
}
```

With such approach you would still achieve all purposes of 7551, mantain backward compatibility with 3643, 1400 but also adhere to the universal interface proposed by 7943 for interoperability.

If you agree with these you can even make 7551 to require 7943 in the header definition.

Wdyt ?

---

**MarkusKluge** (2025-09-27):

Hi Guys, thanks a lot for the thoughtful input. We really value the direction of 7943 and I can imagine 7551 becoming a “profile/plugin” of it in the future.

For now, since 7943 is still a draft and may evolve, We’d prefer to keep 7551 scoped as a stable eWpG-focused standard and achieve interoperability via a thin adapter that implements IERC7943Fungible on top of a 7551 token. That way integrators already get the 7943 surface, while 7551 remains stable.

Once 7943 has finalized its interface and semantics, we’d be happy to revisit making 7551 an explicit 7943 profile. In the meantime, we’re also open to collaborate on a reference adapter and conformance tests so that both paths align smoothly. What do you think?

---

**xaler** (2025-09-29):

Thanks for the quick answer !

7943 is in review stage, approaching finalization indeed. It already received a lot of feedback which has been consistently incorporated. It brings semantics and nomenclatures similar to 3643 but it adds generalization which seems applicable already to 7551.

My suggestion is to keep 7551 consistent with it to avoid bigger refactors in the future. I don’t expect 7943 to change drastically.

Having said that, looking forward to what 7551 will become !

