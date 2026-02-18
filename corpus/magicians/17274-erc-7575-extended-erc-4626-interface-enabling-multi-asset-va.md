---
source: magicians
topic_id: 17274
title: "ERC-7575: Extended ERC-4626 Interface enabling Multi-Asset Vaults"
author: joeysantoro
date: "2023-12-12"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-7575-extended-erc-4626-interface-enabling-multi-asset-vaults/17274
views: 4182
likes: 27
posts_count: 31
---

# ERC-7575: Extended ERC-4626 Interface enabling Multi-Asset Vaults

See [Add ERC: Partial and Extended ERC-4626 Vaults by Joeysantoro · Pull Request #157 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/157) for the most up to date draft

## Abstract

The following standard adapts ERC-4626 to support multiple assets or entry points for the same share token.

It adds a new `share` method to allow the ERC-20 dependency to be externalized.

This also enables Vaults which don’t have a true share token but rather convert between two arbitrary external tokens.

Lastly, it enforces ERC-165 support for Vaults.

## Replies

**beringela** (2024-05-06):

Hi Joey,

Could you explain a bit more about this part:

```auto
### Multi-Asset Vaults
Multi-Asset Vaults share a single `share` token with multiple entry points denominated in different `asset` tokens. Multi-Asset Vaults MUST implement the `share` method on each entry point.
```

I’m not clear what is meant by an “entry point”. Does it mean a function on the vault contract? Or does it mean a separate contract altogether?

Also, do you know if there a reference implementation available?

Many thanks,

Kevin.

---

**jeroen** (2024-05-06):

[@beringela](/u/beringela)

> I’m not clear what is meant by an “entry point”. Does it mean a function on the vault contract? Or does it mean a separate contract altogether?

By entry point, it refers to a ERC4626 or ERC7540 Vault, so a separate contract altogether.

So as an example, there could be

- share at 0x01
- vaultA with asset=USDC at 0x02, minting/burning the share at 0x01
- vaultB with asset=DAI at 0x03, also minting/burning the share at 0x01

> Also, do you know if there a reference implementation available?

There is no standalone reference implementation available yet, but you can look at the Centrifuge implementation of ERC7540 + ERC7575. It refers to the `share` in the Vault contract here: [liquidity-pools/src/ERC7540Vault.sol at 215b3ff693bbba9627d56cbf8fb79437dff1147d · centrifuge/liquidity-pools · GitHub](https://github.com/centrifuge/liquidity-pools/blob/215b3ff693bbba9627d56cbf8fb79437dff1147d/src/ERC7540Vault.sol#L40). And links back to the `vault` here in the share contract: [liquidity-pools/src/token/Tranche.sol at 215b3ff693bbba9627d56cbf8fb79437dff1147d · centrifuge/liquidity-pools · GitHub](https://github.com/centrifuge/liquidity-pools/blob/215b3ff693bbba9627d56cbf8fb79437dff1147d/src/token/Tranche.sol#L34)

---

**beringela** (2024-05-09):

Many thanks [@jeroen](/u/jeroen). A follow up question, which of these is correct:

a) A “multi-asset vault” is a separate contract in its own right, and can be thought of as “wrapping” the other vaults `vaultA`, `vaultB` underneath. If someone says “give me the address of your multi-asset vault” I can give them one address.

b) A “multi-asset vault” is actually just the logical grouping of `vaultA` and `vaultB` and `share` all taken together. If someone says “give me the address of your multi-asset vault” I would give them a collection of addresses.

Up till now I was thinking a) is true, but having seen your example, I think now it is b) that is true.

---

**jeroen** (2024-05-09):

Yeah exactly it is b).

---

**beringela** (2024-05-09):

Great, thanks! I think it’d be helpful to new readers to add something explaining that to the ERC. There is no actual “multi-asset vault” contract, it is a logical construct of the *component* vault contracts.

Now imagine I’m looking at an ERC-7575 contract. I call `share()` to get the share token address, and it returns an external ERC-20 contract. Now on that share token contract, I call `vault(asset address)` to get the address of the vault for a given asset.

In this situation, am I able to work out ALL the assets that are supported by that share token contract?

---

**beringela** (2024-05-09):

Would there be value in allowing ERC-7575 entry point contracts to be *fully* backwards compatible with ERC-4626?

If I am following correctly, ERC-7575 entry points *already* have all the ERC-4626 functions, just they “should not” have ERC-20 functions (but can do to allow existing ERC-4626 vaults to be forwards compatible and look like ERC-7575 vaults).

Let’s say that a new ERC-7575 collection of entry point contracts *did* each have all the ERC-20 functions. The ERC-20 functions on each entry point could be passed through to the share token contract (with some extra dev work to give the entry point contracts the authorisations to adjust share token allowances, do share token transfers and so on).

This would mean existing ERC-4626 indexers wouldn’t have to change right away, the ERC-4626 ecosystem would still regard ERC-7575 as vaults.

