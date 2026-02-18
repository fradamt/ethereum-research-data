---
source: magicians
topic_id: 27228
title: Conditional transactions (EIP-7793) for Glamsterdam FAQ
author: marchhill
date: "2025-12-18"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/conditional-transactions-eip-7793-for-glamsterdam-faq/27228
views: 177
likes: 5
posts_count: 12
---

# Conditional transactions (EIP-7793) for Glamsterdam FAQ

# Conditional Transactions (EIP-7793) for Amsterdam

## What is it?

Conditional transactions are a new transaction type that is only valid at a certain slot and index in a block. For instance, you could create a transaction that is valid only if it is included at the top of block (index 0). The primary motivation is more secure encrypted mempools.

## What is the point of encrypted mempools?

Encrypted mempools work by submitting a transaction to the chain in two phases. In slot A the user posts an encrypted transaction onchain, that is sequenced with other encrypted transactions. In slot A+1 the decryption key is revealed and all of the transactions are decrypted and included in the order they were sequenced in at the top of the block. This provide two benefits: frontrunning protection and censorship resistance.

Frontrunning is when someone else sees the contents of my transaction and includes their own transaction ahead of mine based on this information. For example if my transaction is a swap, someone can insert their own transaction first to make a profit at my expense. This is not possible with encrypted mempools: my transaction is encrypted when it is sequenced so does not leak information. Note that this is much stronger than slippage protection, which would simply limit how much I can be exploited by a frontrunner. This can also be used in other contexts, hiding my bid in an auction, or move in a strategy game.

It can also provide censorship resistance guarantees: when I submit my transaction in slot A the builder (or includers) do not know the contents of my transaction, so have no reason to censor it. In slot A+1 it becomes very difficult for the builder to censor my unencypted transaction, since the ciphertext is already on chain everyone can see that the builder is censoring, and they could be slashed within the encrypted mempool protocol (for example).

## Why include in Amsterdam?

Encrypted mempools can provide a big UX boost for users by preventing frontrunning, while strengthening the censorship resistance guarantees of the chain!

## What is the problem with encrypted mempools?

The problem that exists today is that in slot A+1, there is nothing to enforce that the builder actually includes the decrypted transactions in the sequenced order. This undermines everything, we have a list of encrypted transactions specifying their order, but the builder simply ignores it and reorders the transactions, frontrunning without consequence.

Conditional transactions partially solve this problem, using this new transaction type we can specify that a transaction is only valid at the top of the block, preventing the builder from inserting their own frontrunning transactions ahead of the decrypted ones.

## How can it be used in practice?

Conditional transactions alone do not fully solve the problem with encrypted mempools, in practice they must be combined with batched transactions (eg. with EIP-4337).

Without transaction batching we have a problem: if my encrypted transaction is sequenced to be at index 3, I can create a conditional transaction that forces it to be included at index 3. However, what if the builder does include my transaction at index 3, but replaces the transaction at index 2 with their own frontrunning transaction?

This is why batching is needed, all of the decrypted transactions are batched into one single onchain transaction. This allows for smart account code to internally check that the transactions are the ones that are expected, and they are in the correct order. This batched transaction can then be conditional on being included at index 0. If the batched transaction grows too large, it can be split into multiple conditional transactions.

This means we need a batcher, an untrusted entity who bundles all of the decrypted transactions together and submits them to a (trusted) smart contract to verify and execute.

## Why is it designed in this way?

Conditional transactions require the desired index and slot to be specified upfront as a field in the transaction. This means that block building is not significantly complicated, the builder can immediately tell where the conditional transactions needs to be included.

The EIP also includes an opcode that returns the transaction index onchain when executed in a conditional transaction. This allows a users smart account to check that the index is correct without needing to trust the batcher.

## Isn’t top of block too valuable to be used this way?

The top of the block is valuable due to the opportunity to extract MEV. Since transactions from the encrypted mempool go through an extra slot of latency to reach the chain, they don’t gain this same advantage to extract MEV first. Effectively the new top of block from an MEV perspective, is the first transaction after those from the encrypted mempool.

## Are there other applications?

