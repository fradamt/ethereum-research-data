---
source: magicians
topic_id: 21989
title: "ERC-7837: Diffusive Tokens"
author: jamesavechives
date: "2024-12-07"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-7837-diffusive-tokens/21989
views: 157
likes: 0
posts_count: 7
---

# ERC-7837: Diffusive Tokens

I would like to present a draft EIP introducing **Diffusive Tokens**, a new variant of fungible tokens. In this model, every transfer mints new tokens directly to the recipient without reducing the sender’s balance. The approach includes:

- Per-Token Native Fee: Each token transferred incurs a fee in the native currency (e.g., ETH), discouraging frivolous minting.
- Capped Max Supply: While transfers increase total supply, the total is capped to maintain a form of scarcity.
- Burn Mechanism: Token holders can burn their tokens, reducing total supply and potentially enabling real-world redemption processes.

This design differs from traditional ERC-20 tokens and may find use cases in real-world asset tokenization, controlled distribution, or unique economic experiments.

I invite feedback, questions, and discussions on the viability, security, and potential applications of Diffusive Tokens. Your insights will help refine the standard and guide its evolution.

[github pull request for Diff Tokens](https://github.com/ethereum/ERCs/pull/1030)

## Replies

**0xTraub** (2024-12-09):

This just seems like a token contract with an unlimited and permissionless mint functionality. This seems extremely insecure. Why do we need this?

Without a check on existing balance what’s to stop someone from backrunning a contract deployment and then just calling `transfer(SOME_ADDRESS, maxSupply)` and then preventing the contract from being used by anyone else ever since any new transfers would have supply exceed the max?

`- **Real-World Asset Backing**: A manufacturer can issue DIFF tokens representing a batch of products (e.g., iPhones). Each token can be redeemed (burned) for one physical item.`

I understand how the transfer tax is supposed to prevent inflation by making it economically inefficient but if tokens are fungible at a certain point value from a redemption becomes worth more than whatever the value of the transfer tax is, especially if the fee is static and there’s basically an exponential increase in a users’ balance every time they pay it, and since tokens are fungible how does a redeemer prevent what’s basically a sybil attack?

---

**radek** (2024-12-17):

[@jamesavechives](/u/jamesavechives) Thx for the interesting topic. Can you elaborate more on the use cases?

Also besides the issues mentioned by 0xTraub, IMO the administrative functions do not belong to the standard as they are not key for interoperability. The same wrt data structures - they can be implemented differently.

What is rather missing is the `maxSupply()` function in the interface as it is crucially impacting the ability to execute.

What is the point of having `transfer()` when no transfer is made at all? Is it only called in order to be close to ERC20 std.? IMHO such naming is misleading.

---

**jamesavechives** (2025-02-09):

You’re correct that if the real-world redemption value of each token far exceeds the cost to mint it (the fee), it creates an *arbitrage* problem. However:

1. Fee-Setting Is Crucial
The contract owner must set the per-token fee to reflect the asset’s current or anticipated value. If each token claims 1 iPhone worth $1,000, the fee cannot remain $5—or you’d have a clear exploit! One must price the fee in a way that prevents an economic giveaway. Some issuers might use dynamic or tiered fees, or even pause/upgrade the contract if real-world conditions change drastically.
2. Max Supply as a Failsafe
Even if the fee is temporarily mispriced, maxSupply prevents endless inflation. The total supply can’t exceed that upper bound, so there’s only so much “arbitrage” possible.
3. Off-Chain Redemption Checks
In many real-world asset use cases, redemption won’t be purely “show me a token, I ship you an iPhone” in an automated sense. A manufacturer may still limit redemptions by identity, location, or quantity. If someone tries a Sybil attack, the manufacturer can require more rigorous KYC before delivering.
4. Specialized Use Cases, Not a Universal Fit
DIFF tokens aren’t intended for every scenario. They’re a niche standard for token distributions that expand supply on transfer while collecting a pay-as-you-mint fee. Where real-world redemption is involved, either the fee must be set high enough or additional “off-chain” redemption controls must be in place to prevent unlimited or Sybil-based redemptions.

---

**jamesavechives** (2025-02-09):

#### 1. Use Cases and Motivation

**a) On-Demand Distribution / Pay-to-Mint**

- Traditional ERC-20 tokens are typically minted at deployment or by the owner using a standard “mint” function. By contrast, DIFF tokens let anyone effectively “mint” tokens as they transfer them to a target address, provided they pay the fee.
- This can be useful in scenarios where the issuer wants a more “automatic,” open-ended distribution method. For instance, a project launching a collectible or merchandise token can say: “Anyone can acquire these tokens if they’re willing to pay the fee, up to the supply cap.”

**b) Ties to Real-World Goods**

- One of the proposed use-cases is redeeming tokens for physical items (e.g., iPhones). If each DIFF token is redeemable for an item, the token effectively represents a “claim” on it. The transfer fee (plus the max supply) can be set so that it aligns with the item’s real cost or scarcity.
- If the fee is properly priced, each minted token covers manufacturing or overhead costs. The sender pays the contract’s owner for each token minted, so it’s akin to “purchasing” newly created claims.

