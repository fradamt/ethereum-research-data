---
source: magicians
topic_id: 11612
title: "EIP-5875: Opcode for TX number in a block"
author: xinbenlv
date: "2022-11-04"
category: EIPs > EIPs core
tags: [opcodes]
url: https://ethereum-magicians.org/t/eip-5875-opcode-for-tx-number-in-a-block/11612
views: 1175
likes: 5
posts_count: 10
---

# EIP-5875: Opcode for TX number in a block

Github Pull Requestion: [Add EIP-5875: Instruction to Get Transaction Index of Block by xinbenlv · Pull Request #5875 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/5875/files)

A TX is an *atomic* point of time for world state.

Currently we have access to `blocknum` but there is no way to access a `txnum` within a smart contract.

We hereby propose a `TXNUM` opcode instruction to fetch TXNUM which can be used to

1. identify the ordering of exact transaction in its block
2. Better than blockNum: identifying uniquely and unambiguously the world state.
3. Better than txHash: allow simply arithmatic  by  BlockNum.TxNum

It would be helpful for on-chain and off-chain indexing and snapshotting.

An example of use-case is [EIP-5805 Voting with Delegation](https://ethereum-magicians.org/t/eip-5805-voting-with-delegation/11407) wants to store snapshot of voting rights. The current option with with either block.timesamp or block.number all only have the granularity at the level of blocks. But world state changes across transaction. If there is any TX in the same block cause a voting right to change, the blocknum or block.timstamp will not be sufficient to pin-point the world state of snapshot of voting rights.

Previous attempts:

1. Transaction index OpCode by decanus · Pull Request #4363 · ethereum/EIPs · GitHub

### Request for feedback

- @Amxx , @frangio, the author and contributors of EIP-5805

## Replies

**MicahZoltu** (2022-11-05):

In the past, we have introduced opcodes that seemed reasonably useful but later we found people using them in ways that harmed the network.  Examples include ORIGIN and SELFDESTRUCT.  ORIGIN is used by people to discriminate between contracts and EOAs, which has made contract wallet adoption harder than it otherwise would have been and SELFDESTRUCT has been used for gas banking over time.

Given these past experiences, I am now generally reluctant to add new opcodes that expose world state details to the EVM as it is possible that someone could leverage them in the future to do bad things.

This isn’t to say this is a bad idea, I just want to make sure that we try *extremely* hard to think of the worst things people could do with the transaction number to ensure we aren’t introducing another opcode that causes problems for us down the road.

Off the top of my head, one can imagine using such an opcode to cause a transaction to simulate differently than it executes, perhaps leading to scams (there are other ways to do this, but they often aren’t reliable).

---

**yoavw** (2022-11-05):

I’m with [@MicahZoltu](/u/micahzoltu) .  I can see a number of ways this will be abused.

One is a more reliable way to mess with simulations, as Micah pointed out.  It’ll have to be banned in any situation where simulation matters.  During ERC-4337 validation it’ll just be added to the banned opcodes along with things like ORIGIN, but there may be less obvious ways.

Another is MEV searchers messing with transactions.  The block builder has direct control over this variable.  Any reliance on this opcode to determine execution flow could enable some form of frontrunning/sandwiching.

The snapshot voting use case in the EIP could be addressed by other means.  For example saving `start=block.number+1` at the current block, and then only starting to count votes at `start` (the next block).  Mid-block changes in the previous block have no effect.

Also, any use case that requires establishing causality between transactions could also be addressed through state.  E.g. checking and incrementing midBlockCtrs[block.number].

[@xinbenlv](/u/xinbenlv) if would be useful if you add a couple of more use cases where this opcode is needed.  It’ll be good to consider whether:

1. There’s no other way to address them.
2. The opcode enables solving them safely - while assuming block builders with malicious intent.

---

**xinbenlv** (2022-11-06):

Thanks [@yoavw](/u/yoavw) and [@MicahZoltu](/u/micahzoltu) .

I agree with [@MicahZoltu](/u/micahzoltu) that we need to think really hard for cases that this proposed opcode can be used to do bad things.

[@yoavw](/u/yoavw) I kind of wonder if MEV would be made worse by this opcode. Ultimately I feel that MEV has too be solved by block producer to know Zero Knowledge other than  a specific batch of TXs are valid as a whole, before they can pack a block. Anything else, if a block producer is malicious or team with MEVer, I  couldn’t think of a thing that *with* this opcode it could abuse but without this opcode they could not abuse.

Could I borrow your wisdom to get a specific example of what kind of MEV abuse is enabled that was not previously possible without the new opcode?

I am also debating whether the TXNUM should return (1) the index of the TX in this *current* block or (2) the index of this TX in all the *history* of blocks… It seems at least (2) eliminates that a miner/MEVer could use the relative index of a given TX within a block

---

**yoavw** (2022-11-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> I kind of wonder if MEV would be made worse by this opcode.

I believe it can be.  This opcode gives block builders a direct way to change the outcome of the transaction.  Once the transaction is included (with the wrong outcome from the user’s perspective), it is no longer in the mempool and cannot be included in a subsequent block.  Therefore any case where a block builder could benefit from censoring a transaction, would be affected by this opcode.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> I feel that MEV has too be solved by block producer to know Zero Knowledge

I don’t think we’re ever going to fully eliminate MEV (but that’s a bit beyond the scope of this thread I guess).  However, we should be careful when introducing new vectors.  I think it’ll be quite challenging to use TXNUM in a contract without introducing undesired MEV vectors.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> Could I borrow your wisdom to get a specific example of what kind of MEV abuse is enabled that was not previously possible without the new opcode?

Plenty.  As I explained above, if the execution flow depends in any way on TXNUM, the block builder can control that branch of the execution flow.  If it can lead to a revert, or to some operation happing or not happening, then there’s a censorship vector.

Frontrunners typically can’t censor other transactions, only get in front of them and affect the price.  But they couldn’t for example, prevent your vote in a governance proposal from being counted.  In the example you used in the EIP, a block builder could invalidate a vote that happens in the same block by moving it around.  That’s something they wouldn’t be able to do without this opcode.

The same goes for any contract where an action would depend on TXNUM.  Suppose a contract uses commit/reveal to protect users against frontrunning.  Currently it’s immune to MEV.  A concrete example is ENS, where you commit your domain registration before revealing the name.  Currently there’s no way to prevent the registration.  If a block builder doesn’t include it, the next one will, or the one after that.  Now suppose ENS used TXNUM anywhere in the transaction that finalizes the registration.  An mev-boost builder will pay the next builder to include it in a position that causes it to fail.  They only do it once, since the transaction reverts and the user needs to resubmit it.  Keep watching the mempool, invalidate any such transaction at the cost of a single transaction.  It would effectively censor the registration.

Suppose a rollup would use TXNUM in its L1 batching contract.  A builder can similarly prevent finalization of the entire rollup chain by including it in the wrong position.  It makes things quite brittle.

What are some use cases that can only be implemented with TXNUM and wouldn’t be vulnerable to such attacks?

The only use case I could think of, is one that benefits MEV searchers: require the block proposer to include their transaction early in the block and be able to verify it.  But I’m sure that’s not what you have in mind.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> It seems at least (2) eliminates that a miner/MEVer could use the relative index of a given TX within a block

Why would it matter if it’s relative to the entire history or just this block?  The code will still make decisions based on its relative position in the current block (or else it could just use block.number).  Once the code makes decisions based on that, it’s likely to become vulnerable to such manipulations.

---

**xinbenlv** (2022-11-11):

Adding [Transaction index OpCode by decanus · Pull Request #4363 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/4363) as previous attempt

---

**sbacha** (2022-11-30):

Am I to understand that the cost of this OPCODE is 2 ? Should it not be priced closer to EXCODESIZE or BALANCE?

This would enable implementing transaction dependencies would it not?

Edit: Here is a way of providing such tx hash poof using current protocol:

[Hidden in Plain Sight: A Sneaky Solidity Implementation of a Sealed-Bid Auction - a16z crypto](https://a16zcrypto.com/hidden-in-plain-sight-a-sneaky-solidity-implementation-of-a-sealed-bid-auction/) see [auction-zoo/OverCollateralizedAuction.sol at main · a16z/auction-zoo · GitHub](https://github.com/a16z/auction-zoo/blob/main/src/sealed-bid/over-collateralized-auction/OverCollateralizedAuction.sol#L182)

---

**xinbenlv** (2022-12-01):

[@sbacha](/u/sbacha) thank you for the comment

I was proposing gas cost to be 8 (same as BLOCK or TIMESTAMP), open to be convinced.

- BLOCK 8
- TIMESTAMP 8
- EXTCODESIZE and BALANCE depends on the way touching address or not below

> gas_cost = 100 if target_addr in touched_addresses (warm access)
> gas_cost = 2600 if target_addr not in touched_addresses (cold access)

It seems none of them is `2`. Could you clarify [@sbacha](/u/sbacha) ?

> Edit: Here is a way of providing such tx hash poof using current protocol:
> Hidden in Plain Sight: A Sneaky Solidity Implementation of a Sealed-Bid Auction - a16z crypto  see auction-zoo/OverCollateralizedAuction.sol at main · a16z/auction-zoo · GitHub

[@sbacha](/u/sbacha) could you share a Github permlink so it doesn’t change due to new commits to the repo?

---

**sbacha** (2023-04-12):

Whats the status with this EIP? You need help? Very interested in getting this through.

---

**xinbenlv** (2023-04-12):

I love to pursue it, but

IIUC, two things block it

1.(against) Some core devs are concerned this could be used for MEV to make such problems more severe

2.(lack of support) Some core devs want to see stronger use case to justify this cost and risk.

