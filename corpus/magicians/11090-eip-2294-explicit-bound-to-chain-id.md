---
source: magicians
topic_id: 11090
title: "EIP-2294: Explicit bound to Chain ID"
author: xinbenlv
date: "2022-09-28"
category: EIPs > EIPs informational
tags: [evm, opcodes, core-eips, shanghai-candidate, chain-id]
url: https://ethereum-magicians.org/t/eip-2294-explicit-bound-to-chain-id/11090
views: 4829
likes: 28
posts_count: 29
---

# EIP-2294: Explicit bound to Chain ID

I came across this [EIP-2294](https://github.com/ethereum/EIPs/issues/2294) and think it’s important. Highlighting it here for the community discussion.

Related prior discussion

- EIP-1344: Add chain id opcode
- EIP-1344: Update uint256 field size to uint64 by fubuloubu · Pull Request #2263 · ethereum/EIPs · GitHub

So far the biggest chainid that’s publically known to us is

- 868,455,272,153,094 aka
- 0x 3 15DB 0000 0006

from in [github.com/ethereum-lists/chains](https://github.com/ethereum-lists/chains/blob/master/_data/chains/eip155-868455272153094.json)

---

Update 2022-10-18:

Here are two mutually exclusive scenarios the EIP try to prevent/resolve

1. With the increasing number of chains, in particular in the post-sharding future of EVMs, some people want to use some hash function for collision resilient hashing functions e.g. keccak256(<human-readable-string") as a way to generate new chainIds which will be the full space of uint256
2. ChainId was being used be added to the parity bit for signatures e.g. EIP-712 which has a ceiling of floor(MAX_UINT64 / 2) - 36 unless we manipulate the algorithm.

These two requirement for chainId space must be resolved and I urge that we make a decision before Shanghai hardfork

---

## Invite to comment

### Authors of EIPs that might be affected

- EIP-712:  @recmo et al
- EIP-1191: @juli et al
- EIP-1271: @frangio et al
- EIP-1344: @rmeissner at al
- EIP-1959: @wighawag at al
- EIP-3770: @lukasschor at all

## Replies

**xinbenlv** (2022-09-28):

Resuming the EIP-2294 as PR [EIP-2294: Explicit bound to Chain ID size by xinbenlv · Pull Request #5728 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/5728)

---

**shemnon** (2022-10-04):

One major concern I have with limiting chain IDs to ~63 bits is that you cannot then have a hash used as a chainID.  I would want the limit to be 256, 384, or 512, or unspecified.

~63 bits of entropy is not sufficient collision resistance for a hash function, reasonable use or not.

What may be needed is for clients to present loud warning messages when chain IDs that are not supported by hardware wallets are used (and I think 32 bits is the real limit for that). Just a  loud obnoxious warning if block height is < 100k (i.e. soon enough to reconsider your chain), not a hard block.

---

**xinbenlv** (2022-10-05):

Hi all, I am moving the EIP-2294 to Review status

https://github.com/ethereum/EIPs/pull/5763

---

**xinbenlv** (2022-10-18):

[@shemnon](/u/shemnon)

Totally agree with that rationale. Let me address them and loop in other authors for comment

---

**xinbenlv** (2022-11-10):

In today’s ACD,

[@xinbenlv](https://github.com/xinbenlv) advocated to prioritize EIP-2294 into shanghai fork.

[@MariusVanDerWijden](https://github.com/MariusVanDerWijden) responded that if it’s low cost, let’s do it, but don’t need to have a deadline to be shipped before Shanghai fork.

[@MicahZoltu](https://github.com/MicahZoltu) responded support EIP-2294 that bounds chainId at its current proposed ceiling. Because it has been a de facto rule. [@MicahZoltu](https://github.com/MicahZoltu) further proposed that we don’t need to do any coding immediately, just need to agree as a group and call it a rule.

[@shemnon](https://github.com/shemnon) responded whether we should accept such bounding just because no one has ever used any chainId above bounds. Ask to think twice.

Please correct me if I were wrong.

---

**xinbenlv** (2022-11-10):

@sambacha responded on [github](https://github.com/ethereum/EIPs/issues/2294#issuecomment-1297145918)

Metamask has a hardcoded value for rejecting chainId’s over a certain number. That number is calculated based off of

[source from remarks, metamask engineer](https://gist.github.com/rekmarks/a47bd5f2525936c4b8eee31a16345553)

```auto
From ethereumjs-util@7.0.5, we have that:

  v = recovery + (chainId * 2 + 35)

Per the above discussion, we also have that:

  int_max = 2**53 - 1
  recovery_max = 3
  chainId_max = ?

Therefore:

  v_max = 3 + (chainId * 2 + 35) = chainId * 2 + 38
    &&
  v_max

  2**53 - 1 = MAX_SAFE_CHAIN_ID * 2 + 38

    ->

  // Since we're dealing with integers, we round down.

  MAX_SAFE_CHAIN_ID = floor( ( 2**53 - 39 ) / 2 ) = 4503599627370476
```

Ethereumjs-util as referenced above has BigInt support since 7.0.9, regardless metamask has encoded this value within their application.

[see https://github.com/ethereumjs/ethereumjs-util/releases/tag/v7.0.9](https://github.com/ethereumjs/ethereumjs-util/releases/tag/v7.0.9)

---

**sbacha** (2022-11-10):

Here is an example of how replay protection safe chainId is used in a contract: [tweak: add block.chainid as per t11s public shaming · yieldprotocol/yield-utils-v2@13ec941 · GitHub](https://github.com/yieldprotocol/yield-utils-v2/commit/13ec941f201b0923777771f41de3e72505ef89e8)

A more comprehensive example: [BoringSolidity/Domain.sol at master · boringcrypto/BoringSolidity · GitHub](https://github.com/boringcrypto/BoringSolidity/blob/master/contracts/Domain.sol)

WETH10 adopts such measures even: [WETH10/WETH10.sol at e952d1ec4c149e85d93ed2ce4040ac571ed6bc19 · WETH10/WETH10 · GitHub](https://github.com/WETH10/WETH10/blob/e952d1ec4c149e85d93ed2ce4040ac571ed6bc19/contracts/WETH10.sol#L282)

As for networks that exceed the safe limit, I have only seen one, and it was an ephemeral test network.

---

**shemnon** (2022-11-15):

I understand that some tooling limits CHAIND, but I don’t see this as a reason to shut down all ChainIDs over 53 bits in length.  I see a future where there are large amounts of ephemiral L2 and L3 chains and they will need a mechanical way to set a rational and deterministic means, and a 256 bit hash is that means.  Much like how CREATE2 enabled Uniswap and it’s derivatives.  I don’t want to kneecap this future because math in JavaScript has non-obvious rules.

Perhaps we need to limit chainIDs expressable by transaction types.

- For Type 0/legacy (Frontier) transactions the metamask limit is enforced, since integer math needs to be performed on the chain ID.
- For Type 1 (Berlin) and Type 2 (London) transactions a 256 bit limit is enforced. There is no math done for these transactions: it is a binary blob moved around without encoding.  The limit here comes from EVM limits of 256 bits returned from the CHAINID operation.

The impact being if you want to use a hashed ChainID you must use a modern transaction container.

---

**MicahZoltu** (2022-11-18):

I find the “deterministically generated globally unique chain ID” argument to be quite compelling and I think that puts me into the camp of asserting that ChainID is 256 bits.

---

**xinbenlv** (2022-11-20):

[@MicahZoltu](/u/micahzoltu) good point. I start to find [@shemnon](/u/shemnon) 's argument quite compelling too.

> I see a future where there are large amounts of ephemiral L2 and L3 chains and they will need a mechanical way to set a rational and deterministic means

One possible use case: in the future [@shemnon](/u/shemnon) described one-day that uint256 bit of ChainId could be used to used on a chain to point to another chain… or bridges between them

---

**sbacha** (2023-02-06):

Yall are assuming no contention between competing Chains. In reality chain id is insufficient to be able to guarantee such global characteristics

This is what is needed for those constraints [tmp · sambacha/permit-everywhere@279f475 · GitHub](https://github.com/sambacha/permit-everywhere/commit/279f475517e98d3643d23e222a2c8485540c6e3e)

---

**sbacha** (2023-02-06):

As you have stated yes certainly a compelling use case. How to resolve contention though with competing chainIds?

---

**MicahZoltu** (2023-02-06):

I think that is a separate problem.  Even if we only support Ethereum and Ethereum L2s and we come up with some Ethereum specific mechanism for avoiding collisions (e.g., something like an on-chain registry for chain IDs), there is still value in 2^256 for “deterministically generated globally unique IDs for short-lived chains”.

---

**etan-status** (2023-02-09):

In that case, it would still be great to limit chain ID to `floor(MAX_UINT256 / 2) - 36`, to prevent accidents with type 0/legacy (Frontier) transactions being processed by existing implementations that happily perform integer math on the chain ID.

For example, the deterministic hashing method could always set the top two bits to 0, effectively leading to a list of reserved chain IDs consisting of `0` and the range with one of the top two bits set: `[0x4000..., 0xffff...]`.

---

**etan-status** (2023-02-09):

Small inconsistency:

In Specification section, the allowed range is `[0, MAX_CHAIN_ID]`, but in Rationale section, language suggests that minimum is `1` instead of `0`.

> For reference, a value of 0 or less is also disallowed.

As `0` is not currently used, would appreciate going with the Rationale approach of reserving it. This would allow using `chain_id = 0` to indicate pre-EIP-155 `LegacyTransaction`. This would still be compatible with the uint256 hash based approaches.

---

**xinbenlv** (2023-02-09):

Cross-posting a conversation between etan and me from discord

> (@etan-status ): Heya! I stumbled upon your old EIP-2294. Do you know why it wasn’t adopted yet, given its origin in 2019? Also, you state “For reference, a value of 0 or less is also disallowed.” Where is this specced out?

> ( @xinbenlv ): On one ACD call I asked, the client teams said it was a de facto case right now that no known ChainIds have exceeded the bound indicated in EIP-2294. There has not been code enforcement inside of clients that I personally know off.

---

**xinbenlv** (2023-02-09):

[@etan-status](/u/etan-status) asked if `ChainId=0` is being used.

To my knowledge the smallest known id is `ChainId=1, ETH Mainnet`. I am not aware of any chain using ChainId=0 nor am I aware of ChainId=0 being a reserved for any future or current semantics.

[@MicahZoltu](/u/micahzoltu) could you help correct me if I am wrong?

---

**shemnon** (2023-03-08):

I honestly don’t think any limitation is necessary, since any value that makes a transaction un-handleable will be rejected by either the wallet, mempool, or chain.  A chain will only have chainIDs the clients support, and furthermore one per chain right now.  So to wind up on the chain there must be at least one client that can handle it, and then at least one wallet that supports it (or custom submission software).  The software will implicitly limit it without need to force it down the rest of the chain.  Metamask in effect enforces the 55 bit limit for legacy transactions.

There already exists a consensus rule for chainID bounds: each chain accepts only one.  Mainnet and the testnets only accept single bytes at the moment.

Placing a limit on the size of the chainID only places an unneeded limit in innovation.  Clients will ignore that the moment it becomes interesting, such as the size limit on ExtraData in the block header, something the python libs ever enforced.

---

**sbacha** (2023-03-24):

Could ChainId=0 be used to help support multiple wallets / connections to multiple chains? We used a specific chainId to do this for metamask to get it to send txs to mainnet and testnet at the same time.

Agreed that placing a limit in the spec is not useful, was moreso making a note for developers down the line whom may encounter that edge case.

---

**etan-status** (2023-04-20):

Another problem there is that transaction types may have different meaning across chains. Only the legacy transaction type (without chain ID) is truly replayable across networks, for the rest there is no guarantee.


*(8 more replies not shown)*