---

**jeroen** (2024-05-10):

> Would there be value in allowing ERC-7575 entry point contracts to be fully backwards compatible with ERC-4626?

I think this is fine, and is not blocked in the current specification. I would not enforce it though, the “with some extra dev work to give the entry point contracts the authorisations to adjust share token allowances, do share token transfers and so on” part is quite complex. This can be done by implementing ERC-2771 on the share and setting the ERC-7575 entry points as trusted forwarders.

But indeed some ERC-7575 implementations might opt to do this, at which point they are fully compatible with ERC-4626.

Others might not, e.g. implementations of ERC-7540, since these are already non-compliant with ERC-4626, so it makes more sense to keep the vault implementation and share token simpler. (this is the case for the ERC-7540 implementation we have at Centrifuge).

---

**jeroen** (2024-05-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/beringela/48/12441_2.png) beringela:

> Now imagine I’m looking at an ERC-7575 contract. I call share() to get the share token address, and it returns an external ERC-20 contract. Now on that share token contract, I call vault(asset address) to get the address of the vault for a given asset.
>
>
> In this situation, am I able to work out ALL the assets that are supported by that share token contract?

Not easily onchain no. I don’t think it would make sense to store this in an array either, it would add significant gas overhead (for updating and reading the array).

What we could consider, is adding events to the share token, like

```auto
AddVault(address indexed asset, address vault)
RemoveVault(address indexed asset, address vault)
```

What use case do you think this would help with?

Currently 4626 vaults are anyways already indexed through other means.

I would also think in most cases, a user would want to look up a vault by a specific asset, rather than get the full list.

But if there’s a clear value for this, I’m happy to add this to the spec!

---

**beringela** (2024-05-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jeroen/48/10696_2.png) jeroen:

> I would also think in most cases, a user would want to look up a vault by a specific asset, rather than get the full list.

Yes I agree, adding a list is not ideal. The use case I was thinking of was just indexers. If I look at a share token contract, I can tell it is ERC-7575 (presumably the share token is also obligated to have ERC-165?). I might wonder “what entry points does this share token have?”. At present I can’t easily answer that by looking on-chain, but with the addition of those events on the share token I could collect those events and work it out. Indexers can then make sense of the vault without needing additional off-chain knowledge.

Maybe the ERC spec could have addVault etc functions defined against the share token, those are not explicitly mentioned.

---

**jeroen** (2024-05-13):

