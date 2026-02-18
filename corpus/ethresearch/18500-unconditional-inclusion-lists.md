---
source: ethresearch
topic_id: 18500
title: Unconditional inclusion lists
author: mikeneuder
date: "2024-01-30"
category: Proof-of-Stake > Block proposer
tags: [censorship-resistance]
url: https://ethresear.ch/t/unconditional-inclusion-lists/18500
views: 6067
likes: 69
posts_count: 39
---

# Unconditional inclusion lists

# Unconditional inclusion lists

[![upload_d8336517ff27bb713b162aea8e862611](https://ethresear.ch/uploads/default/optimized/2X/d/d6fe238dfb55e13146a0b91b64a514c48122f44d_2_476x400.jpeg)upload_d8336517ff27bb713b162aea8e8626112648×2220 258 KB](https://ethresear.ch/uploads/default/d6fe238dfb55e13146a0b91b64a514c48122f44d)

^lol

\cdot

*by [mike](https://twitter.com/mikeneuder) & [toni](https://twitter.com/nero_eth) based on discussions with [potuz](https://twitter.com/potuz1) & [terence](https://twitter.com/terencechain)*

\cdot

*tuesday – january 30, 2024*

\cdot

***tl;dr;*** *Inclusion lists return agency to the proposer in a PBS world by allowing them to express preferences over the transactions included onchain, despite outsourcing their block production to the specialized builder market. This document discretizes the inclusion list design, advocates for a specific feature set, and aims to justify these decisions based on an analysis of the tradeoffs.*

\cdot

***Acks***

*Many thanks to [Roman](https://twitter.com/r_krasiuk), [Dan](https://twitter.com/Rjected), [Barnabé](https://twitter.com/barnabemonnot), [Francesco](https://twitter.com/fradamt), [Julian](https://twitter.com/_julianma), [Thomas](https://twitter.com/soispoke), [Stokes](https://twitter.com/ralexstokes), [Hsiao-Wei](https://twitter.com/icebearhww), [Justin](https://twitter.com/drakefjustin), [Vitalik](https://twitter.com/vitalikbuterin), & [Mikhail](https://twitter.com/mkalinin2) for thoughtful comments and reviews!*

\cdot

***Related work***

| Article | Description |
| --- | --- |
| No free lunch | research post |
| IL eip | eip |
| censorship.pics | toni’s dashboard |
| Spec’ing out ILs | terence’s research post |
| Non-expiring inclusion lists | toni’s research post |
| draft spec pr | hsiao-wei’s draft CL spec change |

---

### High-level summary

**We advocate for unconditional inclusion lists.** The two-slot process is:

1. The slot n proposer builds an inclusion list published alongside their block.
2. The transactions in the inclusion list are either:
a) included in the slot n execution payload,
b) included in the slot n+1 execution payload, or
c) appended (in order) to the end of the slot n+1 execution payload.
3. The validity of the slot n+1 block depends on the existence and satisfaction of a signed inclusion list summary.

The following figure demonstrates this process.

[![upload_9e2c321a76fd4bf927abb937e65284e4|522x500,](https://ethresear.ch/uploads/default/optimized/2X/d/d13e0e4550ac6d8037eff026875129ba99c78dbc_2_522x500.png)upload_9e2c321a76fd4bf927abb937e65284e4|522x500,1463×1401 275 KB](https://ethresear.ch/uploads/default/d13e0e4550ac6d8037eff026875129ba99c78dbc)

Note that this is slightly different than the original proposal in [“No free lunch”](https://ethresear.ch/t/no-free-lunch-a-new-inclusion-list-design/16389), in which transaction inclusion is conditioned on sufficient gas remaining in the `slot n+1` block. Instead, the unconditional IL acts as a “block extension” appended to the `slot n+1` payload. The figure below shows the transaction order that results from this design:

[![upload_b0e3599e2c43335cb956bdde3a4b75af-1](https://ethresear.ch/uploads/default/optimized/2X/c/cbd1c5da2dfed2f654010529b134661caff2fdac_2_317x500.png)upload_b0e3599e2c43335cb956bdde3a4b75af-1461×727 37.3 KB](https://ethresear.ch/uploads/default/cbd1c5da2dfed2f654010529b134661caff2fdac)

While unconditional ILs require a selection for the “inclusion list gas limit”, this value is not the focus of this document. The remainder of this document aims to justify the other elements of this design.

---

### Core design philosophy.

**The “forward” property** – This property dictates the enforcement of the `slot n` inclusion list during `slot n+1`. This has been a core desideratum in inclusion list designs since Francesco [published the idea](https://notes.ethereum.org/@fradamt/forward-inclusion-lists) at the end of 2022. The forward property provides incentive compatibility because the `slot n` proposer can safely construct an IL with the knowledge that the value of their block will be unimpacted by the IL.

**The “unconditional” property** – This property ensures that once an IL includes a transaction, that transaction is guaranteed to go onchain at the latest in the subsequent slot (unless another transaction with the same nonce from the same address takes its place, see [here](https://ethresear.ch/t/no-free-lunch-a-new-inclusion-list-design/16389#how-does-that-solve-the-free-da-problem-6) for the details).

**The “bottom-of-next-block” property** – This property enforces any `slot n` IL transactions not in the main body of either the `slot n` or `slot n+1` payloads must be included at the end of the `slot n+1` payload. Note that these transactions could also be included ~at the top~ of the `slot n+1` block. The top-of-block vs bottom-of-block remains one of the main sticking points in design discussion; we highlight the tradeoffs below.

**The “ordered” property** – This property mandates any `slot n` IL transactions not in the main body of either the `slot n` or `slot n+1` payloads must be included in the order at the bottom of the `slot n+1` payload. In other words, any IL transactions occupying the “bottom-of-next-block” must appear in the same order as the IL.

By separating these four criteria we independently address the natural questions that arise from each. We skip the “forward” property because it is discussed elsewhere ad nauseam.

***[unconditional property] How should inclusion list enforcement be handled?***

- The enforcement of the IL depends on how you view the IL object in the context of the main block body. The two ideas below capture the difference:

The slot n IL extends the slot n+1 block. (unconditional) The IL has a fixed gas limit and the execution of the transactions occurs if they are not in the slot n payload. These transactions consume the IL gas (as opposed to the slot n+1 30mm gas limit). (Note that viewing unconditional IL transactions as an extension of the gas limit of a block could equivalently be seen as a reduction of the gas limit of a block if the transactions are force-included even if the block is full.)
- The slot n IL constrains the slot n+1 block. (conditional) In this case, the IL does not have any extra gas beyond the 30mm contained in the payload, thus conditioning the enforcement of the IL transactions on the existence of extra unused gas in the slot n+1 payload.

***[unconditional property] What are the tradeoffs between unconditional and conditional ILs?***

- Pros of unconditional ILs

The IL transactions are guaranteed to be included in the next block, no matter what the payload contains. Because the IL serves as an extension of the gas limit of the block, we have maximally strong assurances about transaction inclusion.

Cons of unconditional ILs

- The IL becomes a de-facto block size increase, which could induce an external market for IL construction. During periods of high demand for block space, getting included in the IL may be extremely valuable, making MEV over the IL relevant.

Pros of conditional ILs

- The IL provides no strict guarantees and is less MEV-able. This is the inverse of the previous point. When the IL transactions are only conditioned on the block having remaining gas, there is much less value gained from getting included in the IL during high congestion periods. However, because of EIP-1559, blocks are not regularly full (only 11690 / 432970 \approx 2.7\% of blocks contain >29mm gas over the last 3 months), so this may not significantly change the demand for IL inclusion.

Cons of conditional ILs

- The transaction inclusion guarantees are weaker because the ILs are conditional. As a result, a censoring builder might choose to fill the block with irrational transactions to avoid using the IL (see Barnabé’s post Fun and Games for the description of “block stuffing”). With conditional guarantees, multiple proposers may have to include the transaction in the IL before the transaction is included in a block (e.g. if the first block is full).

***[bottom-of-next-block property] Why include the IL transactions at the bottom of the `slot n+1` payload (as a suffix) instead of at the top (as a prefix)?***

- The top-of-block positioning is valuable. Consider the case where an NFT mint starts at slot n+1. MEV searchers who want to be the first to mint the NFT can guarantee this privilege by bribing the slot n proposer to construct an IL with their transactions in it. This may induce a marketplace (similar to mev-boost) for proposers to auction off the right to construct an IL for their slot. Externalization of the IL is not desirable because we want the validators to construct their ILs based on their local view of the mempool to preserve the censorship resistance benefits of having a decentralized validator set. With the IL transactions at the end of the slot n+1 payload, these transactions have no guarantees beyond inclusion. The downside is that IL transactions may be arbitrarily front-ran by transactions in the slot n+1 payload. However, this doesn’t significantly change the semantics of getting in an IL because even in the slot n+1 top-of-block version, IL transactions can still be indiscriminately frontran by transactions in the slot n payload.

***[bottom-of-next-block property] Is there a situation where the guarantee of being included in the end-of-block for `slot n+1` is valuable?***

- We don’t think so; consider the reframing of the question: “Is there value in having an arbitrarily ‘frontrunable’ end-of-block transaction?”  Both the slot n and slot n+1 builders can arbitrarily insert transactions at the end of their block to exploit the IL transactions. In that regard, these transactions don’t have any guarantees about the post-state of slot n+1. Further, they must be broadcast by t=4 in slot n, meaning they have no latency advantage over just being included in the slot n or slot n+1 payloads directly.

***[ordered property] Why do the transactions in the IL get inserted in order?***

- Great question, simple answer: there does not seem to be any reason to allow their reordering. Preserving the IL ordering simplifies the implementation (de-duplicate the IL \rightarrow linearly scan) and reduces the control the slot n+1 builder can exert over the slot n IL.

---

### Inclusion list usage considerations.

***How do we know that proposers will use inclusion lists?***

- We don’t know. As with the rest of the validator specification, we rely on honest participants to run one of the default client implementations. These defaults will construct the IL before proposing their blocks. Some users may choose to modify their client software to behave differently. On a higher level, we are asking: “Who do we want to depend on for censorship resistance of the protocol?” The status quo depends on builders who have total autonomy over what transactions end up in the block; this has obvious downsides as the builders are a small set of doxed actors. ILs allow validators to reclaim some agency over their block space and bring the censorship resistance properties back to the validator set, which we assume to be more decentralized and much longer-tailed than the builders. One amazing feature of inclusion lists is that they don’t rely on an “honest majority” assumption; even a small minority (e.g., 5% of validators) using ILs greatly hardens the protocol censorship resistance (though we would hope for a higher adoption rate of course).

***How do ILs interact with self-building?***

- ILs do not change the process of self-building a block. When the self-building proposer receives the previous block over the network, an IL accompanies it. The self-building proposer inserts the transactions in the IL as the suffix to their block (they could also just as easily include the transactions in the main block body). Most commonly, the self-building proposer will have an empty inclusion list for the subsequent slot because they will include all visible transactions in their block. If the self-built block is full, they can fill their IL with the next highest-paying transactions (greedy).

***How could we incentivize inclusion list usage?***

- To make the IL usage more meaningful, we may consider simple options to incentivize validators to opt in. For example, if we encourage validators to put all the transactions they see into an IL (in effect constructing a locally built block), we could reward them through the tips of all the included transactions (even if the transaction inclusions are in the subsequent slot payload). While we think this would increase IL usage generally, validators could still choose to exclude a small subset of transactions they want to censor without sacrificing much in terms of priority fees. Thus it is not clear that this would meaningfully improve the censorship resistance of the protocol. We advocate for starting with unincentivized ILs and only consider incentivizing them in the future if initial adoption is insufficient and more data is available.

***Are there legal concerns with IL usage?***

- This is not legal advice; I am not a lawyer. Some node operators may modify the client software to exclude a subset of transactions. Despite this ILs can ~only improve~ the censorship resistance of the protocol. Consider that right now, validators self-select into three groups.

Validators who connect to non-censoring relays/builders.
- Validators who *do not* connect to non-censoring relays/builders.
- Validators who self-build.
- With ILs, we now have four groups (assuming here that validators in group 2 above will not use ILs).
\;\; 1a. Validators who connect to non-censoring relays/builders and construct ILs.
\;\; 1b. Validators who connect to non-censoring relays/builders and *do not* construct ILs.
\;\; 2. Validators who *do not* connect to non-censoring relays/builders and *do not* construct ILs.
\;\; 3. Validators who self-build.
- Note that we get the improvement of censorship resistance from group (1a) above because even though those validators may end up proposing a censored block (e.g. if a censoring builder has the highest paying block), they produce an IL that will be enforced on the subsequent slot. Group (1b) continues to connect to non-censoring relays and builders, so they don’t increase the amount of censoring that they do, they just don’t contribute to the censorship resistance of the protocol because they don’t construct ILs.

---

### Additional design considerations.

***How large should the inclusion list be?***

- If we go for an unconditional inclusion list that acts as an extension to the gas limit of a block, we would need to choose the size of that limit accordingly. In the most congested periods, this will set an upper bound on the total gas limit of the block + IL pair. For example, an IL with 10mm gas would mean the total block could be 40mm, effectively raising the gas limit. We defer further discussion on the exact gas limit of the IL to future work.

***Should the inclusion lists be expiring or non-expiring?***

- An additional design axis to consider is if the inclusion list has an “expiration”. Expiration enforces that the IL enforcement occurs within some specified window of slots. For example, should an IL expire after just one slot, even the missed slot scenario, or should it be enforced on the next proposer regardless? A non-expiring design comes with the advantage of not allowing validators with subsequent proposers to deliberately miss the first slot if they prefer not to adhere to the IL to enforce their censorship. However, missing the slot intentionally to avoid IL conformance is a dramatic decision. In the current design by Potuz, the IL doesn’t expire and remains valid even after a missed slot. With a stricter approach to enforcement, we eliminate the possibility of intentionally missing the first of several consecutive slots to circumvent the IL. For a more detailed discussion on this topic, see the thread under this post.

***Should the inclusion lists be cumulative?***

- This design consideration only matters if we want proposers to be able to specify a certain number of slots in the future by which then the IL ~must~ be enforced. For example, a transaction that pays enough fees to be included in any of the next m blocks, even if the base fee rises continuously until then, could be put onto the IL with the deadline of m. This implies that the subsequent proposer is not obligated to adhere to the IL unless the deadline for inclusion is the current slot. A notable downside of this approach is that transaction inclusion may have to wait for a few more slots. The advantage of such a design is that it prevents certain games that entities with consecutive slots could play. For example, an entity with a 10% validator share has three consecutive slots ~7 times per day. This entity could leave the IL empty if the subsequent proposer is its own, but fill the IL if the subsequent proposer belongs to someone else. This strategy allows the entity to avoid constraining its proposers while continuing to impose constraints on others.

---

## Replies

**themandalore** (2024-01-30):

Awesome post!

I could see a scenario where you purposely fill the IL with as many low value transactions as you can to limit the rewards of other validators.  a) how do you ensure the IL transactions are paying the appropriate fee for a block (or could you just stuff it with 0 gas txns?)  or b) how do prevent just filling up the IL with useless things so other validators don’t have as much space to get MEV or higher value transactions?

Also, I saw Justin’s talk on splitting out the attester and proposer roles for MEV auctions.  Why not have attesters be in charge of the inclusion list since the proposer role in general seems to be centralizing like the builder one?

---

**Pintail** (2024-01-30):

Also love this! One thought: rather than have a separate IL gas limit, why not just subtract any excess gas consumed by IL transactions from the gas limit of block n+2? For the EIP-1559 basefee update the excess gas of block n+1 is then accounted for in the block n+2 basefee calculation and overall throughput is unaffected.

---

**pyggie** (2024-01-30):

Does the gas base fee rule also apply to transactions in the IL? If yes, what happens to transactions in the IL whose gas price is lower than the base fee for the block?

---

**Pintail** (2024-01-30):

They have to be dropped if they can’t afford the basefee otherwise getting into the IL would be a way of circumventing it.

---

**ChrisBender** (2024-01-31):

Interesting proposal! However, I’m a bit worried/confused as to how IL blockspace doesn’t just degenerate into the same market structure as “normal” blockspace.

Since inclusion in the IL is valuable and scarce, users will be paying gas in a standard first-price auction, no? What prevents a similar relayer-builder dynamic from forming on the extended IL blockspace? Why would validators not also opt-in to “IL-mev-boost”?

---

**The-CTra1n** (2024-01-31):

![](https://ethresear.ch/user_avatar/ethresear.ch/chrisbender/48/15050_2.png) ChrisBender:

> Interesting proposal! However, I’m a bit worried/confused as to how IL blockspace doesn’t just degenerate into the same market structure as “normal” blockspace.

That’s a valid concern.

Unconditional txs in a block N probably need to pay a premium compared to normal transactions in block N (and possibly also N+1). Something that normal transactions wouldn’t do. [Inclusion lists have the issue of handling the increase in gas from full block to full block](https://ethresear.ch/t/fun-and-games-with-inclusion-lists/16557#block-stuffing-in-forward-ils-2).

For example, by forcing IL txs to commit to double the current base-fee (plus some tip), the IL should be used pretty exclusively for txs needing CR. Normal users can still tip+correct current basefee, and risk getting in through the normal entrypoint.

In such a setup, a user needing CR in the presence of non-censoring proposers probably sends an IL tx and a non-IL tx (which can tip more due to lower basefee). If the proposer is censoring, we’re back to square 1… Maybe ILs can be enforced by non-proposer validators?

---

**Nero_eth** (2024-01-31):

![](https://ethresear.ch/user_avatar/ethresear.ch/themandalore/48/1652_2.png) themandalore:

> how do you ensure the IL transactions are paying the appropriate fee for a block

First, there is still the base fee which every transaction must be able to pay. You cannot go below the basefee. Otherwise the IL would be perceived invalid and your full block would turn invalid too. The end result is that you missed your slot for building an invalid IL.

Second, with “useless” you refer to low-gas transaction. This is not the case as the IL has it’s own gas limit.

The only concern could be that you put ofac transaction in it to constrain the next proposer by not having access to 4 out of the 5 largest builders bc they are censoring.

![](https://ethresear.ch/user_avatar/ethresear.ch/themandalore/48/1652_2.png) themandalore:

> Why not have attesters be in charge of the inclusion list since the proposer role in general seems to be centralizing like the builder one?

This is already the case. Validators are enforcing the IL by only attesting to blocks that obey the IL. If a builder builds a block that is invalid because e.g. it censors, then the relay wouldn’t even give that block to the validator because the relay would simulate the block and see that it’s invalid.

---

**Nero_eth** (2024-01-31):

They won’t be dropped because they should never reach the state in which they cannot be put into a block at the beginning.

Every IL in which there is a transaction that doesn’t `pay current_basefee + 12.5%` as `maxFeePerGas` is invalid from the beginning. Thus, the validator who built it shouldn’t have gotten the block on-chain as validators should perceive that block as invalid.

The 12.5 ensure that the transaction is valid even if the basefee increases and the transaction pays nothing in priority fees.

---

**Nero_eth** (2024-01-31):

I think this might make the whole thing little more complicated to implement and additionally adds this strange “attack” on the next proposer in which you fill the IL with non-mev/low priofee transactions to reduce the next’s profits. By allowing the IL to have it’s own limit, this cannot happen.

Would be actually interesting start discussing the size of the IL. It should accomodate large transactions (TC deposits/withdrawals of each 1m gas) but should also not end up raising the block gas limit by too much.

---

**Pintail** (2024-01-31):

I can see that the attack vector you describe is potentially a serious problem.

To me it seems that the introduction of a new protocol variable (an IL gas limit) represents significant unwelcome complexity. Is it really justified by the benefits relative to the ‘conditional IL’ approach?

---

**mikeneuder** (2024-01-31):

IMO yes! the unconditional property feels super important. [@pintail](/u/pintail) what you describe as “not increasing the gas limit but still requiring the transactions to be in the block” is effectively lowering the gas limit of that block, which IMO is two sides of the same coin. Using it as an extension rather than a reduction is more of an aesthetic choice, i think the unconditional property is the real design consideration that is worth aiming for.

This is what I was trying to get across with

> Note that viewing unconditional IL transactions as an extension of the gas limit of a block could equivalently be seen as a reduction of the gas limit of a block if the transactions are force-included even if the block is full.

Either way, these edge cases apply only when the blocks are full, which I think is rare enough to not worry about average case usage of ILs IMO.

---

**mikeneuder** (2024-01-31):

![](https://ethresear.ch/user_avatar/ethresear.ch/themandalore/48/1652_2.png) themandalore:

> Also, I saw Justin’s talk on splitting out the attester and proposer roles for MEV auctions. Why not have attesters be in charge of the inclusion list since the proposer role in general seems to be centralizing like the builder one?

Making the attesters in charge of CR would be great, but in practice i dont see how this works. the attesters would need to come to consensus over a set of transactions to include, which is a whole can of worms and seems data intensive (e.g., coming to consensus over a mempool is kinda a blockchain in its own right lol).

---

**themandalore** (2024-01-31):

Why not just give it to the aggregators? Another benefit of aggregating the most attestations. If there’s not enough room for all of them, make it a race so they do it faster too

---

**Milli3E** (2024-01-31):

Mulled this over for a bit and I kind of feel like this is a bit overkill for the current censorship landscape, especially considering the fact that it doesn’t change the root of the problem, which seems to be relay centralization.

The main reason for relay centralization atm isn’t due to MEV forces as we predict will be the case in a post PBS world, but instead it’s due to the lack of incentives for running a relay.

Once PBS is enshrined I’m assuming there will be some economic incentive to be a builder, and thus, there will naturally be more competition and better builder diversity as a result.

The root cause of censorship seems to be:

1. Validators jobs involve block construction (even though most run MEV boost) and in practice they have the ability to include and disclude txs as a result
2. There isn’t ant incentive to run a relay

After PBS validators won’t need to be concerned with block building and so in practice they will likely ignore the contents of the block and simply attest to the most profitable blocks. And once there is an incentive for builder diversity, competition will increase and naturally censorship will decrease as a result.

If ILs are enforced right now, there’s a good chance many validators (especially the staking pool operators) will ignore the new spec, and the relays (which are easily identifiable entities) will ignore it as well just as they currently are.

If a builder and validator were to respect the inclusion lists, then they would also likely process a block with those txs without inclusion lists anyway (assuming the base fee and priority fees are respected).

So I’m a little concerned that ILs don’t change much in practice and instead create a contentious environment on the chain and a culture of ignoring protocol spec (which isn’t the case right now) over something that isn’t egregious as of yet.

Atm it’s a validator’s prerogative to include or not include what ever txs they want and that’s also the case for Bitcoin miners. The protocol was designed to factor that in and maintain a fair degree of censorship resistance in light of that (which to this day, I’d say has been successful if not for the highly trusted and un-incentivized role of relays)

I think ILs would make a lot more sense if the volume of censorship was much greater,

ie) If builders were censoring transactions over $10k between “unverified” parties based on some jurisdictional restrictions or terms and conditions.

imo if the above example were to happen then inclusion lists would be 100% warranted and there would likely be enough of an incentive to service such a large market and certainly more relays would come online to fill that role, even before enshrined PBS.

I should note that this is just my humble observation and if any of the assumptions I’m making are incorrect (especially in regards to the root of the censorship issues or to the severity of censorship) I’d be happy to change my views ![:slightly_smiling_face:](https://ethresear.ch/images/emoji/facebook_messenger/slightly_smiling_face.png?v=12)

---

**ChrisBender** (2024-02-01):

Even if you have double base fee for IL blockspace, that does not change anything about the potential for “IL-MEV-boost”, since proposers will always make more money by getting their IL blocks from sophisticated builders, rather than the public mempool.

Unless I’m missing something, I see zero value-add with this CR proposal over the current status quo.

---

**MicahZoltu** (2024-02-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/mikeneuder/48/11832_2.png) mikeneuder:

> IMO yes! the unconditional property feels super important.

I would like to see this fleshed out more.  The original post correctly states the following, which makes it unclear where the big win from unconditional ILs lies.

![](https://ethresear.ch/user_avatar/ethresear.ch/mikeneuder/48/11832_2.png) mikeneuder:

> The IL provides no strict guarantees and is less MEV-able. This is the inverse of the previous point. When the IL transactions are only conditioned on the block having remaining gas, there is much less value gained from getting included in the IL during high congestion periods. However, because of EIP-1559, blocks are not regularly full (only 11690 / 432970 \approx 2.7%11690/432970≈2.7%11690 / 432970 \approx 2.7% of blocks contain >29mm gas over the last 3 months), so this may not significantly change the demand for IL inclusion.

The attack vector (block stuffing) mentioned in the original post (quoted below) requires builders pay extra to fill blocks, and every block they do this in a row gets exponentially more expensive, so censorship in this way even for a short time ends up costing a huge amount of money, which I suspect is sufficient disincentive to make the problem something that we can ignore.

![](https://ethresear.ch/user_avatar/ethresear.ch/mikeneuder/48/11832_2.png) mikeneuder:

> The transaction inclusion guarantees are weaker because the ILs are conditional. As a result, a censoring builder might choose to fill the block with irrational transactions to avoid using the IL (see Barnabé’s post Fun and Games  for the description of “block stuffing”). With conditional guarantees, multiple proposers may have to include the transaction in the IL before the transaction is included in a block (e.g. if the first block is full).

---

**mikeneuder** (2024-02-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> The attack vector (block stuffing) mentioned in the original post (quoted below) requires builders pay extra to fill blocks, and every block they do this in a row gets exponentially more expensive, so censorship in this way even for a short time ends up costing a huge amount of money, which I suspect is sufficient disincentive to make the problem something that we can ignore.

IMO the bigger issue is the fact that the builder will only need to stuff a single block to avoid the enforcement of the IL. e.g., if only 5% of blocks fill make use of the IL, the builder only has to stuff those blocks, unless we do the cumulative version of the ILs, which is stateful and much more complicated. the unconditional property that I like is “a transaction needs to get in a ~single~ in order to ensure that it lands onchain within the next two blocks”

---

**mikeneuder** (2024-02-02):

thanks for the super thoughtful response! i am going to push back on a few points, but really appreciate your perspective ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/milli3e/48/14573_2.png) Milli3E:

> After PBS validators won’t need to be concerned with block building and so in practice they will likely ignore the contents of the block and simply attest to the most profitable blocks. And once there is an incentive for builder diversity, competition will increase and naturally censorship will decrease as a result.

This is where I disagree. I don’t see ePBS as a way of increasing builder competition and diversity. If anything, the builder market now with open relays is much more of a meritocracy given ultrasound accepts any blocks and is highly competitive.

![](https://ethresear.ch/user_avatar/ethresear.ch/milli3e/48/14573_2.png) Milli3E:

> So I’m a little concerned that ILs don’t change much in practice and instead create a contentious environment on the chain and a culture of ignoring protocol spec (which isn’t the case right now) over something that isn’t egregious as of yet.

I see it slightly differently. IMO the censorship regime is highly unstable and could quickly evolve based on the decisions of a few people. CR seems like a candidate for a “defense in depth” approach, and the overton window of making big changes might be shrinking. setting the norm of “CR is the top priority” and getting ILs enshrined would also help us as we develop the protocol and begin to collect data on their usage.

![](https://ethresear.ch/user_avatar/ethresear.ch/milli3e/48/14573_2.png) Milli3E:

> I think ILs would make a lot more sense if the volume of censorship was much greater,

The volume could quickly go to 90+% overnight. what is an “unacceptable level” for you? feels like having several years at 90% (if we don’t go for it in electra) is potentially much more damaging than any residual risk of “doing something”.

![](https://ethresear.ch/user_avatar/ethresear.ch/milli3e/48/14573_2.png) Milli3E:

> even before enshrined PBS.

The current ePBS landscape is wide open. It is a highly contentious topic, and it doesn’t seem likely that anything will be enshrined in the next fork. So it’s helpful to think two years into the future. Do we think going two more years without directly addressing the CR holes in the protocol is a good idea? personally, i don’t.

---

**MicahZoltu** (2024-02-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/mikeneuder/48/11832_2.png) mikeneuder:

> IMO the bigger issue is the fact that the builder will only need to stuff a single block to avoid the enforcement of the IL. e.g., if only 5% of blocks fill make use of the IL, the builder only has to stuff those blocks, unless we do the cumulative version of the ILs, which is stateful and much more complicated. the unconditional property that I like is “a transaction needs to get in a ~single~ in order to ensure that it lands onchain within the next two blocks”

Assuming a block is half full (average due to 1559) and base fee is 20 nanoeth/gas, then this is 0.3 ETH cost to the builder to stuff a *single* block.  Do we have data on how far apart various builder blocks are from each other?  Is 0.3 ETH enough to make the non-censoring builder win the bid, or are the censoring builders more than 0.3 ETH better at block building than their competitors?

---

**Milli3E** (2024-02-02):

Thanks for the response Mike, I can appreciate your counter angle.

![](https://ethresear.ch/user_avatar/ethresear.ch/mikeneuder/48/11832_2.png) mikeneuder:

> This is where I disagree. I don’t see ePBS as a way of increasing builder competition and diversity. If anything, the builder market now with open relays is much more of a meritocracy given ultrasound accepts any blocks and is highly competitive.

Why do you think competition won’t increase? Running a relay atm is basically a free service, there are no economic incentives to enter the market, especially since (as you mentioned) the current relays are offering rather competitive services.

To add to that question, in the early ePBS concepts being proposed, is there a meaningful economic incentive to be builder? My assumption was that there will be, but if that’s not the case then I would fully agree with you.

![](https://ethresear.ch/user_avatar/ethresear.ch/mikeneuder/48/11832_2.png) mikeneuder:

> The volume could quickly go to 90+% overnight. what is an “unacceptable level” for you? feels like having several years at 90% (if we don’t go for it in electra) is potentially much more damaging than any residual risk of “doing something”.

I personally don’t think any level of censorship is acceptable. With that said, this particular form of censorship imo is less an issue of censorship than a philosophical pricing of risk by block builders.

The censorship in question is really more a case of builders thinking that a lack of an arbitrary incentive for creating a block is not enough to cover the risk of processing those txs.

I have no data to back this up but something tells me if the censored users were to increase priority fees (or increase slippage for a swap, etc) by a meaningful amount, some bock producer would pick up their txs and include it expeditiously by potentially bypassing the mempool/relays all together.

I think it’s quite difficult to enforce, what some builders would likely consider, a set price of risk (via ILs) for processing certain txs. Social layer economics are a non-trivial aspect of our society and they’re the primary reason why certain goods and services are more expensive in some countries vs others.

eg) Alcohol is much more expensive in middle east countries where it’s banned than in Europe/North America. Conversely alchohol in certain canadian jurisdictions is also more expensive due to government monopolies on the ability to sell liquor, leading to an uncompetitive market which ultimately over prices alcohol compared to most places in the first world.

Ultimately I think the concentration of relays makes for an environment where the risk of not censoring is priced too high and creates an environment which indirectly incentivizes censorship. Counteracting these effects requires more than a change in spec imo (which can easily be ignored). It really requires a fundamental change in the incentives to run a relay/be a builder, which equates to better competition.

I may need to brush up on what a post ePBS landscape looks like, but something tells me as long as builders (relays) have some economic incentive to participate, that competition is all but guaranteed to increase among actors. Especially considering the fact that there are like 3 relays atm. I just don’t see how it could possibly get more concentrated in the presence of incentives where it currently lacks.

To sum things up, I really wonder if the combination of the two points I made about lack of competition and the fair pricing of risk, will result in any meaningful change even in the face of ILs in a pre-ePBS world.


*(18 more replies not shown)*
