---
source: magicians
topic_id: 27407
title: "ERC-8129: Non-Transferable Token"
author: Vantana1995
date: "2026-01-09"
category: ERCs
tags: [erc, nft, erc-721]
url: https://ethereum-magicians.org/t/erc-8129-non-transferable-token/27407
views: 264
likes: 13
posts_count: 12
---

# ERC-8129: Non-Transferable Token

I’ve been thinking about current Soulbound token implementations and their reliance on ERC-721 as a base. Most existing solutions (like ERC-5192) essentially bolt locking mechanisms onto ERC-721, reverting transfers with custom errors. While this works, it feels architecturally wrong.

The core issue: **Soulbound tokens aren’t non-fungible - they’re non-transferable**. ERC-721 is built around the concept of transferability. The entire interface revolves around `transferFrom`, `safeTransferFrom`, `approve`, `setApprovalForAll` - functions that fundamentally contradict what Soulbound means.

When we inherit from ERC-721 and override these functions to revert, we’re carrying dead weight:

- Storage slots for approvals and operators that will never be used
- Larger deployment bytecode
- Higher gas costs on mint/burn due to unnecessary state management
- Increased Ethereum state growth from unused mappings

Here’s a minimal implementation that covers everything Soulbound needs:

```solidity
interface IERC8129 {
    event Mint(address to, uint256 id);
    event Burn(address from, uint256 id);

    function mint() external returns(uint256);
    function burn(uint256) external;
}

interface IERC721Metadata {
    function name() external view returns (string memory);
    function symbol() external view returns (string memory);
    function tokenURI(uint256 tokenId) external view returns (string memory);
}

contract ERC8129 is IERC8129, IERC721Metadata {
    uint256 private tokenId;
    string private _name;
    string private _symbol;
    string private _baseURI;

    mapping(uint256 => address) public ownerOf;

    error ErrNotAnOwner();
    error ErrNotMinted();

    constructor(string memory name_, string memory symbol_, string memory baseURI_) {
        _name = name_;
        _symbol = symbol_;
        _baseURI = baseURI_;
    }

    function name() external view override returns (string memory) {
        return _name;
    }

    function symbol() external view override returns (string memory) {
        return _symbol;
    }

    function tokenURI(uint256 _tokenId) external view override returns (string memory) {
        if (ownerOf[_tokenId] == address(0)) revert ErrNotMinted();
        return _baseURI;
    }

    function mint() external virtual returns (uint256 id) {
        tokenId += 1;
        id = tokenId;
        ownerOf[id] = msg.sender;
        emit Mint(msg.sender, id);
    }

    function burn(uint256 id) external virtual {
        if (ownerOf[id] != msg.sender) revert ErrNotAnOwner();
        ownerOf[id] = address(0);
        emit Burn(msg.sender, id);
    }
}
```

This drastically reduces codesize, which opens up space for storing additional data directly in the contract - like on-chain SVG metadata.

The semantic argument matters too. When you see ERC-721, you expect transferability. Soulbound tokens represent credentials, achievements, identity - things that by definition shouldn’t move between addresses. Using a transferable token standard and disabling transfers creates conceptual confusion.

Current ERC-721-based SBT implementations aren’t truly “bound to soul” - they’re transferable tokens with transfer restrictions. That’s a workaround, not a solution.

A dedicated standard would:

- Remove unused storage (approvals, operators)
- Reduce deployment bytecode significantly
- Lower gas costs for mint/revoke operations
- Decrease state growth compared to ERC-721-based implementations
- Provide clear semantics: mint once, own forever, or burn

The counterargument is ecosystem compatibility - wallets and marketplaces already understand ERC-721. But Soulbound tokens don’t need marketplace support. They’re not meant to be traded. Wallet support just needs `ownerOf` and metadata URI, which any minimal standard can provide.

Curious what others think - is the convenience of ERC-721 inheritance worth the architectural and efficiency tradeoffs?

## Replies

**abcoathup** (2026-01-12):