**c) Built-In Scarcity (Max Supply)**

- Because there’s a maxSupply, supply cannot expand infinitely. The contract reverts once it hits that cap. In many real-world goods scenarios, that aligns with a fixed production run (e.g., 10,000 product units).

In short, DIFF tokens aren’t intended to replace standard ERC-20s. They’re specialized for contexts where “minting” is open but subject to an economic cost (a fee) plus a known maximum quantity.

---

#### 2. Admin Functions

You are correct that admin functions (like `setTransferFee` or `withdrawFees`) are not strictly *required* for interoperability. Wallets and dApps that only need to *transfer* the token or *query* balances do not rely on them. These functions can be seen as part of an *extension* or an *administrative layer* that’s optional.

We included them in the reference specification to illustrate how a typical issuer might manage fees, supply, and revenue flows. In practice, they could be omitted, replaced with immutable settings, or put into a separate contract module.

---

#### 3. Including maxSupply() in the Interface

You make a good point about exposing a `maxSupply()` function in the interface. Because hitting the `maxSupply` is a key part of this token’s logic (transfers will revert if they exceed it), dApps and end-users benefit from being able to query it directly.

A minimal DIFF interface could be:

solidity

CopyEdit

```auto
interface IDiffusiveToken {
    function maxSupply() external view returns (uint256);
    function totalSupply() external view returns (uint256);
    function balanceOf(address account) external view returns (uint256);
    function transfer(address to, uint256 amount) external payable returns (bool);
    function burn(uint256 amount) external;
    // ... plus optional approve/allowance/transferFrom if needed
}
```

This ensures any integrator can *programmatically* check how close the token is to the cap before initiating a minting transfer.

---

#### 4. Why Is It Called transfer() If the Sender’s Balance Doesn’t Decrease?

Yes, the behavior is *semantically different* from a typical ERC-20 transfer. We kept the name `transfer()` for a few reasons:

1. Ecosystem Compatibility
Many wallets, block explorers, and DeFi integrations rely on “ERC-20 style” function signatures—particularly transfer, transferFrom, and approve. Renaming them (e.g., to “diffuse()” or “mintTo()”) would require custom integration or cause breakage in standard interfaces.
2. Log Compatibility
Tools typically listen for the Transfer(address indexed from, address indexed to, uint256 value) event to track token movements. Aligning with that event signature means existing dashboards, portfolio trackers, etc., can at least pick up the tokens, even if the economics are unusual.

We do realize it’s somewhat misleading from a purely logical standpoint, since the *sender’s balance never decreases*. But from an ERC-20 interface perspective, that’s how we achieve the broadest synergy with existing tools. DIFF tokens intentionally deviate from the normal “balance reallocation” model in favor of “mint on transfer.”

If a project wants to highlight that difference, they could create separate user-facing function names (like `diffuseTokens`) that internally call the same logic. The official standard function would remain `transfer()` for third-party wallet compatibility.

---

**radek** (2025-03-05):

[@jamesavechives](/u/jamesavechives) Thx for the use cases and further explanation.

I am still not sure the adoption shortcut of “misusing” `transfer()` function is a long term correct approach to be codified within the standard.

I would like to invite you to the regular dev/auditors meetup (can be via remote talk) to discuss the concept / use cases / implementation. It runs every last Tuesday - [BeerFi Prague - Web3 on-chain dev Meetup Group | Meetup](https://www.meetup.com/web3-on-chain-dev-meetup-group/) - we often review the standards there.

A suggestion - to rename `maxSupply()` to something more namespaced / concrete like `diffusiveSupplyCap()` to avoid name / selector clashes when combining several standards and additional custom logic. IMHO `maxSupply` is too generic term.

---

**jamesavechives** (2025-03-06):

[@radek](/u/radek) Thank you for the kind invite and for your continued feedback on the concept. I’d be happy to attend the BeerFi Prague meetup (even remotely) to discuss this further.

Regarding your point about using the `transfer()` function in this manner: I agree it’s an unorthodox approach, and I appreciate the concern about “misuse.” The motivation, as mentioned, is purely for tooling compatibility—many wallets and DeFi platforms rely heavily on the `transfer()`, `transferFrom()`, and `Transfer` event signatures. That said, I acknowledge the potential confusion for auditors, integrators, and developers who expect the traditional ERC-20 semantics. This will definitely be one of the key points to hash out in broader discussions.

On naming `maxSupply()` vs. `diffusiveSupplyCap()`: that’s an excellent suggestion. The function name is, indeed, quite generic. Namespacing it more explicitly can help avoid clashes with other contracts or potential multi-standard implementations. We’ll likely adopt such a more descriptive naming convention (`diffusiveSupplyCap()` or similar) in the final version.

Looking forward to further collaboration and more in-depth conversation at the meetup!

