---
source: ethresearch
topic_id: 1438
title: Incentivizing a Robust P2P Network/Relay Layer
author: phil
date: "2018-03-20"
category: Economics
tags: []
url: https://ethresear.ch/t/incentivizing-a-robust-p2p-network-relay-layer/1438
views: 13525
likes: 26
posts_count: 26
---

# Incentivizing a Robust P2P Network/Relay Layer

**WARNING : THIS SCHEME IS HALF BAKED AND PLACED HERE EXCLUSIVELY FOR OPEN DISCUSSION / FEEDBACK**

# Background

As part of Project Chicago for Cryptocommodities (https://projectchicago.io/), we intend to analyze a range of blockchain resources and the cryptocommodities that they represent (and therefore the higher-order financial instruments they are able to create).

Part of the goals of such a project include the creation of fully incentive-compatible systems operating robustly in the rational actor model, with fair pricing for both providers and consumers of blockchain resources.  Unfortunately, several such resources, including the current peer-to-peer network, follow an unincentivized commons model which simply fails to achieve these properties.

Recent work (https://fc18.ifca.ai/bitcoin/papers/bitcoin18-final18.pdf) has identified three base resources of note in Ethereum transactions: computation, network, and storage.  To build efficient markets for all three resources, some price discovery mechanism is required.  In Ethereum, of these, computation currently enjoys the most robust such mechanism, with a two-sided gas market between miners and clients and relatively trustless derivative instruments enabling more advanced forms of speculation and risk management (eg https://gastoken.io/).  In this post, we seek to extend such an incentivization model to the p2p network layer.

# Strawman Scheme

For the sake of discussion and to establish feasibility, let us consider a scheme not optimized for efficiency / overhead / etc.  Optimizing and improving the scheme will continue in future work.

For simplicity, let’s also assume the current miner-based PoW blockchain architecture pre-sharding.  There are natural analogues to this scheme for the PoS and/or sharded blockchain model.

For each transaction, a sender generates some number (say, 4) fresh keys, SK_1, ..., SK_n, PK_1, ..., PK_n.

With each transaction, the sender s signs <data, PK_1, ..., PK_n, hopfee>_{PK_s}.  A transaction is considered invalid if a user’s balance is not sufficient to pay for gas + hopfee * tx_size.  When relaying, the sender includes the vector SK_1, ..., SK_n to the relayer.  The first relayer adds an onion-like layer to the transaction, signing <<data, PK_1, ..., PK_n, hopfee>_{PK_s}, A_1>_{PK_1} and sending the remaining data SK_2, ..., SK_n to all potential next-hops in the relay path.  In the case of an invalid SK, the relayer discards the transaction and bans the corresponding peer, bounding the denial of service vector involved with sending fake keys or signatures and performing the corresponding, somewhat expensive ECDSA operations.  This process is repeated until a transaction reaches a miner.  When included in a block, as part of ``miner-like" fees, each included relayer address is paid the hopfee from the user’s balance.  Validity of the process is checked, including that all sequential keys exist and are appropriately used in order. An honest miner will accept only the first such routed transaction, adding this transaction to its mempool as usual.  Any transaction that is signed by k<n public keys pays the miner (n-k)*hopfee*tx\_size in additional fees.

Relayers can now choose which transactions to relay based on their included hopfee, statically and efficiently rejecting transactions with low hopfees.  Relayers can also efficiently reject requests to which there are no corresponding secret keys through which they are paid.  Each relayer (including potential miners) can only be paid for hops after the first hop at which they received the transaction, as they have no knowledge of the secret keys before that point.  Relayers can double sign, but if n is chosen carefully to only slightly exceed the expected number of hops in the network, they risk some future relayer potentially running out of secret keys and rejecting the transaction, potentially losing them the relay race and thus profit on expectation.  n is chosen by the user carefully, with an economically rational user choosing an n that is high enough for routing to succeed, but as low as possible to avoid excessive fee payment.  The network also enforces a maximum n.

It is worth noting that by pre-sigining a set of addresses, a user can also enforce a given routing path to the miner, never distributing keys that enable miners to choose a route on which they are an earlier hop. This gives users relatively high levels of granularity in their choice of route.  Furthermore, each relayer can potentially pre-sign for the next relayer, requiring a p2p-level public key exchange.  This may however be undesirable for privacy, as it encourages address reuse over time.

# Incentives and Analysis

**(this analysis is not exhaustive, cursory, and likely flawed, but my intuition is that any major incentive incompatibilities here are fairly easy solvable)**

Users who wish to have their transactions relayed are incentivized to obey all validity rules, providing an appropriately sized valid vector of secret/private keys, obeying the network-wide limit on n, and ensuring they hold enough balance to pay hop fees.  Users who wish to perform a denial of service attack have several choices of griefing vectors, though the most expensive verification of validity is the check that the private keys and previous signatures are valid.  This is a relatively bounded amplification vector, though some careful analysis is required on this vector (if it turns out to be bad, one option is requiring deposits for incentivized/prioritized relays, and having some quota of free relays to allow users to bootstrap, or simply considering such invalid transactions as throws that pay full gas and can be included in blocks).

Relayers are incentivized to relay transactions as quickly as possible, winning the race for miner fees (probabilistically, under honest miner majority).  Any attempts to modify previous relayers’ onion layers will make the transaction invalid without knowledge of the original secret keys vector, and will delay propagation, potentially causing a loss in expected income.  Relayers can double sign, but likely will not, as miners earn more from transactions with shorter relay paths and will prefer such transactions for inclusion (and double singing is also an operation which may delay propagation).

Miners are incentivized to include all transactions without modification, as they earn fees from any remaining hops between k and n. This directly incentivizes miners to build and support relay networks with maximally short paths, increasing both their per-transaction take and relayer fee take.  Miners are also incentivized to be peers in this relay network, allowing them knowledge of earlier secret keys in the vector and increasing their overall take.  In general, if miners participate in the relay network, they will have a competitive advantage over other users proportional to their hashpower, meaning that it is possible that the system will essentially devolve to relaying transactions directly to miners.  This, however, is OK, as if miners are not available to some part of the network, other relayers can take up the task of building the missing paths that may be suffering from censorship or unavailability.

An open question is the value of relaying; if the value of each relay is really small, the cost of the blockspace to include relayers’ signatures may exceed the value of the payments they secure.  This is likely less of an issue as scalability proceeds to make block space far cheaper, but worth thinking about.

Current full nodes are incentivized to be relayers if they are generally on the critical relay path of at least some transactions.  If they are not, their overhead to the p2p layer may mean that it is preferable for such nodes to exclusively receive transactions, saving overall network overhead.

# Building Futures

An important property of both efficient price discovery and efficient marketplaces for cryptocommidities, including relayer bandwidth, is the existence of a robust market for speculation on the underlying commodity.

This scheme allows for such a marketplace to arise.  For example, cash-settled oracle-based futures that settle based on the average hop fees in a given period can be created, as can in-protocol futures using this approach.

The exploration of the full range of financial instruments enabled by this approach is left to future work.

# Acknowledgments

Thanks to [Ari Juels](http://www.arijuels.com/) for proposing the original version of this scheme, and for helpful discussions that lead to exploration of this problem.

## Replies

**phil** (2018-03-20):

Worth noting that a fun optimization here involves substantially reducing the security of the keys involved, since they only need to stay secure for the time it takes for a transaction to be included in a block.  There are definitely many more optimizations involved, both protocol and cryptographic, e.g. using (also low-security) Schnorr signatures [https://eprint.iacr.org/2018/068.pdf].

---

**jamesray1** (2018-03-20):

Thanks for the write up Phil! I definitely see the value in this proposal, incentivizing resource management / internalizing costs is critical for sustainability, and it will be interesting to keep an eye on further developments from Project Chicago. It would be good to see more research released on this, e.g. an analysis of all possible attacks (maybe similar in style to correct by construction, or [Rafael Pass et al’s Analysis of the Blockchain Protocol in Asynchronous Networks](https://eprint.iacr.org/2016/454.pdf)), optimizations, but you may also want to consider making a draft EIP to generate discussion there as well. Please continue to post your research findings here, and consider making an EIP once you have a well developed and tested framework.

---

**phil** (2018-03-20):

Omissions pointed out by Ari:

The scheme can be made much more space efficient, by the way, by using a PRNG to generate private keys and deriving public keys. E.g., in the ROM, X_i = H(X_{i-1}, 0), SK_i = H(X_i,1). Node i sends uses SK_i and passes X_{i+1} to Node i+1.

https://orbilu.uni.lu/bitstream/10993/19655/1/alex-ivan-tor-micropayments.pdf is relevant related work

---

**vbuterin** (2018-03-21):

Excellent job!

![](https://ethresear.ch/user_avatar/ethresear.ch/phil/48/18_2.png) phil:

> An honest miner will accept only the first such routed transaction, adding this transaction to its mempool as usual.  Any transaction that is signed by k<n public keys pays the miner (n−k)∗hopfee∗tx_size in additional fees.

One possible modification here is that we could allow each forwarder to specify what fee they want to claim; they would be incentivized to claim as much as they could but leave enough to get included by miners. Forwarders can already choose their fee to some extent, as they can claim multiple keys, so this would just make it easier to do so. We could even change the structure so that the inner signature only commits to the first public key, and then the forwarder could choose to either try their luck getting included by a miner directly or themselves commit to another public key and let some other forwarder claim a reward for forwarding it. Basically abstract the scheme and make it voluntary at every stage of transmission.

---

**Uptrenda** (2018-03-21):

Doesn’t this incentivize relayers to ignore TX validity rules though? If they want the hop fee they are encouraged to route messages as fast as possible. Blindly following the protocol to get hop fees is all they need to do here which should make the network less secure. I find the scheme interesting but I’m not sure I see the value in people forwarding messages like this if they don’t have to validate the blockchain. How do full nodes fit into this?

Given that Vitalik is in this thread: what thoughts have researchers given to full node incentives in Ethereum?

---

**phil** (2018-03-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/uptrenda/48/4308_2.png) Uptrenda:

> Doesn’t this incentivize relayers to ignore TX validity rules though?

No, honest peers can easily ban them for relaying invalid transactions, all the way to the mining level.  You don’t want to run the risk of cutting off your route.  Also, tx validity can be processed in parallel with the ECDSA sign operation, so I don’t see this as a major practical optimization, though this should be tested.  Would love to hear arguments otherwise though.

![](https://ethresear.ch/user_avatar/ethresear.ch/uptrenda/48/4308_2.png) Uptrenda:

> Blindly following the protocol to get hop fees is all they need to do here which should make the network less secure.

Not sure I agree.  At the end of the day, miners need to get paid by including *valid transactions* in blocks, so they should absolutely ban peers that open them to a DoS vector.

![](https://ethresear.ch/user_avatar/ethresear.ch/uptrenda/48/4308_2.png) Uptrenda:

> I find the scheme interesting but I’m not sure I see the value in people forwarding messages like this if they don’t have to validate the blockchain.

They may, because they can’t tell if the fee will be paid unless they are holding state.  This would open them up to a trivial DoS vector, especially with peer banning.

![](https://ethresear.ch/user_avatar/ethresear.ch/uptrenda/48/4308_2.png) Uptrenda:

> How do full nodes fit into this?

Full nodes serve as relayers and get paid.   Eventually, this role will move to proposers.

![](https://ethresear.ch/user_avatar/ethresear.ch/uptrenda/48/4308_2.png) Uptrenda:

> Given that Vitalik is in this thread: what thoughts have researchers given to full node incentives in Ethereum?

This is a way to incentivize full nodes with “proof of resources” in Ethereum.  There are other incentivization schemes that will incentivize making blockchain data available (serving downloads to other users who are not storing state).  This will of course make downloads cost money.  I’ll be proposing such a scheme in the next few days, though some proposals for this already exist.

---

**phil** (2018-03-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> One possible modification here is that we could allow each forwarder to specify what fee they want to claim; they would be incentivized to claim as much as they could but leave enough to get included by miners. Forwarders can already choose their fee to some extent, as they can claim multiple keys, so this would just make it easier to do so. We could even change the structure so that the inner signature only commits to the first public key, and then the forwarder could choose to either try their luck getting included by a miner directly or themselves commit to another public key and let some other forwarder claim a reward for forwarding it. Basically abstract the scheme and make it voluntary at every stage of transmission.

Making the hop fees variable is a great economic idea, thanks!!  I really like that variant of the scheme.

One thing I do want to support is a user selecting a pre-defined longer paths; I suppose they can just pre-sign with the addresses of those hops, so you get the same thing, and they also have more granularity on the incentives there.

---

**Uptrenda** (2018-03-21):

Good answers. Then I wonder how the network ends up building routes and what attacks might be there. How does bootstrapping / maintaining peer lists fit into this and is this secure against sybil attacks?

Really interesting work, by the way. This kind of thing is well overdue.

---

**phil** (2018-03-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/uptrenda/48/4308_2.png) Uptrenda:

> Good answers. Then I wonder how the network ends up building routes and what attacks might be there. How does bootstrapping / maintaining peer lists fit into this and is this secure against sybil attacks?

Since payments need to be on-chain, you can likely maintain a bonded peer list on chain too though.  But yeah, these interactions are super worth thinking about.  Deposits for relayers can guard against Sybil, though there would be a balance there because you don’t want to require a large / frequent deposit; perhaps optional deposits, where the probability of being selected in a node’s peer list was weighted by deposit, plus some classic slots?  Sybil can just be viewed as providing infrastructure in this model.

![](https://ethresear.ch/user_avatar/ethresear.ch/uptrenda/48/4308_2.png) Uptrenda:

> Really interesting work, by the way. This kind of thing is well overdue.

Thanks so much, glad you like it!

---

**ChosunOne** (2018-03-22):

I think a glaring issue with this type of scheme is that in the current PoW architecture how do you know which miner to send a transaction to?  By design the miners creating blocks are random, so under this scheme it seems like it would cause extreme mining centralization by rewarding more powerful miners both from the block reward and the fact that other miners don’t get nearly as much traffic to get transactions fees from.

---

**phil** (2018-03-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/chosunone/48/732_2.png) ChosunOne:

> I think a glaring issue with this type of scheme is that in the current PoW architecture how do you know which miner to send a transaction to?  By design the miners creating blocks are random, so under this scheme it seems like it would cause extreme mining centralization by rewarding more powerful miners both from the block reward and the fact that other miners don’t get nearly as much traffic to get transactions fees from.

Ideally you’d broadcast to all miners who intend to mine a block.  The economies of scale for mining are so bad that I doubt small number of fees could make a difference.  If anything, you’d find an intermediary to route to you at a relatively small cut (there would be an implicit competitive marketplace for such intermediaries).

---

**ChosunOne** (2018-03-22):

How do you calculate and find all miners “intending to mine a block”?  It seems like this would inflate the cost of a transaction and encourage users to just pick a few miners, which then would give those miners extreme censorship control.

---

**phil** (2018-03-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/chosunone/48/732_2.png) ChosunOne:

> How do you calculate and find all miners “intending to mine a block”?

That’s up to the user.  Naively you can gossip everything, and assume miners will attempt to peer with every node at a height of 1 to collect maximum fees.  You can also use a separate relay network, both, etc.

![](https://ethresear.ch/user_avatar/ethresear.ch/chosunone/48/732_2.png) ChosunOne:

> It seems like this would inflate the cost of a transaction and encourage users to just pick a few miners, which then would give those miners extreme censorship control.

It wouldn’t “inflate the cost of a transaction”, it would bring it closer in line to its true cost to the network (assuming you’re talking about relay fees).

The miner of a block already has full censorship control over that block.  If relaying miners censor relays, this will incentivize relayers who do not censor to do their best to get transactions into the blocks of miners who do not censor.  In case of extreme censorship, the value of these relays and thus the associated fees will rise in a competitive marketplace, incentivizing paths that route around the censorship.

Think Great Firewall of China; a scheme like this could, even when all p2p traffic / ETH nodes are disabled, incentivize steganographic channels between users submitting traffic and miners including them in blocks.

Actually does quite the opposite of censorship control :).

---

**ChosunOne** (2018-03-23):

> The miner of a block already has full censorship control over that block. If relaying miners censor relays, this will incentivize relayers who do not censor to do their best to get transactions into the blocks of miners who do not censor. In case of extreme censorship, the value of these relays and thus the associated fees will rise in a competitive marketplace, incentivizing paths that route around the censorship.

So if I understand you correctly, you mean to say that relayers are actually incentivized to send messages to miners who do not censor?  This comes from the fact that the relayer isn’t paid unless the transaction is mined right?

> It wouldn’t “inflate the cost of a transaction”, it would bring it closer in line to its true cost to the network (assuming you’re talking about relay fees).

I was thinking that miner selection could be an issue if the relayer cost is too high, and users are disincentivized to send transactions to all miners.  When the hopfee is an appreciable amount, the cost of sending a transaction to all miners could be something like 100 or 1000 times more than the miner fee.  In that scenario I think there is a high risk of users only choosing to send transactions to one miner.  I suppose this could be seen as intended behavior, but I don’t know what order the hopfee would end up being if we want to keep all miners seeing all broadcast transactions, which seems like an important property to have.

---

**jamesray1** (2018-03-23):

I’m just going to be a troll and say “In the ROM”…, then share a link to this critique:


      ![](https://ethresear.ch/uploads/default/original/3X/7/8/78cd713ceaae1eda19cfba5be049ddf1f2e0cc19.png)

      [A Few Thoughts on Cryptographic Engineering – 8 Oct 11](https://blog.cryptographyengineering.com/2011/10/08/what-is-random-oracle-model-and-why-2/)



    ![](https://ethresear.ch/uploads/default/original/3X/7/2/722292fffee3ee5b5cc65ecfa9d9a6604c3aeb62.jpeg)

###



This is part 2 of a series on the Random Oracle Model.  See “Part 1: An introduction” for the previous post. In a previous post I promised to explain what the Random Oracle Model is, an…

---

**phil** (2018-03-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/chosunone/48/732_2.png) ChosunOne:

> So if I understand you correctly, you mean to say that relayers are actually incentivized to send messages to miners who do not censor?  This comes from the fact that the relayer isn’t paid unless the transaction is mined right?

Yup.

![](https://ethresear.ch/user_avatar/ethresear.ch/chosunone/48/732_2.png) ChosunOne:

> I was thinking that miner selection could be an issue if the relayer cost is too high, and users are disincentivized to send transactions to all miners.  When the hopfee is an appreciable amount, the cost of sending a transaction to all miners could be something like 100 or 1000 times more than the miner fee.  In that scenario I think there is a high risk of users only choosing to send transactions to one miner.  I suppose this could be seen as intended behavior, but I don’t know what order the hopfee would end up being if we want to keep all miners seeing all broadcast transactions, which seems like an important property to have.

You only pay the hopfee *once*.  EG if your hopfee is 1ETH and you have at most 10 hops, the most fees you will ever pay is 10ETH, no matter how many nodes you relay too.  Only the *winning route* (aka the route that actually gets a transaction mined) is compensated, not all routes.  So in fact all users and relayers will gossip as widely as possible to maximize the probability that their path is the winning one, and they get paid.

---

**phil** (2018-03-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/jamesray1/48/4269_2.png) jamesray1:

> I’m just going to be a troll and say “In the ROM”…, then share a link to this critique:

I don’t think that’s a critique!  But yes, it took cryptographers a long time to become (relatively) comfortable with the ROM.

---

**jamesray1** (2018-03-24):

OK, perhaps I should re-read those blog posts, maybe some time later after lots of development on sharding is done and on an as-needed basis.

---

**ChosunOne** (2018-03-24):

> You only pay the hopfee once. EG if your hopfee is 1ETH and you have at most 10 hops, the most fees you will ever pay is 10ETH, no matter how many nodes you relay too. Only the winning route (aka the route that actually gets a transaction mined) is compensated, not all routes. So in fact all users and relayers will gossip as widely as possible to maximize the probability that their path is the winning one, and they get paid.

Ah I see now, thanks for the clarification!

---

**michaelsproul** (2018-03-28):

Is the A_i that each relayer adds to the transaction bundle and signs the *address* at which they wish to be paid their hop fee? I initially understood the hop fee payments to be made to the PK_1, ..., PK_n keys, which was somewhat confusing.


*(5 more replies not shown)*
