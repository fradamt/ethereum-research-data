---
source: ethresearch
topic_id: 13808
title: How much can we constrain builders without bringing back heavy burdens to proposers?
author: vbuterin
date: "2022-10-01"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/how-much-can-we-constrain-builders-without-bringing-back-heavy-burdens-to-proposers/13808
views: 19701
likes: 35
posts_count: 16
---

# How much can we constrain builders without bringing back heavy burdens to proposers?

One natural response to the risks of builder centralization (mainly censorship, but also various forms of economic exploitation) is to try to constrain the power that builders have. Instead of builders having full rein to construct the *entire* block if they win an auction, builders would have a more limited amount of power. This power should still be enough to capture almost all MEV that could be captured, and it should ideally still be enough to capture other benefits of PBS, but it should be weakened to limit opportunities for abuse.

This idea is sometimes called **partial block auctions**: instead of auctioning off the right to decide everything in a block, auction off the right to decide *some things*, where those “some things” could be much more nuanced than eg. “the builder chooses the first half of the block and not the second”: you could give the builder the right to reorder, prepend, append, and you could even constrain the proposer. This post gets into some possible ways of doing this, and some of the tradeoffs that result.

## Inclusion lists

In the inclusion list paradigm, a proposer provides an *inclusion list*, a list of transactions that they demand must be included in the block, unless the builder can fill a block *completely* with other transactions.

