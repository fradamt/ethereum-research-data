---
source: magicians
topic_id: 15989
title: "EIP-7528: ETH (Native Asset) Address Convention"
author: joeysantoro
date: "2023-10-03"
category: EIPs
tags: [erc]
url: https://ethereum-magicians.org/t/eip-7528-eth-native-asset-address-convention/15989
views: 3815
likes: 13
posts_count: 15
---

# EIP-7528: ETH (Native Asset) Address Convention

---

## eip: 7528
title: ETH (Native Asset) Address Convention
description: An address placeholder for ETH when used in the same context as an ERC-20 token.
author: Joey Santoro ()
discussions-to:
status: Draft
type: Standards Track
category: ERC
created: 2023-10-03
requires: 20, 4626

## Abstract

The following standard proposes a convention for using the address `0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE` in all contexts where an address is used to represent ETH in the same capacity as an ERC-20 token. This would apply to both events where an address field would denote ETH or an ERC-20 token, as well as discriminators such as the `asset` field of an ERC-4626 vault.

This standard generalizes to other EVM chains where the native asset is not ETH.

## Motivation

ETH, being a fungible unit of value, often behaves similarly to ERC-20 tokens. Protocols tend to implement a standard interface for ERC-20 tokens, and benefit from having the ETH implementation to closely mirror the ERC-20 implementations.

In many cases, protocols opt to use Wrapped ETH (e.g. WETH9 deployed at address 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2 on Etherum Mainnet) for ERC-20 compliance. In other cases, protocols will use native ETH due to gas considerations, or the requirement of using native ETH such as in the case of a Liquid Staking Token (LST).

In addition, protocols might create separate events for handling ETH native cases and ERC-20 cases. This creates data fragmentation and integration overhead for off-chain infrastructure. By having a strong convention for an ETH address to use for cases where it behaves like an ERC-20 token, it becomes beneficial to use one single event format for both cases.

One intended use case for the standard is ERC-4626 compliant LSTs which use ETH as the `asset`. This extends the benefits and tooling of ERC-4626 to LSTs and integrating protocols.

This standard allows protocols and off-chain data infrastructure to coordinate around a shared understanding that any time `0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE` is used as an address in an ERC-20 context, it means ETH.

## Specification

This standard applies for all components of smart contract systems in which an address is used to identify an ERC-20 token, and where native ETH is used in certain instances in place of an ERC-20 token. The usage of the term Token below means ETH or an ERC-20 in this context.

Any fields or events where an ERC-20 address is used, yet the underlying Token is ETH, the address field MUST return `0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE`

Any fields or events where the Token is a non-enshrined wrapped ERC-20 version of ETH (i.e WETH9) MUST use that Token’s address and MUST NOT use `0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE`.

## Rationale

Smart Contract Systems which use both ETH and ERC-20 in the same context should have a single address convention for the ETH case.

### Considered alternative addresses

Many existing implementations of the same use case as this standard use addresses such as 0x0, 0x1, and 0xe for gas efficiency of having leading zero bytes.

Ultimately, all of these addresses collide with potential precompile addresses and are less distinctive as identifiers for ETH.

`0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE` has the most current usage, is distinctive, and would not collide with any precompiles. These benefits outweigh the potential gas benefits of other alternatives.

## Reference Implementation

N/A

## Backwards Compatibility

This standard has no known compatibility issues with other standards.

## Security Considerations

Using ETH as a Token instead of WETH exposes smart contract systems to re-entrancy and similar classes of vulnerabilities. Implementers must take care to follow the industry standard development patterns (e.g.  checks-effects-interactions) when the Token is ETH.

## Copyright

Copyright and related rights waived via CC0.

## Replies

**kryptoklob** (2023-10-03):

Thoughts:

1. I think a standard that unifies the several different ways that ETH is represented when returning asset addresses is a great idea
2. I think the specification can be simplified/reworded a bit: “When a smart contract returns an ERC20 address of specifically 0xEEeeEEEE (or whatever you decide on), this signifies that the ERC20 is not actually an ERC20, but raw ETH instead. This signifies to the caller that they should not attempt to transfer this token via ERC20 methods (such as .transfer, .transferFrom).”
3. I don’t think 0xE has any gas improvements from 0xEEEeEEEE…EEE form unless you’re loading via assembly, but I could be wrong.

---

**joeysantoro** (2023-10-12):

