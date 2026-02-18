---
source: magicians
topic_id: 6287
title: Some medium-term dust cleanup ideas
author: vbuterin
date: "2021-05-20"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/some-medium-term-dust-cleanup-ideas/6287
views: 5385
likes: 7
posts_count: 3
---

# Some medium-term dust cleanup ideas

Currently, transaction fees on the Ethereum chain are high, and there are many accounts that have meaningful amounts of money (eg. $1-10) that are now effectively stuck because the transaction fees to move them are too high. Even moving the funds into a rollup is infeasible: depositing into rollups takes more than the 21,000 gas needed to send funds (at least 50,000). Ethereum’s current scaling roadmap is [L2-focused](https://ethereum-magicians.org/t/a-rollup-centric-ethereum-roadmap/4698), and while this *will* lead to low fees *inside* layer 2 protocols on top of Ethereum, it does not help users with small amounts of existing funds move over.

This post describes some longer-term ideas for allowing at least some small-balance accounts to clear out their balances. The ideas are focused around the assumption that many users will want to withdraw these balances directly into L2 protocols such as rollups, but there is no globally accepted single rollup and so the solution will have to support migration to arbitrary addresses (but most people will only send to a few major addresses).

### Why do txs cost 21000 gas?

To understand how special-purpose cheap withdrawals could be done, it helps first to understand what goes into the 21000 gas in a tx. The cost of processing a tx includes:

- Two account writes (a balance-editing CALL normally costs 9000 gas)
- A signature verification (compare: the ECDSA precompile costs 3000 gas)
- The transaction data (~100 bytes, so 1600 gas, though originally it cost 6800)

Some more gas was tacked on to account for transaction-specific overhead, bringing the total to 21000.

**[EDIT 2021.05.29: much of the section on EIP 3074 that was here before is wrong, because EIP 3074 does not allow balance transfers out of accounts). The content below was editng ted to account for this; thanks to @lightclient for pointing this out]**

### Special-purpose multi-extraction with SNARKs

We could imagine an EIP-3074-like opcode that allows a large number of accounts to be emptied, taking as input some kind of aggregated signature that proves that all accounts authorized the operation. To preserve the invariant that editing storage must cost at least 5000 gas, this opcode would have to cost 5000 gas per account (plus 320 gas for the call data to specify the accounts), and it would sweep the funds into one destination address. This can be done with a call that provides the list of accounts and balances as call data, to facilitate sweeping into trustless rollups.

To ensure mempool safety, the opcode should also require a *maximum ETH balance* in the account: it should not be possible to empty the account with a regular transaction. Alternatively, this could be done as a transaction type instead of an opcode, which would remove this requirement.

A major challenge with this scheme is that SNARK verification has a high constant overhead, so this would only make sense for large batches (100+ signatures).

### Multi-extraction with Schnorr