[![inclusionlist.drawio](https://ethresear.ch/uploads/default/original/2X/1/17c9ae8c2f65fde9dbf814376563b338b1d0aff7.png)inclusionlist.drawio541×341 14.5 KB](https://ethresear.ch/uploads/default/17c9ae8c2f65fde9dbf814376563b338b1d0aff7)

For a profit-maximizing builder that is not affected by unusual external incentives, an inclusion list is no constraint at all: adding an additional transaction to the end of a block always gives the builder that transaction’s priority fee as an extra profit.

In the case where the block is filled up to the full gas limit (2x the target), so the builder would have to choose between that transaction and other transactions, the constraint is disabled. This does not affect inclusion in the long run, because a run of full blocks can only be sustained briefly as it makes the base fee rise exponentially (~2.02x every 6 blocks).

However, if a builder does have some desire to refuse to include specific transactions that it disapproves of or is incentivized to exclude, that builder would be forced to not participate in the auction.

This design is reasonably simple, but it is important to describe some of its weaknesses:

- Incentive compatibility issues: the builder sees the inclusion list ahead of time, and the builder can refuse to build blocks that contain an inclusion list that they do not want to build on. This creates an immediate incentive for proposers to have empty inclusion lists, to maximize the chance that builders will build blocks for them.
- Extra burdens on proposers: the proposer needs to be able to identify fee-paying transactions. This requires (i) access to the mempool and (ii) either ability to read the state to determine fee-paying-ness, or witnesses attached to transactions. Witnesses are preferable, as they would preserve the PBS property that validators could be stateless clients.
- The builder can still engage in some abuses: notably sandwich attacks. However it’s not clear how it’s possible to remove this issue without extreme approaches like using advanced cryptography to encrypt mempools, since otherwise taking this power away from the builder implies giving it to the proposer, which would incentivize proposers joining stake pools.
- Requires partial enshrining for account abstraction to work: see The road to account abstraction - HackMD

## Proposer suffixes

An alternative construction is to allow the proposer to create a suffix for the block. The builder would see no information about the proposer’s intentions when they build a block, and the proposer would be able to add to the end any transactions that the builder missed.

[![proposersuffix.drawio](https://ethresear.ch/uploads/default/original/2X/e/ed4171d244d3c3bd8fd6730ef5fbeacfdbb1b773.png)proposersuffix.drawio541×371 16.5 KB](https://ethresear.ch/uploads/default/ed4171d244d3c3bd8fd6730ef5fbeacfdbb1b773)

- Reduced incentive compatibility issues: the builder can still retroactively punish proposers (eg. by refusing to build for them in the future) that include transactions that the builder disapproves of, and sends the root to the builder. This is unavoidable, but this is much more proposer-friendly than builders being able to refuse to construct blocks in real time (especially since each individual proposer only proposes occasionally, today once every ~2 months).
- Even more extra burdens on proposers - the proposer now has to compute the post-state root, which means that the proposer must hold the entire state. Hence, no statelessness is possible, unless the proposer outsources this task to a separate intermediary.
- The proposer gets some MEV opportunities between getting the response from the builder and having to publish the block. This is likely only half a second worth, but it’s still some increase to the incentive for validators to join stake pools to be able to optimize in-house.
- The builder can still engage in some abuses, as before
- Requires partial enshrining for account abstraction to work, as before

## Fix to proposer suffixes: pre-commitment

The proposer pre-commits to a Merkle tree or KZG commitment or other accumulator of the set of txs that they want to include. The builder creates their block. The proposer must then add the suffix consisting exactly of the subset of the Merkle tree that has not yet been included by the builder, and that the gas limit allows them to include, ordering by txhash or some other standardized order (if they add any other suffix, they get slashed).

[![proposersuffixwithtree.drawio](https://ethresear.ch/uploads/default/optimized/2X/9/9f6f4ddfedb97abfc4f4b571f9edb5ef903f9036_2_528x500.png)proposersuffixwithtree.drawio541×512 20.8 KB](https://ethresear.ch/uploads/default/9f6f4ddfedb97abfc4f4b571f9edb5ef903f9036)

The details of enforcing the slashing are somewhat involved, especially if you want to avoid putting the proposer’s inclusion tree in the clear. It could be reasonably easily done with KZG commitments and special-purpose ZK-SNARKs, using specialized polynomial equations to verify the concept of “if you start from the set with commitment X, and remove anything that’s in Y, then the remaining set is Z”.

This removes the proposer’s MEV opportunities, because the proposer has zero degrees of freedom in what block to publish once the builder replies back with their own block contents, but it leaves the other issues unresolved.

## The longer-term endgame: how do we constrain the builder and minimize responsibilities of the proposer?

The proposer’s role should ideally be kept minimal: simply identify transactions that deserve to be included. Minimizing the proposer’s role ensures that the role is kept highly accessible. The builder’s role should ideally be kept minimal: the builder should have the right to reorder transactions from the mempool and insert their own transactions to collect MEV, without being able to discriminate against blocks based on which transactions they will include.

But this leaves many other important tasks unallocated, especially tasks that will become necessary in the future:

- The task of computing the post-state root
- The task of computing and publishing the witness
- The task of making a ZK-SNARK attesting to the block’s correctness

If these tasks do not go to the builder, or the proposer, then they would have to go to some *third* actor. There are a few possible ways to implement this:

- We create a separate class of builder-like intermediary, which proposers contract with, and which considers itself to merely be a specialized cloud computing provider whose job it is to compute outputs of functions (ZK SNARK generation, state root computation, etc), and is not involved in choosing block contents
- We require the next block to contain these values for the previous block. It’s up to the next block’s proposer to find an intermediary to construct these values and if needed to verify them.
- We enshrine a separate class of intermediary in-protocol and add in-protocol incentives for them
- We leave it up to altruistic actors in the network to publish these values (so they do not get hashed into the block). Attesters only attest once they see correct values provided.

In any case, the simultaneous need to minimize the powers and information available to the builder, and the load imposed on the proposer, seems to clearly point towards the need for some third actor in the block production pipeline (unless we bite the bullet and accept that builders have the right to see the inclusion list, and hence discriminate against particular transactions being included in the same slot). We should start thinking more deeply about how exactly this is going to be handled.

## Replies

**fradamt** (2022-10-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Incentive compatibility issues: the builder sees the inclusion list ahead of time, and the builder can refuse to build blocks that contain an inclusion list that they do not want to build on. This creates an immediate incentive for proposers to have empty inclusion lists, to maximize the chance that builders will build blocks for them.

One way around this is to just have someone else make the inclusion list, so that they don’t have this conflict of incentives. This does complicate things, because it requires moving to the inclusion lists being enforced by attestations rather than as a validity condition, but this seems anyway to be necessary for compatibility with SSLE. The simplest scheme is just to have a proposer make the inclusion list which is enforced for the *next* block, instead of theirs. Most of the time, two proposers won’t have common incentives, so one could make the list without any worry of giving up profits.

---

**vbuterin** (2022-10-01):

> The simplest scheme is just to have a proposer make the inclusion list which is enforced for the next block, instead of theirs

One issue with this is that you can abuse it for data availability purposes.

In slot N, which the attacker controls, you add to the inclusion list a transaction with 1 MB calldata. In slot N+1, you broadcast a transaction from the same account with a high priority fee, but with no calldata, just 21000 wasted gas, and make sure that builders see it. They include it instead of the old tx, so you never pay for the old tx, but data availability of the old tx is still guaranteed. If you want to ensure that the builder doesn’t choose the old tx anyway, you could wait until you have control of *both* slots N and N+1, and self-build slot N+1.

---

**MicahZoltu** (2022-10-02):

How unreasonable would it be to make it so you can’t RBF once a transaction is “scheduled” for future inclusion?  Essentially, the transaction is included in block `n`, even though it isn’t *executed* until block `n+1`.  Functionally, this means the nonce is “used” already in block `n` even though execution is delayed.

I suspect the answer here is that this kinda ruins some of the account abstraction designs?

---

**vbuterin** (2022-10-02):

Isn’t that just equivalent to executing the transaction at the end of the previous block? Or is the idea that the validation step is done in the previous block, and the execution step is done in the next block, to make that transaction useless for MEV extraction?

It definitely would break lots of abstractions and interact with the transaction / account system in complicated ways if you do that; significant rise in systemic complexity.

---

**MicahZoltu** (2022-10-02):

A proposer including non-executed transactions in their block can do so without updating the state tree.  They still need the state to validate balance, which is unfortunate, but presumably this is already a requirement for transaction pool management.

What is important here is that the proposer can include a list of transactions without seeing the unblinded block from the builder, because they don’t need to update any of the EL trees.  If a account+nonce is in their list and in the blinded block, the transaction from proposer list is ignored (not fully gossipped).  If a transaction is in their list and valid next block, it **must** be executed in that block for the block to be valid.

I agree that this adds a lot of complexity.  My hope is that perhaps this idea can grow into something simpler.

EDIT: thinking more on this, we can’t “not gossip” a transaction in the proposer list because you have to send the whole transaction so the signature can be validated, so we still would have the DOS attack.

---

**domothy** (2022-10-03):

Throwing some random ideas here regarding the free DA problem, unsure about extra complexity involved but there may be some merit:

a new EIP2718 transaction type specifically for transactions who want to make it into the inclusion list (possibly with a bribe for the validator who puts it in the list) which forces the user to pay max fee × gas limit ahead of time when it makes it in the list, rather than when it’s actually included in a block. The only possible refund is for unused gas if/when the transaction makes it in a block. We can possibly force some rule like the transaction’s max fee must be greater than 10x the current block’s base fee to have a more-than-reasonable shot at being included in the next few blocks

alternatively, the inclusion list could merely contain transaction hashes - with a multi round PBS, we could have a scheme where block builders have to sign a message ahead of time saying “yes, I have seen the contents of the transaction with hash `0xabc...` and will be including it in my block” in order to be considered as possible (this may open up new attack vectors with proposer/builder collusion w.r.t. private order flows, maybe we need strong commitment from validator committees to be reasonably confident that the transaction has in fact been seen by enough people for block building to remain open and competitive)

---

**Pandapip1** (2022-10-03):

How does this proposal look? It doesn’t add too much of a burden to proposers (the worst-case computational complexity doesn’t change).



    ![](https://ethresear.ch/user_avatar/ethresear.ch/pandapip1/48/9697_2.png)
    [MEV minimization using randomness](https://ethresear.ch/t/mev-minimization-using-randomness/13825/4) [Economics](/c/economics/16)



> I propose the following alternative, which would make MEV very hard for block proposers:
>
> Block proposers can pick which transactions to include or not to include in advance. The hash of all these transactions is computed. Let these be the initial orders for those transactions.
> A block is only valid if the following is true:
>
> The transaction with a median order (treated as binary numbers) is the next transaction included in a block. The median can be efficiently found in O(n) time with a select…

---

**tbrannt** (2022-10-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Incentive compatibility issues: the builder sees the inclusion list ahead of time, and the builder can refuse to build blocks that contain an inclusion list that they do not want to build on. This creates an immediate incentive for proposers to have empty inclusion lists, to maximize the chance that builders will build blocks for them.

I feel like you’re all a bit too certain that this will indeed be a problem. Sure, for now flashbots has quite the strong position but I think over time there will just be too much competition for one builder to have such an influence on proposers. We just need to make sure that it’s an open auction where the barriers to entry are as low as possible. E.g. one could think about nodes paying each other small amounts of eth to become each others peers. So there won’t be one well connected flashbots builder who will out-compete all others.

The main reasons I’m optimistic is that it’s an open space to innovate and compete: everyone can see the mempool, everyone can freely compete in writing mev scripts. And also, excluding tx should naturally be a disadvantage when trying to build maximally profitable blocks. So builders who include everything should always have an edge over those who don’t (at least in the long run).

So maybe don’t add more complexity to fix problems that might not actually be problems? Sure doesn’t hurt to think about potential solutions though. But as mentioned I think one way to tackle this is to think about ways to incorporate ways for nodes to pay each other small amounts of eth so there are straight forward ways to become a well connected node. (Also nodes could recommend other nodes and receive “commisions”)

---

**MicahZoltu** (2022-10-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/tbrannt/48/1050_2.png) tbrannt:

> I feel like you’re all a bit too certain that this will indeed be a problem.

The design philosophy of Ethereum is generally to assume worst case scenarios and build defensively against them.  We also generally design under the assumption that people will follow incentives.  In this case, the incentives exist for this to be a problem so we should design around that, rather than hoping that it doesn’t come to pass.

---

**bruno_f** (2022-10-05):

It’s not clear to me (assuming rational proposers and builders) why proposers would include any transactions in their inclusion list at all. A builder supposedly can extract more value from any given amount of block space than the proposer, so the optimal strategy for the proposer is to just let the builder utilize the entire block (i.e. have an empty inclusion list).

---

**bertmiller** (2022-10-05):

Brainstorming a bit with research folks and here is an early idea for how inclusion lists could apply to mev-boost:

1. Proposer can send a list of transactions to mev-boost relays that specifies which transactions must be included in a block for that to be considered valid by mev-boost. This likely needs to be done with a new API call that’s signed by the proposer.
2. Then when the proposer asks relays for a block header the relay responds with a header along with merkle proofs proving that the transactions from the proposer’s inclusion list are present in the block.
3. For each block header that is returned mev-boost validates the proofs to ensure each transaction from the proposer’s list was included. If a block header did not include the necessary transactions then it is discarded.

In effect this would make mev-boost temporarily filter out, just for that block, relays which are not able to include their desired transactions.

We had thought about allowing the proposer to specify their inclusion list in the getHeader() call when they got a block. However, this doesn’t work because that call isn’t authenticated, so the relay can’t know that it was actually the proposer who is asking for transactions to be included. A new API call also avoids having the inclusion list come “just in time” and the proposer can register their inclusion list ahead of their slot.

One additional thing that could be done is have the beacon node validate the merkle proofs of the final block header and switch to a block built locally if the block doesn’t meet their requirements. I’m not sure if this is necessary (as mev-boost does the validation too), so others would need to weigh in here.

Perhaps there is a way to disable the merkle proof checks if the relay is offering a block that is filled up to the full gas limit. I’ll think about that a bit more. Right now the above doesn’t offer that functionality.

Lastly, I’ve described how this works primarily with a proposer <> relay interaction in mind, but the system should work the same if a proposer is interfacing directly with a builder. I think it would also translate to in-protocol PBS well some day.

---

**mkoeppelmann** (2022-10-06):

[@bertmiller](/u/bertmiller)

This would certainly be a significant improvement over the status quo.

> Perhaps there is a way to disable the Merkle proof checks if the relay is offering a block that is filled up to the full gas limit. I’ll think about that a bit more. Right now the above doesn’t offer that functionality.

IMO that is not needed. In my view, a good “default strategy” for any validator caring about censorship resistance but also wants to minimize the loss against don’t restrict the builder in any form would be: Select transactions they know about by the highest tip and include so many into the list that they fill up, up to 10% of the block space. This should almost never prevent a “max profit” block but should also be a significant factor in getting transactions included that have been potentially left out of a previous block despite the willingness to pay a high enough fee.

**Edit:**

Though one risk that should be considered: currently (as far as I understand) anyone can query relays which helps with transparency. If calls are authenticated relays could either stop responding to anyone else or even give different responses to others to try to obfuscate their behavior.

---

**quintuskilbourn** (2022-10-06):

[@mkoeppelmann](/u/mkoeppelmann)

One concern with full blocks is that some proposers run an auction for access to the inclusion list when there are demand spikes. The issue would be that small validators wouldn’t be able to do this.

Of course, this may not be that big of a deal, depending on how often and large we anticipate demand spikes to be.

---

**bertmiller** (2022-10-06):

> Though one risk that should be considered: currently (as far as I understand) anyone can query relays which helps with transparency. If calls are authenticated relays could either stop responding to anyone else or even give different responses to others to try to obfuscate their behavior.

I think only the call to register an inclusion list (and `registerValidator`) would be authenticated, and otherwise all other calls be unauthenticated as the status quo is.

---

**AnneGloindian** (2023-02-13):

[@domothy](https://kohiclicks.com/space-bar.html/) thank you so much share the detial so helpful for me