Here’s some proposed updates to the spec to address your comments: [Update ERC7575 by hieronx · Pull Request #23 · ERC4626-Alliance/ERCs · GitHub](https://github.com/ERC4626-Alliance/ERCs/pull/23/files)

- ERC-165 was added to the share token, but optionally, for backwards compatibility (same reason the vault-to-share lookup is optional)
- UpdateVault event was added. This is more flexible than the add/remove events.
- No methods were added, since there is no clear use case for integrating add/removeVault methods, just for indexing the changes, I wouldn’t include this.

---

**beringela** (2024-05-15):

Ok thanks Jeroen. A few more points:

1. The section titled “backwards compatibility” shouldn’t that read “forwards compatibility”? This is because it talks about making existing ERC-4626 vaults forwards compatible with ERC-7575. When new multi-asset vaults are created, if we follow the standard, the vaults should not be ERC-20. So therefore, in general, we’d expect ERC-7575 vaults to not be backwards compatible with ERC-4626.
2. The section titled “pipes”, could you explain that further, maybe supply examples of how uni-/bi-directional vaults would look? As it stands, when I read this sentence “a unidirectional Pipe SHOULD implement only the entry function(s) deposit and/or mint” it makes it sound like assets can only move into the vault and never out of the vault. Presumably a vault that is a pipe needs a function asset() that gives the address of the external asset? (similar to share() providing external share address). Do non-pipe vaults need that function too?
3. In the section on “Specification” under sub-section “Definitions” it says "existing definitions from ERC-4626 apply. But then under the sub-sections “Methods” it doesn’t say “also include all the methods and events from ERC-4626”. I think it is implied, but it should be spelled out.
4. I think a sentence near the start explaining that there is no such thing as an address of a multi-asset vault, rather a multi-asset vault is a logical grouping of ERC-7575 compliant “component” vaults that happen to share the same share token. It might just be me, but it took me a while to appreciate that. I’d thought a multi-asset vault was a separate contract that “wrapped” the component vaults.

---

**jeroen** (2024-05-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/beringela/48/12441_2.png) beringela:

> The section titled “backwards compatibility” shouldn’t that read “forwards compatibility”? …
> In the section on “Specification” under sub-section “Definitions” it says "existing definitions from ERC-4626 apply. But then under the sub-sections “Methods” it doesn’t say “also include all the methods and events from ERC-4626”. I think it is implied, but it should be spelled out.
> I think a sentence near the start explaining that there is no such thing as an address of a multi-asset vault, …

Really good feedback, thanks! All updated in [ERC7575 updates by hieronx · Pull Request #28 · ERC4626-Alliance/ERCs · GitHub](https://github.com/ERC4626-Alliance/ERCs/pull/28)

Also added a pseudocode reference implementation which should help clarify the 4th point regarding the grouping of the multi-asset vault components.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/beringela/48/12441_2.png) beringela:

> The section titled “pipes”, could you explain that further, maybe supply examples of how uni-/bi-directional vaults would look? As it stands, when I read this sentence “a unidirectional Pipe SHOULD implement only the entry function(s) deposit and/or mint” it makes it sound like assets can only move into the vault and never out of the vault. Presumably a vault that is a pipe needs a function asset() that gives the address of the external asset? (similar to share() providing external share address). Do non-pipe vaults need that function too?

`asset` is already part of 4626: [ERC-4626: Tokenized Vaults](https://eips.ethereum.org/EIPS/eip-4626#asset)

---

**beringela** (2024-05-17):

Going back to the event “VaultUpdate” emitted by the share, how can we tell by looking at that event if the vault was added or removed from the share?

---

**jeroen** (2024-05-17):

To remove a vault you would set the address to `address(0)`. If it’s not the zero address, it would be either added (if it was previously the zero address) or updated (if it was previously another non-zero address).

---

**beringela** (2024-05-17):

understood, thank you

---

**beringela** (2024-05-28):

Hey Jeroen thanks for all the updates, it’s looking good. Here are some more comments and questions:

## 1) Backwards compatibility

In the section “Backwards Compatibility” it says:

> ERC-7575 Vaults are compatible with ERC-4626 except for the ERC-20 functionality which has been removed.

I think this could be misinterpreted, it kind of suggests ERC-7575 is backwards compatible, which it isn’t. I think it would be clearer to say:

> ERC-7575 Vaults are not backwards compatible with ERC-4626 because the ERC-20 functionality which has been removed.

## 2) Pipes

I understand pipes only at the highest level, they convert one thing to another. But I do not understand how they would work. Also, where it says:

> A unidirectional Pipe SHOULD implement only the entry function(s) deposit and/or mint

If a contract didn’t implement other entry functions (which ones?) then that would surely make it non-ERC-7575 compliant?

## 3) Asset contracts as ERC-7575 contracts

I’m thinking of a use case, say where we have 20 assets (ERC-20 of course). We want to put them into a multi-asset vault. We’d create another 20 contracts (one ERC-7575 vault per asset) plus 1 for the share. Couldn’t we have the asset contract *also be* the vault contract? I know the spec says “the entry points SHOULD NOT be ERC-20.” but why is this?

---

**jeroen** (2024-05-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/beringela/48/12441_2.png) beringela:

> I think this could be misinterpreted, it kind of suggests ERC-7575 is backwards compatible, which it isn’t. I think it would be clearer to say:

That’s fair, updated.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/beringela/48/12441_2.png) beringela:

> If a contract didn’t implement other entry functions (which ones?) then that would surely make it non-ERC-7575 compliant?

This refers to not implementing redeem and/or withdraw (since that would make it non-unidirectional). I’ll update the spec to make this clearer.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/beringela/48/12441_2.png) beringela:

> I’m thinking of a use case, say where we have 20 assets (ERC-20 of course). We want to put them into a multi-asset vault. We’d create another 20 contracts (one ERC-7575 vault per asset) plus 1 for the share. Couldn’t we have the asset contract also be the vault contract? I know the spec says “the entry points SHOULD NOT be ERC-20.” but why is this?

The SHOULD NOT is a reference to the 7575 vault not implementing the share ERC20 methods.

I’m not sure I follow entirely how the Vault could also be the asset itself. But the spec is not preventing this in any case, since it states SHOULD NOT rather than MUST NOT.

---

**beringela** (2024-05-28):

Thanks Jeroen, I see the updates are there it is clearer to me now.

I still have a big gap though around pipes. I get the high level idea. I do not understand how they will work. It might just be me, but I don’t think there is enough explanation for a new reader about how they will work.

---

**jeroen** (2024-05-28):

I added a short explanation of pipes now as well.

To add some more context here, the idea is for example for a pipe to be used to represent a PSM. Something like (pseudocode)

```solidity
contract PSM {
  IERC20 asset = USDC;
  IERC20 share = DAI;

  function deposit(uint256 assets, address receiver) external returns (uint256 shares) {
    shares = convertToShares(assets);
    asset.transferFrom(msg.sender, address(this), assets);
    share.mint(receiver, shares);
  }

  function redeem(uint256 shares, address receiver, address owner) external returns (uint256 assets) {
    require(owner == msg.sender);
    assets = convertToAssets(shares);
    share.burn(owner, shares);
    asset.transferFrom(adress(this), receiver, assets);
  }
}
```

---

**beringela** (2024-05-30):

Ok thanks Jeroen. What does PSM stand for here?


*(10 more replies not shown)*
