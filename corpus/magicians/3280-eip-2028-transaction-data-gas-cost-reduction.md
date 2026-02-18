---
source: magicians
topic_id: 3280
title: "EIP-2028: Transaction data gas cost reduction"
author: TomBrand
date: "2019-05-15"
category: EIPs
tags: [gas, eip-2028]
url: https://ethereum-magicians.org/t/eip-2028-transaction-data-gas-cost-reduction/3280
views: 20059
likes: 34
posts_count: 36
---

# EIP-2028: Transaction data gas cost reduction

This is to discuss the EIP I am currently creating. Will fill this out later

https://eips.ethereum.org/EIPS/eip-2028

## Replies

**axic** (2019-05-17):

> The gas per non-zero byte is reduced from 68 to TBD. Gas cost of zero bytes is unchanged.

This EIP proposes a change to the cost of CALLDATA but doesn’t specify the new cost. It proposes a model with certain parameters to be considered when coming up with the new value.

I think there should be some kind of initial ballpark figure given to kick start discussions. Is it a 10% reduction? Is it a 50% reduction? A 90% reduction?

Or at least giving a ballpark figure for a time/effort needed to do the simulation using the models. Is this work feasible within the Istanbul timeline?

---

**jochem-brouwer** (2019-05-18):

I’d like to know how the gas costs for `TXZERODATA` and `TXNONZERODATA` were choosen in the first place. Why is there a difference in cost for zeros and non zeros?

If I would want to send a boolean (0x00 or 0x01) to the chain it would be cheaper to encode 0x01 as 0x0000. This seems weird to me.

For costs itself I don’t see why there should be a difference in data aswell. To me it seems that the data gets included (in the end) in one of the block hashes (**transactionRoot**?) but then it makes no sense to me why nonzero data has different cost. Storing this data would also make no difference to me? Unless I’m missing some trivial trick which you can do with this data. I’d like to learn why the cost is different in the end =)

---

**PhABC** (2019-06-02):

To echo [@axic](/u/axic), do we have a rough estimate of what the new cost per byte could be?

An estimate value would help me figure out if I should go or not for a more complicated architecture using much less storage.

---

**elibensasson** (2019-06-03):

We don’t know yet by how much, we need to collect data and extrapolate the impact of reduced gas cost on things like uncle rate. We’ll definitely have a new estimate by time for Istanbul and we’ll support it with some data (now being collected). We’ll also discuss this matter at Scaling Ethereum this week.

---

**axic** (2019-06-23):

Was there any progress made on this? I’d be curious to see some results, so that it can be seriously considered for Istanbul.

---

**elibensasson** (2019-06-28):

Yes, we’re working on this diligently, on track for the July 19th deadline, will update ASAP when we have preliminary results but we’re optimistic that gas can be safely reduced.

(Louis answered this along these lines yesterday but his membership in this thread is pending so this comment will likely be repeated in other words by him.)

---

**guthlStarkware** (2019-06-28):

We are actively working and are on track for the deadline of July 19th.

We are currently running a simulated network in a controlled environment where tried various numbers for the call data gas cost and measure their effect on network security and open access (aka syncing time).

So far, our preliminary results are positive and points toward a large reduction.

We hope to share preliminary results as soon as we have them.

---

**jpitts** (2019-06-28):

Ok I see it, just approved this post by [@guthlStarkware](/u/guthlstarkware) (flagged by Discourse for some reason). Perhaps it was “preliminary results” that seemed too business-like for the spam filter LOL.

---

**shemnon** (2019-06-28):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/e/74df32/48.png) elibensasson:

> Yes, we’re working on this diligently, on track for the July 19th deadline,

July 19 is the deadline for clients to have EIPs implemented, not for the EIP to be complete.  I know this is water under the bridge and an audible was called but the intent was that the May deadline was when this data should have been available.

How much sooner than 19 July can this data be made available?

---

**guthlStarkware** (2019-06-28):

Hahaha I will know better next time ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**elibensasson** (2019-06-30):

Later this week we’ll share what we currently have, and will keep doing so as data emerges from the various simulations.

---

**guthlStarkware** (2019-07-04):

Disclaimer: I cannot post more than two links per post as a new user, therefore the multiple posts.

## EIP-2028 Standalone Analysis