Another potential application of conditional transactions is [Ultra tx](https://ethresear.ch/t/ultra-tx-programmable-blocks-one-transaction-is-all-you-need-for-a-unified-and-extendable-ethereum/21673), as this proposes batching many transactions into one that must be posted at the top of block.

## Replies

**Helkomine** (2025-12-18):

This transaction format includes blobs, making it overly specific. I think a similar approach to EIP-7702 should be adopted, as it inherits type 2 instead of 3. Because our primary customer base consists of regular users, transaction type 2 will be more widely used.  Please criticize me if I’m wrong.

---

**marchhill** (2025-12-19):

Hey thanks for the feedback. We designed the transaction type in a way that it can be flexible, allowing for blobs to be optionally included. This is open to be changed, but it seems more future-proof to allow conditional transactions to be used in this way (for example this aligns better with Ultra tx)

---

**Helkomine** (2025-12-19):

Thanks for your feedback. Are you planning to integrate the authorization_list to support atomic transactions?

---

**MariusVanDerWijden** (2026-01-05):

Adding transactions that can only be valid at a specific index and block will make mining infinitely more complex. Sequencing transactions is inherently np and we only get around it by having decent heuristics. This change will break all of those heuristics and will dump a lot of additional complexity on client maintainers.

Also if the transaction is becoming invalid, will a block that includes it at a wrong index be invalid? I am wondering how the security section of this EIP can just say “none”.

---

**fab-10** (2026-01-07):

I am still understanding the use case, so I can miss something, but since a rational builder should include at the top of the block the most valuable tx, regardless if it is or not conditional, so to work well the conditional tx should also be the one paying more or otherwise the builder should be smart enough to understand that even if it is not paying more, there is enough space in the block to fit all the other txs that are paying more fee and the conditional one as first, and one (but inefficient) way to do it is to build the block twice and choose the one with the higher value for the builder.

It is also true that with a base fee market, unless there is a long strike of full blocks, in general when building a block there is enough space for all the executable txs currently in the pool. But if the block will be full or not is not known in advance, so for example if the first attempt put the conditional txs first, and the block is not full, then there is no need for the second attempt, unless is more convenient for the builder to include the conditional tx when it reverts.

---

**marchhill** (2026-01-08):

The way we designed this EIP is to not add too much complexity to block building. The desired tx index is specified upfront in the body of the transaction rather than in the bytecode, so we can sequence conditional transactions before other transactions in the block. For example we might have conditional transactions at index 0, 1, 2, so we can lock those in place and sequence the rest of the block.

I agree this would require some changes to block building code, but generally nothing major and I don’t think this should prevent us from adding protocol features. Since the building aspect is non-consensus, it doesn’t have to be implemented by the fork, builders could just ignore conditional transactions in the meantime (missing out on extra tips).

The main application for conditional transactions is out-of-protocol encrypted mempools. In this context the builder has opted-in to including EM transactions at top of block (with rewards and penalties out-of-protocol). The block building logic is very simple in this case (include specific conditional transactions at top of block, build the rest), and it would be implemented in a block building plugin for the EM that not all clients need to support.

For block builders not opted-in to the EM protocol, they could ignore conditional transactions altogether. Alternatively they could employ some simple heuristic:

`for (int i = 0; ; i++)`

`  txs = get_cond_txs_with_index(i)`

`  if (txs is empty)`

`    break`

`  selected_tx = txs.get_highest_paying_tip()`

`  add_to_block(selected_tx)`

`build_block_from_index(i)`

Generally we expect all of the conditional transactions to be sequential with no gaps (there would be no point as it wouldn’t provide frontrunning protection), so we ignore the rest once we reach a gap. The builder could try this, and compare with the profit from building the block with no conditional transactions.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mariusvanderwijden/48/1374_2.png) MariusVanDerWijden:

> Also if the transaction is becoming invalid, will a block that includes it at a wrong index be invalid? I am wondering how the security section of this EIP can just say “none”.

Yes if a conditional transaction is included at the wrong index it will be invalid, which would also mean that a block including it would be invalid. Are there any specific security concerns you have?

---

**marchhill** (2026-01-08):

No there are no plans to support authorisation lists. Could you expand a bit more on what you think the application would be and what atomic transactions are?

---

**fab-10** (2026-01-08):

So most of the design is out-of-protocol, but `TXINDEX` is needed to prevent the execution, of the conditional tx, in case a builder is cheating, because even if you can penalize the builder out-of-protocol, there is no other way to prevent the execution and the builder could prefer the penalization if for it is more convenient to front-run the conditional tx.

About the block building, probably vanilla execution clients will not by default implement the EM protocol, like they did with MEV, but they could optionally do, even if I imagine that, in the main use case for conditional txs, we will not see them broadcast in the public txpool, but only between the actors that will join the EM protocol, is that assumption correct?

---

**Helkomine** (2026-01-09):

An ERC-4337 transaction may include additional authorization sets to place code on the sponsored EOA and then perform atomic interactions such as batch transactions. Without adding the `authorization_list` field, the sponsor would have to split the transaction into two: one for set code and another for a conditional transaction afterward. This could be a bit inconvenient.

---

**fab-10** (2026-01-09):

I think the EIP should also evaluate the possible impact, also in term of security, to the transaction pool, since conditional transactions should be managed in a way so that a malicious actor could not pollute the pool with txs that are not executable and force a DoS.

For example sending a ton of conditional txs with the same slot and index, knowing that only one of them could be included in a block, thus consuming a lot of space and evicting other txs or preventing other legitimate txs to be accepted.

---

**Madeindreams** (2026-01-10):

I like the direction of encrypted transactions and conditional inclusion, but I’m trying to better understand the trust boundaries around *who* is responsible for encryption and *when* it happens.

In most practical deployments today, encryption would occur at the wallet / connector / RPC layer before submission. That raises an important question:

**what prevents connectors or RPC providers from inspecting, fingerprinting, or correlating transactions *before* they are encrypted?**

Even if the payload is encrypted on-chain, a connector that sees the raw transaction first could still:

- Observe intent before encryption
- Correlate wallet behavior and timing
- Decide whether to forward or withhold the encrypted transaction

This seems to leave open a failure mode where an actor with access to pre-encryption data could:

- Attempt to frontrun via alternative channels, and
- If unsuccessful, simply choose not to include or relay the transaction at all (a “fail-safe” censorship / option-value mechanism)

In other words, encryption protects against *post-submission* manipulation by builders, but may not fully address *pre-submission* leakage or selective inclusion by intermediaries.

Is the expectation that encrypted mempools are only safe if combined with strong guarantees around wallet / connector behavior (e.g. minimal metadata leakage, no inspection, decentralized encryption relays)?

Or is this considered an acceptable trust assumption for the initial design?

I’d appreciate clarification on how this part of the threat model is viewed.