An alternative to using SNARKs is to use [Schnorr multi-signatures](https://hackernoon.com/a-brief-intro-to-bitcoin-schnorr-multi-signatures-b9ef052374c5). This would require passing in N *public keys* as input, hashing each key to find the address to be authorized, and verifying the provided signature against the set of keys.

This would cost 5000 gas for state editing plus 480 gas per public key and ~500 gas for EC point unpacking. The fixed overhead is small, making it suitable for small batches.  Note that the multi-signatures would have to be coordinated off-chain (it’s a 2-round protocol with an interaction step in the middle). This likely makes it non-viable for large batches (more than a few dozen participants).

### Force transfer into a minimal withdraw-only rollup

To avoid the need for state storage access, we would need to take more extreme steps: essentially, migrating small balances (eg. anything under 0.005 ETH) from the state into a special-purpose accumulator. This is best done after the [state expiry](https://hackmd.io/@vbuterin/state_expiry_paths) roadmap is complete and we are in epoch 1, as then the epoch 0 state will be static and large-scale manipulations like this will be easier (because they can be computed off-chain and there’s no interference from a constantly-mutating state tree).

This accumulator would maintain a state root, which would contain the public keys and balances of every participant. Users can make a multi-withdrawal by signing a message, and an aggregator can make a transaction giving a recipient, the indices of accounts participating, and a ZK-SNARK proving that signatures authorizing the withdrawals exist. The SNARK would also prove the correctness of the updated state root.

This could reduce per-user overhead to as little as 64 gas: 4 bytes for which *index* in the list of public keys and balances is cleaned out. In practice, however, it may be advisable to add another 20 bytes (320 gas) for each user’s address, so that the addresses can be concatenated and put into txdata so that the rollup will know how to update the balances.

### Recap

- Today, clearing an account costs 21000 gas ($5.25 assuming $2500 ETH and 100 gwei)
- EIP 3074 with no modifications will reduce that to ~14000 gas, though some off-chain batching will be required ($3.50)
- Witness gas cost changes could reduce that to ~10000 gas ($2.5)
- A fancy EIP 3074 alternative that takes Schnorr signatures or SNARKs could reduce that to ~6500 gas ($1.62)
- A much more invasive strategy that could be done after state expiry is implemented and we are in epoch 1 could reduce that to ~64-600 gas ($0.01-0.16), or basically the same cost as a transfer inside a rollup

### My thoughts

- If we implement EIP 3074, then adding witness gas cost changes is a no-brainer. This already lets us have 2x cheaper withdrawals
- Fancy versions of EIP 3074 are probably not worth implementing. I already have some concerns about EIP 3074, particularly its forward-compatibility with a desired future world where accounts are fully abstracted and EOAs are abolished entirely (would AUTH and AUTHCALL then just become calls to the default contract account? More thinking would be desired). These issues don’t outweigh EIP 3074’s amazing benefits, but they do outweigh the benefits of making a significantly more complicated special-purpose EIP 3074 just to make mass movement of funds a little bit cheaper.
- The much more invasive strategy is the most powerful, but it’s invasive, and it’s only realistically implementable post-state-expiry once we are in epoch 1, so the pre-epoch-1 state tree is static. Additionally, it’s probably a bad idea to redirect effort toward this problem while more pressing issues such as the merge and state expiry need all our attention. So we should probably just delay thinking about this for at least a year.

## Replies

**Shymaa-Arafat** (2021-05-26):

I’m postponing any thinking or brainstorming about this too, and probably u do know about Cardano, but just as a cautionary step I thought u should know that they addressed the dust problem. I always believe it’s useful to be aware of others ideas, the pros&cons, what is suitable for ur system,…etc.

.

In

https://emurgo.io/blog/understanding-unspent-transaction-outputs-in-cardano

"Dust

Dust is the term for when small UTxOs gather in a user’s wallet over time. These UTxOs are so small that it costs more in transaction fees than they are worth to send over the network. The distribution of these UTxOs depends upon the underlying coin selection algorithm used by the wallet. Sebastien Guillemot has extensively covered the effects that different coin selection algorithms have on creating dust. If you are interested, you can watch his video or refer to the blog post that he reviews, which is originally based on the formal wallet specification paper.

He highlights a number of interesting points, two of which stand out: by choosing a coin selection algorithm that keeps transaction amounts and change amounts close to 1:1 you maximize the pseudo-anonymity of the transactions, because it is harder for people to identify who is actually receiving a cryptocurrency payment and who is receiving the change. The second point is that the coin selection algorithm may not matter all that much for individual wallets, but for an exchange it can have serious efficiency consequences."

.

I fastly scanned the paper, but haven’t read the blog or watched the video.

---

**Ferns** (2021-05-26):

Pricing out small players will absolutely hurt Ethereum in the long run.

Lowering L1 fees can also minimize damage to said users given MEV proliferation.

Unlikely to eat up L2 given that L2 is where trading bots have more market leverage in the medium term.