TL;DR - We present our simulation plan and explain why we focus only on network delay and history. The plan is available [here](https://notes.whiteblock.io/s/SkV_SEYlB)

#### Introduction

When EIP-2028 was introduced, we discussed two kinds of test-cases:

(1) measuring network effects of increased calldata

(2) measuring local effects on a single node.

Here’s a brief update on both cases. For item (1), we collect data from Ethereum’s mainnet. We shall report our preliminary findings early next week.

To corroborate our findings, we’ve partnered with WhiteBlock to simulate the effect of reducing calldata gas cost and increased block size on important parameters such as network delays, and uncle rate. Our simulation plan is available [here](https://notes.whiteblock.io/s/SkV_SEYlB) and is already running.

---

**guthlStarkware** (2019-07-04):

The rest of this post discusses (2), the effects on a single node. The purpose of this analysis is to understand how calldata was priced at the network launch.

#### Update on Local Tests (Standalone Node) and Gas Cost Comparison

The main goal of performing local tests is to understand how the decrease in calldata gas cost would impact the system, assuming the network has zero delay (the effect on network delays is investigated separately). Recall that each node must validate the header of each new block and then, process the block. We want to ensure that the implementation of this EIP does not harm the network: for example, that the mere increase in blocksize does not cause significant problems in computing block headers and increase processing time, even if we assume zero network delays.

Recall that the current cost for calldata is 68 gas for each non-zero byte and 4 gas for each zero byte.

An increase in headers validation would impact security whereas an increase in block processing, all other things being equal, would impact throughput.

A quick gas comparison is interesting here:

When a validator receives a block, it computes the Keccak hash of the whole block to verify that the header used for the PoW is correct.

For a calldata input of size N bytes, if this verification operations were done in the EVM, the gas cost would be 30 gas for the first invocation of keccak and 6 gas for each additional word (32 bytes), totaling 30+6 * N / 32 gas. Asymptotically (neglecting the first 30 gas) this gives a gas price of roughly 6 for every 32 bytes, or 0.2 gas per byte. So, under current pricing, transmission and history for nonzero bytes accounts for all 68 gas.

One could argue that Keccak might be underpriced too. This is debunked by [Holiman vm analysis](https://github.com/holiman/vmstats), based on a historical analysis of opcode runtime over Ethereum lifetime. According to this work, the Keccak opcode’s gas price is on par with its processing time.

Our local measurements on our machine go along with this analysis.

So far, we compared calldata to computation cost. One could also try to compare calldata and storage. We tried but failed to find similar analogies there. This goes along with several other reports on SLOAD and SSTORE, stating that their pricing is complex and must be understood as a design choice for the network future [1](https://github.com/renlord/bookish-octo-barnacle/blob/master/slides.pdf)

To conclude, assuming zero network delay, the fair and consistent pricing of calldata has a lower bound at 0.2 gas per byte. Practically, this means that the new gas cost recommendation should be based on its effects on network delay and history. This is also what was done in the original system design.

---

**axic** (2019-07-05):

This was pointed out by [@AlexeyAkhunov](/u/alexeyakhunov) on today’s ACD: this EIP only tries to change the txdata cost and not the cost for CALLs between contracts.

Would it make sense changing the title of this EIP to “Transaction data gas cost reduction”?

---

**chfast** (2019-07-05):

1. Can you rename to something like `“Transaction data gas cost reduction”.
2. Can you also run simulations for the case where the same cost for zero and non-zero bytes?

---

**guthlStarkware** (2019-07-05):

It would make sense, the new title being self-explanatory.

Where do we need to change it?

---

**guthlStarkware** (2019-07-05):

Let me discuss it with WhiteBlock.

On a side note, I’m still looking a good reason for the distinction in the first place and would be pleased to discuss it.

---

**axic** (2019-07-05):

File a PR changing the EIP, it should be merged automatically. Please also update the title of this forum topic, if it won’t allow it for you, [@jpitts](/u/jpitts) can help.

---

**chfast** (2019-07-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/guthlstarkware/48/2064_2.png) guthlStarkware:

> On a side note, I’m still looking a good reason for the distinction in the first place and would be pleased to discuss it.

I believe the reasoning for pricing zero bytes differently was that they might be compressed easier. But considering that these numbers do not closely reflect CPU times, it was rather premature optimization.

If there is a chance to simplify this with this EIP I’d go for it.

---

**TomBrand** (2019-07-05):

[@axic](/u/axic) [@chfast](/u/chfast) good suggestion - changed it. Thank you


*(15 more replies not shown)*