Adoption (by wallets & explorers) of a new standard would likely take years, even if there was a compelling application. (based on my experience with ERC721).

That doesn’t mean you shouldn’t do it, but it would be a long road.

---

**Vantana1995** (2026-01-12):

I understand that this may take a long time, but I am more interested in the implementation of the idea and the community’s response. If the community responds, then it is worth it; if the community does not care, then there is probably no point in pushing this idea

---

**Vantana1995** (2026-01-19):

[github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/11105)














####


      `master` ← `Vantana1995:eip-nontransferable-tokens`




          opened 12:19PM - 19 Jan 26 UTC



          [![](https://avatars.githubusercontent.com/u/138480754?v=4)
            Vantana1995](https://github.com/Vantana1995)



          [+278
            -0](https://github.com/ethereum/EIPs/pull/11105/files)







**ATTENTION: ERC-RELATED PULL REQUESTS NOW OCCUR IN [ETHEREUM/ERCS](https://gith[…](https://github.com/ethereum/EIPs/pull/11105)ub.com/ethereum/ercs)**

--
## Summary

This PR proposes EIP-XXXX: Non-Transferable Token Standard - a minimal standard for tokens that are permanently bound to an address.

## Description

Introduces a dedicated interface for non-transferable (Soulbound) tokens that eliminates transfer functionality by design, rather than extending ERC-721 and blocking transfers. The standard:

- Defines tokens as non-transferable through interface design (no transfer functions)
- Reduces bytecode bloat by ~80% compared to ERC-721 extensions
- Provides semantic clarity - tokens that cannot be transferred vs tokens that block transfers
- Includes only essential operations: `mint()`, `burn()`, `ownerOf()`
- Requires ERC-721 Metadata interface for wallet/indexer compatibility

This approach addresses architectural mismatches in existing Soulbound implementations (ERC-5192, ERC-4973, ERC-5484) that inherit unused transfer infrastructure.












today open request, this is my first time, what should i do next?

---

**Vantana1995** (2026-01-21):

## Unsolicited Minting Risks

In ERC-8129, minting is issuer-initiated rather than user-initiated. This means recipients may receive non-transferable tokens with metadata they did not explicitly request.

This raises potential UX and safety concerns. Token metadata may include images or other rich media that wallets, indexers, or explorers automatically render. In such cases, users could be exposed to unwanted or inappropriate content before they have an opportunity to react (for example, by hiding or burning the token).

Given that this issue already exists for issuer-minted NFTs and credentials, but may be more visible for permanently bound tokens, I’d like to get feedback on how this should be handled in practice.

- Should ERC-8129 explicitly acknowledge unsolicited minting risks, or is this better handled entirely at the wallet and application layer?
- What expectations, if any, should exist for wallets and indexers when rendering metadata for non-transferable tokens?
- Are there existing patterns or best practices (especially from wallet or indexer implementations) for mitigating unwanted or harmful metadata exposure without expanding the core token interface?

The goal here is to understand where the responsibility boundary should lie between a minimal token standard and higher-layer UX and safety policies.

---

**AccessDenied403** (2026-01-22):

Hello,

Great proposal! I also think it makes sense to have a standard that doesn’t rely on ERC-721 to represent soulbound tokens, for the sake of clarity and efficiency.

Certainly, the standard won’t be supported by all wallets from the start, etc. But that’s not essential, and I think there will still be an incentive for companies to adopt this standard.

I am just wondering for the mint function if it would be better to revert if the token can not be minted instead of returning (true, false).

The standard behavior now is generally to revert if an action can not be done.

Also it is also particularly confusing if a transaction is accepted but do nothing

So I will change

`function mint() external virtual returns (uint256 id, bool)`

To

`function mint() external virtual returns (uint256 id)`

Additionally, we could also add a custom error for invalid mint in the interface

---

**Vantana1995** (2026-01-22):

Thank you for the feedback! You’re absolutely right about the `bool` return value.

My initial motivation for including it was related to potential `IERC8129Receiver` integration for smart contract wallets (see my previous message about consent-based minting). I thought returning `false` could signal rejection without reverting, allowing the caller to handle it gracefully.

However, I agree that reverting is the correct Solidity pattern here. It’s more gas-efficient and prevents silent failures. If we do add receiver support, it should revert when rejected, not return `false`.

I’ll update the specification to:

```solidity
function mint(address to) external returns (uint256 tokenId);
```

Thanks for catching this!

---

**docbot** (2026-01-23):

This is an interesting proposal, and I agree that carrying the dead weight of `approve` and `transferFrom` logic for Soulbound tokens feels inefficient.

However, my main concern with the reference implementation is the removal of the standard `Transfer` event. The entire ecosystem (Etherscan, The Graph, Dune, etc.) relies on listening for `Transfer(address from, address to, uint256 tokenId)` to index ownership changes.

By switching to custom `Mint` and `Burn` events, these tokens would effectively be invisible to existing infrastructure. Have you considered keeping the standard `Transfer` event (emitting `address(0)` for mints/burns) while still stripping out the transfer *functions*? That seems like a middle ground that preserves gas savings on deployment while maintaining indexer compatibility.

###

---

**Vantana1995** (2026-01-23):

Thanks for raising this concern about indexer compatibility.

You’re right that the existing ecosystem relies heavily on the `Transfer` event. However, I believe using custom `Mint` and `Burn` events is the correct choice here for several reasons:

1. Semantic accuracy: Transfer implies movement between addresses, which contradicts the core principle of non-transferability. Using Mint/Burn makes the token’s nature immediately clear.
2. Existing precedent: Other standards like ERC-1155 and ERC-4973 use their own events and are successfully indexed. Custom events don’t create indexing problems - they’re a standard practice for non-ERC-721 token standards.
3. Indexer capabilities:

Etherscan already tracks Mint and Burn events in transaction logs
4. The Graph is specifically designed for custom event indexing - projects write their own subgraphs to track ANY events they need, not just standardized ones
5. This is a UX-layer concern, not a protocol limitation
6. Future compatibility: As the ecosystem grows and potential extensions to this standard emerge, clearly separating Mint from Transfer becomes critical for distinguishing transferable from non-transferable tokens. This separation is essential for proper categorization and tooling support.
7. Interface clarity: Emitting Transfer events while not implementing transferFrom() would create confusion. Tools that detect the Transfer event might incorrectly assume ERC-721 compatibility.

Projects adopting ERC-8129 will need to build appropriate subgraphs and integrations, but that’s expected for any new standard.

---

**jaybuidl** (2026-01-29):

It looks interesting.

It seems difficult to query ownership of the token onchain unless the exact `tokenId` is known. I would find it useful to query ownership of the token regardless of the `tokenId`. Something similar to `erc20.balanceOf(address)`, maybe `ownedBy(address)` to follow the ERC8129 semantics.

---

**Vantana1995** (2026-01-30):

That’s a really good point that I hadn’t considered myself - it made me think more deeply about the design.

Since soulbound tokens typically represent unique credentials where an address should only own one instance (like a university diploma, concert ticket, or unique in-game item), perhaps it makes sense to change the `ownerOf` mapping to a `hasToken` mapping that stores a boolean value - either you own it or you don’t.

For multiple certificate types, I think each should be a separate contract rather than multiple tokens within one contract.

---

**Vantana1995** (2026-02-02):

I thought about it and I don’t think this is the best idea. Due to minimal interface implementation and gas/storage optimization, we should keep only `ownerOf(tokenId)` - the same approach used in any NFT standard.

Adding `balanceOf(address)` or `tokensOwnedBy(address)` would require additional storage mappings and increase deployment costs, which contradicts the core principle of minimalism.

If someone needs to query all tokens owned by an address, they can do it the same way they do with ERC-721 - by indexing `Mint`/`Burn` events off-chain. On-chain, `ownerOf(tokenId)` provides the source of truth when you know the `tokenId`.

The current design is sufficient and follows established patterns from existing NFT standards.