Moving the proposal to review status.



      [twitter.com](https://twitter.com/joey__santoro/status/1709708704243667435?s=20)





####

[@joey__santoro](https://twitter.com/joey__santoro/status/1709708704243667435?s=20)

  If you needed to represent ETH with an ERC-20 address as an industry standard, which would you pick:

more context below

  https://twitter.com/joey__santoro/status/1709708704243667435?s=20










I did a twitter poll and 0xeeee…eeee won by a decent margin, but not an overwhelming one. The benefits of 0xe are still strong for the longer term especially if the precompile address can be reserved for a potential future enshrined ERC-20 native asset.

I am hoping to get more focused feedback from Eth magicians before adjusting the proposal.

---

**wminshew** (2023-10-12):

Would be nice to standardize. I prefer 0xE as well but am fine w 0xeeee

---

**joeysantoro** (2023-10-13):

Updated the proposed address to `0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE` due to the following feedback

1. It won a twitter poll by hundreds of votes
2. Specifically, major protocols and institutions such as Curve and Coinbase use this address to denote eth already
3. There is currently no known way to reserve a precompile address as in the original proposal Discord
4. Existing tooling like Foundry already has cheat code overrides for 0xe
5. The gas benefits are only useful when sending the address via calldata, and it is only ~300 gas difference

---

**timbeiko** (2023-10-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/joeysantoro/48/5147_2.png) joeysantoro:

> There is currently no known way to reserve a precompile address as in the original proposal Discord

One detail worth emphasizing: precompiles are allocated sequentially from `0x00...01` and up. Given we don’t have a way to “reserve” precompiles, it’s likely `0x00..0e` would be allocated “by default” when we hit it. For example, see [EIP-2537](https://eips.ethereum.org/EIPS/eip-2537#proposed-addresses-table). Given the pace at which we add precompiles, by the time we get to `0xEe...eE`, I doubt the universe would still exist ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12)

---

**SamWilsn** (2023-10-23):

Are there any security considerations that should be included in a similar vein to: users get used to `0xEe...` representing ether, and try to use it in contracts that don’t follow this convention?

---

**joeysantoro** (2023-10-25):

I think this is the same class of issue as “what if the ERC-20 I’m interacting with is malicious or not implemented to spec”

In other words, non implementation of the spec is sort of always an issue. Protocols / users should be aware of the safe patterns for interacting and use design patterns that don’t break when something isn’t compliant.

In the case of EIP-7528 here its far more likely that a non-implementation case would simply revert as the attack surface is minimal. Worst case seems to be lost tokens.

Would this merit a discussion in security considerations? I don’t think it is noteworthy enough.

---

**SamWilsn** (2023-10-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/joeysantoro/48/5147_2.png) joeysantoro:

> Would this merit a discussion in security considerations? I don’t think it is noteworthy enough.

You’d be very surprised at what people are willing to fight for…

---

**0xMawuko** (2023-10-26):

More specifically about using Twitter for polling:

A lot of factors come into play such as

- Lack of a proper or well-defined quorum.
- Poll creator not being “famous” enough to garner interest/votes.
- Poll creator’s account being limited/censored w.r.t. their reach
- The risk of bots addling the polling process. Poll creator or adversary can easily pay for bots to sway the results.

I’m on highlighting this because a Twitter Poll was used to gain a sense of support for this EIP. Ideally, we should have a standard system for organising polls for the purpose of EIPs/ERCs.

---

**joeysantoro** (2023-10-28):

the rationale listed above was in no particular order. I was actually ready to disregard the results of the twitter poll and keep 0xe but the other issues outweighed the gas savings.

---

**sbacha** (2023-11-30):

`0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE` is actually not ERC-1191 compliant, the correct address *should* be

`0xeeeEEEeEEeeeEeEeEEEeEeeeeEEEEeEEeEeeeeeE`

ERC-1191 does checksum encoding using `chainId`, see the spec here: https://github.com/ethereum/ercs/blob/master/ERCS/erc-1191.md

---

**joeysantoro** (2023-12-04):

Good point, I’ll update to be ERC-1191 compliant

---

**joeysantoro** (2023-12-13):

Is there a reason ERC-1191 isn’t final? If it isn’t being adopted or has no plans to become final, then I don’t think it would be worth it to include here.

---

**joeysantoro** (2023-12-13):

Made some light changes to get around the 1191 issue [Update ERC-7528: ERC 7528 Clarifications by Joeysantoro · Pull Request #161 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/161/commits/d3fd26b7b54f54bf52ba5b91a9035beddeaa3803)

Basically reverted to all lowercase in the EIP with a reference to “checksum such as ERC-155”

