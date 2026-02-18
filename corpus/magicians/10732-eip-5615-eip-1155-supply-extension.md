---
source: magicians
topic_id: 10732
title: "EIP-5615: EIP-1155 Supply Extension"
author: Pandapip1
date: "2022-09-07"
category: EIPs
tags: [nft]
url: https://ethereum-magicians.org/t/eip-5615-eip-1155-supply-extension/10732
views: 2727
likes: 1
posts_count: 14
---

# EIP-5615: EIP-1155 Supply Extension

https://github.com/ethereum/EIPs/pull/5615

Since, apparently, this isn’t an EIP yet?!

## Replies

**SamWilsn** (2022-10-24):

Would you mind adding a bit to the Rationale section about why `exists` needs to *ahem* exist at all?

---

**Pandapip1** (2022-10-24):

Sure. The answer is simple: backward compatibility.

---

**CHANCE** (2022-11-01):

Does this support “backward compatibility,” though?

I presume this to mean consistency in existing ecosystem standards?

For example, Etherscan total supply would still be broken provided this implementation: [Please (PLEAS) Token Tracker | PolygonScan](https://polygonscan.com/token/0xd047e4b2c6f7d5072bbea49ee560525ca7e05efc) and an individual token page does not even show supply (because it has not been standardized, obviously) [Please (PLEAS) Token Tracker | PolygonScan](https://polygonscan.com/token/0xd047e4b2c6f7d5072bbea49ee560525ca7e05efc?a=1).

Is the definition of this EIP accepting that the “enabled” functionality will have little result on the state of 1155s and that existing support for “Supply” extensions will still be non-functional at the collection level?

---

**fulldecent** (2022-11-06):

The backwards compatibility section should reference ERC-20 and ERC-721. Clearly this function is modeled off the expectations set by those two specifications and ecosystem.

---

**Pandapip1** (2022-11-06):

> The backwards compatibility section should reference ERC-20 and ERC-721.

This is **not** backward compatible with EIP-20 or EIP-721. It is implicitly compatible with EIP-1155, as it is an extension.

> Clearly this function is modeled off the expectations set by those two specifications and ecosystem.

This is true, and I will add a variation of this in the rationale.

---

**Pandapip1** (2022-11-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/chance/48/7577_2.png) CHANCE:

> Does this support “backward compatibility,” though?

It’s backward compatible with the most commonly used/widely supported supply extension; the OpenZeppelin one.

---

**Pandapip1** (2022-11-06):

Relevant links:



      [github.com/OpenZeppelin/openzeppelin-contracts](https://github.com/OpenZeppelin/openzeppelin-contracts/issues/2536)












####



        opened 12:01PM - 24 Feb 21 UTC



          closed 11:37PM - 13 Jul 21 UTC



        [![](https://ethereum-magicians.org/uploads/default/original/2X/2/25ecfec94e89e81e1553723f9a30aef27c4e1627.jpeg)
          Amxx](https://github.com/Amxx)





          contracts


          idea







**🧐 Motivation**
ERC1155 supports a middle-ground between ERC20 (fungible) and […]()ERC721 (unfungible) in which token are fungible within the same tokenId. Depending on the sum of all balances for a tokenId, the corresponding token can be seen as fungible or nonfungible. However, there is no on-onchain mechnism to keep track of this.

**📝 Details**
A `totalSupply(uint256 tokenId)`, similar to ERC20's `totalSupply`, but with a "per tokenid" result be provided. This would be usefull to distinguish between fongible and nonfongible assets. It also adds a `exists(uint256 tokenId)` function that returns weither the totalSupply is not null. This would be equivalent to checking weither the corresponding token exists.














      [github.com/OpenZeppelin/openzeppelin-contracts](https://github.com/OpenZeppelin/openzeppelin-contracts/pull/2185)














####


      `master` ← `KaiRo-at:erc1155-exists`




          opened 01:16PM - 14 Apr 20 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/b/baca9ae447eeb6d6c075cb27f9117f809d99f2c6.jpeg)
            KaiRo-at](https://github.com/KaiRo-at)



          [+36
            -0](https://github.com/OpenZeppelin/openzeppelin-contracts/pull/2185/files)







This PR is based on a discussion started at https://github.com/OpenZeppelin/open[…](https://github.com/OpenZeppelin/openzeppelin-contracts/pull/2185)zeppelin-contracts/issues/2003#issuecomment-612109928 and should give the ERC-1155 implementation more compatibility to OpenZeppelin's ERC-721 implementation and also better compatibility to services like OpenSea as pointed to by https://twitter.com/xanderatallah/status/1232124941425881089

The main thing introduced here is an `_exists()` function that is checked in a few places where we'd otherwise return a null-ish default value (`0` or `''`), and to know if a token ID is valid, it has to be registered internally first - either via minting a first token on that ID, or by calling an explicit function.

Tests will fail on this PR for the moment as it bases on both #2130 and #2029 - also, I have not written any tests for this PR itself yet as it's mostly a suggestion on how we could do this in a good way.

---

**Pandapip1** (2022-11-06):

Copying this [from another thread](https://github.com/ethereum/EIPs/pull/5778#issuecomment-1304884991):

OpenSea supports both of these functions. This is undocumented but is clear from their example repository. It’s also noted in the first thread I just linked to. I don’t know whether to mention this or not. I’m leaning slightly towards no (it’s undocumented!) but my mind can be easily changed on this.

OpenZeppelin, of course, has an implementation of this, as noted in the EIP itself.

I don’t see an easy way to track support for this for deployed contracts.

---

**SamWilsn** (2022-11-25):

We’re trying a new process where we get a volunteer peer reviewer to read through your proposal and post any feedback here. Your peer reviewer is [@dadybayo](/u/dadybayo)!

---

[@dadybayo](/u/dadybayo) please take a look through [EIP-5615](https://eips.ethereum.org/EIPS/eip-5615) and comment here with any feedback or questions. Thanks!

---

**estarriolvetch** (2022-12-05):

One challenge I can think of with this EIP is: In order to have `exists()` work in some implementations, it may require adding additional counters in the implementation, leading to a higher gas usage.

---

**Pandapip1** (2022-12-05):

I guess this could be fixed by making that function optional. It doesn’t seem fully necessary (even if it’s very useful).

---

**jseam** (2022-12-15):

In this EIP spec, it states that in `totalSupply()` that `This MUST revert if exists(id) returns false`.

It might be not ideal to revert, as it is possible that a function would want to check if `totalSupply(some id) = 0`. Instead of requiring a revert in `totalSupply()` if `exists()` equals false, it should just return 0 and let the respective functions that rely on `totalSupply()` handle the logic instead. This is the behavior in the existing OpenZeppelin contract.

---

**Pandapip1** (2022-12-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jseam/48/7960_2.png) jseam:

> It might be not ideal to revert, as it is possible that a function would want to check if totalSupply(some id) = 0. Instead of requiring a revert in totalSupply() if exists() equals false, it should just return 0 and let the respective functions that rely on totalSupply() handle the logic instead. This is the behavior in the existing OpenZeppelin contract.

This seems reasonable for backward compatibility. I’ll make that change.

