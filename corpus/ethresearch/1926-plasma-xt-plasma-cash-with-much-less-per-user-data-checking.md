---
source: ethresearch
topic_id: 1926
title: "Plasma XT: Plasma Cash with much less per-user data checking"
author: kfichter
date: "2018-05-07"
category: Layer 2 > Plasma
tags: [new-extension]
url: https://ethresear.ch/t/plasma-xt-plasma-cash-with-much-less-per-user-data-checking/1926
views: 17999
likes: 26
posts_count: 35
---

# Plasma XT: Plasma Cash with much less per-user data checking

Plasma XT embraces Plasma Cash’s original vision of simple, reliable, low-cost transactions for everyone in the world.*

Special thanks to Dan Robinson for discussion and coming up with much of this, as well as David Knott, Joseph Poon, Karl Floersch, and Vitalik Buterin for ideas and feedback that led to this design. Another special thanks to Justin Drake for the gorgeous construction of [cryptoeconomic aggregate signatures](https://ethresear.ch/t/cryptoeconomic-signature-aggregation/1659) and to Sunny Aggarwal for the Plasma XT name.

(enough memes now)

Really, huge thank you to [@danrobinson](/u/danrobinson)! Almost all of this came out of discussion with/ideas from Dan.

*[context](https://bitcoinxt.software)

## TL;DR

Plasma XT is a modification to Plasma Cash that enables safe checkpointing.

## Background

[Plasma Cash](https://ethresear.ch/t/plasma-cash-plasma-with-much-less-per-user-data-checking/1298), as originally specified, requires that users maintain an ever-growing history of transactions, inclusion proofs, and non-inclusion proofs. **Currently, this history is too large to be feasible.**

Some napkin math to illustrate:

Assuming we have a (very) small Plasma Cash chain with only 2^16 (= 65536) coins, then the Merkle proof of either existence or non-existence for a given coin will be at least 32 bytes * 16 siblings = 512 bytes per block. If we assume that Plasma block is created once every 15 seconds, then we’ll end up with 31557600 / 15 = 2103840 blocks per year. 2103840 blocks per year * 512 bytes per block = 1077166080 bytes per year = ~1.077 gigabytes per year. 1 gigabyte per coin, per year!

This means that the owner of a coin would, after one year, have to send more than a gigabyte of proof data simply to make a single transaction. Although the exact proof size can likely be slightly optimized, the proof size still grows linearly with the size of the Plasma Cash chain. That’s a lot of data! It’d be hard to store and validate a proof this big on devices that might be computationally limited, like phones or embedded devices. After enough time, it might even be difficult to validate these proofs on laptops or workstations.

This post attempts to solve this problem by specifying a protocol in which coins can be checkpointed. The owner of a coin will, therefore, only need to provide a proof back to the coin’s last checkpoint.

## Checkpoints

Checkpoints are one solution to the above problem. If we can properly construct regular intervals in which the state of a coin is considered “finalized”, then it’s possible to reduce the total proof size significantly (to some relatively small constant). Generally, this is accomplished by having the operator attest to the current state and allow for a challenge period in which this state may be contested. If no one shows that the state is invalid, then the checkpoint is considered finalized.

### Naive Checkpoints

Checkpoints are really hard to get right! Let’s look at the following (flawed) checkpoint construction to illustrate some of the challenges:

Every `N` blocks, the operator publishes a Merkle state root. This root is derived from a Merkle tree in which each leaf node represents the current valid owner of each coin in the tree. So if user `A` owns coin #0, then the operator will place `A`'s address at the 0th (first) leaf in the tree.

The operator places a bond on this action. Any user can prove that the state is invalid (and therefore claim the operator’s bond) by showing that the operator has lied about the owner of a certain coin. If no successful challenges take place after some amount of time, then the checkpoint is considered finalized.

Why is this design flawed? It comes down to the (really hard) problem of data availability. If the operator publishes a state root but does not publish the tree itself, then it’s impossible for anyone to challenge the checkpoint. You can’t prove that something is invalid if you can’t even validate it in the first place.

Because we don’t know if the checkpoint is valid or not, we have to assume that the operator is trying to steal some money. Once the checkpoint finalizes, the checkpoint state becomes the “true” state. The only solution is for all of the coin owners to exit *before the checkpoint finalizes*. Even worse, since we can’t prove the operator did something bad, we can’t punish the operator. We never want to force a user to act within some time-frame if the user won’t receive some sort of bounty for doing so.

### Fancy Checkpoints

It turns out we can (sort of) solve the data availability problem by taking advantage of a few interesting observations. Let’s go back to first principles - in the above example, no one can challenge the operator because no one knows if the data is valid or not. So, what if we could design a system so that someone *will* know if the operator is trying to cheat?

Well, we can! We just need to rely on some signatures. The basic idea here is that *each user that wants to have their coin checkpointed will sign off on their coin in the checkpoint*. Generally, this means that the operator has *proof* that each coin holder that wants their coin checkpointed has confirmed the checkpoint to be correct. Then, if the operator claims to have your permission but doesn’t, you know the operator is trying to cheat and the operator can be punished.

#### Cryptoeconomic Aggregate Signatures

But wait, wouldn’t it be too expensive to put all those signatures on-chain? Yes, absolutely. But luckily, we don’t actually have to put all of these signatures on-chain. Here’s where [cryptoeconomic aggregate signatures](https://ethresear.ch/t/cryptoeconomic-signature-aggregation/1659) come into play.

The idea here is that instead of publishing full signatures for every user, the operator only publishes a *claim* that a certain owner has provided a signature (in the form of a bitfield). For example, if we have 4 coins, and owner of coins #0 and #3 have provided signatures, then the operator would publish the bitfield “1001”. If, however, the owner of coin #3 did *not* provide a signature and the operator published that bitfield, then the owner of coin #3 could challenge by requesting the operator provide the owner’s signature. So our signatures are suddenly down to one bit per coin!

#### Checkpoint Zones

But wait, wouldn’t one bit per coin *still* be too expensive to put on-chain? Well, yes. Our scheme just requires putting the bitfield in calldata, so things work out to about 100k gas (currently ~$0.25) per 8192 coins = ~1 kilobyte. This is too much gas if we want to checkpoint many coins (millions) at the same time, so we turn to “checkpoint zones”.

Checkpoint zones effectively checkpoint *some* coins at a time. Every coin will be scheduled to be checkpointed on some regular basis. For example, coins 0-8191 might be checkpointed during one block, and coins 8192-16383 might be checkpointed in the next. By checkpointing on a rolling basis, we make sure that we’re always inside of the gas limit, even if we need to checkpoint millions of coins.

### Challenging a Checkpoint

Users can challenge invalid checkpoints. Checkpoints can be invalid if the operator places a 1 at the index of a certain coin but the true owner hasn’t signed off on that checkpoint. Only the true owner knows if they’ve signed off or not, so each coin owner is responsible for verifying the bitfield in each checkpoint. Luckily, the user is already required to be online regularly to look for invalid exits on their coins, so we’re not changing any assumptions behind Plasma Cash.

If the operator places a 1 in the bitfield for a user that did not sign off on a signature, then the user will challenge. This challenge includes the user’s latest transaction in the history, attesting that the user is indeed the owner. The operator can then respond by either showing a signature from the owner or with a later transaction proving that the challenger is not really the owner. Multiple challenges may exist on the same coin at the same time, but only one bond will be paid per coin.

There’s a potential attack vector if the operator submits very many 1s in the bitfield at the same time, because each user that didn’t sign off will have to submit a challenge. To get around this, we define a maximum number of challenges that may be open per checkpoint at any one time (probably 256). If more than this max number of challenges are open at any one time, then the checkpoint is invalidated. This basically ensures that not *everyone* needs to challenge and we don’t overload the root chain with challenges.

### Caveats

#### Gas Cost

As we stated before, the bitfield grows with the total number of coins in the Plasma Cash chain, so things get more expensive as the total number of coins increases. This checkpoint scheme is a good solution for even many millions of coins, but might need to be revisited if we ever reach many tens of millions or even hundreds of millions of coins.

#### Liveness

We’re assuming that a user will be live at least once during the checkpoint challenge period. This doesn’t change any assumptions of Plasma Cash if we make the checkpoint challenge period at least as long as the exit challenge period.

#### Griefing

##### By Operator

The operator can grief a user by refusing to checkpoint a coin (always putting 0 in the bitfield). If there’s a 0 at some index, it’s impossible to tell if the operator didn’t receive a signature or is simply refusing to include it. This doesn’t harm any security, but means that we’re falling back on Plasma Cash-sized transaction history lengths. We could probably implement some sort of manual checkpointing as an on-chain transaction, but we want to avoid that if possible.

##### By Users

Users can grief other users by making lots of open challenges and invalidating the checkpoint. If the open challenges aren’t valid, then this attack is very costly as each challenge requires a bond. This also doesn’t harm security, but might be annoying. We need to determine the optimal bond size that makes this attack as costly as possible without making it too costly to submit a challenge. Again, this case simply means that we fallback on the guarantees and security properties of Plasma Cash.

## Replies

**ldct** (2018-05-07):

I will throw in my suggestion for the title - “Plasma Cash Cash” ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

slogan: plasma cash cash is plasma cash

meta-slogan: “plasma cash cash is plasma cash” is “plasma cash is plasma”

---

**ldct** (2018-05-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png) kfichter:

> This doesn’t harm any security, but means that we’re falling back on Plasma Cash-sized transaction history lengths. We could probably implement some sort of manual checkpointing as an on-chain transaction, but we want to avoid that if possible.

If a user is being griefed this way, exiting and re-deposit his coin is equivalent to “manual on-chain checkpointing” for a single user. The challenge would be to amortize this cost over multiple users.

---

**danrobinson** (2018-05-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/ldct/48/281_2.png) ldct:

> If a user is being griefed this way, exiting and re-deposit his coin is equivalent to “manual on-chain checkpointing” for a single user. The challenge would be to amortize this cost over multiple users.

This makes me wonder why it should even be a requirement that Plasma XT checkpoints can only be operator-initiated. It makes plenty of sense for the operator to initiate checkpoints (because they have all the information about the state), but users (or anyone) could also conceivably initiate them, by doing the same thing—putting up a bond, and revealing a state commitment and a cryptoeconomic aggregate signature.

If that works, then operators can’t even prevent users from checkpointing their state (although, since they can prevent users from transacting, this isn’t a particularly significant win).

This might be a good reason to look at alternative ways of expressing the bitmaps in cryptoeconomic aggregate sigs. The only requirement is that you somehow identify all the coins that assent to the checkpoint. This can be done via bitmaps (if there are many adjacent coins involved in the checkpoint), but if participating coins are much sparser, a list of indices might be more efficient; indeed if they’re much denser, a list of the unincluded coins could be more efficient, or some kind of runlength encoding. It’s a pretty straightforward compression problem. (These alternative forms could be useful for operator-initiated checkpoints as well, although those are likely to be dense and random enough for bitmaps to be the most efficient representation).

---

**zmanian** (2018-05-07):

It’s worth mentioning that crypto-economic aggregate signatures impose a weak synchrony for safety assumption on clients.

Clients must be able to synch the root chain within the challenge period to detect false checkpoints and challenge them. Otherwise they could loose the ability to withdraw their coins.

---

**danrobinson** (2018-05-07):

Plasma Cash (like Plasma and indeed all state-channel-like designs) already depends on  a synchrony assumption for safety—you have to be online to respond to attempted withdrawals of your coins. We could sync up those delay periods so that it doesn’t impose any additional synchrony requirements on the user.

---

**kfichter** (2018-05-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/danrobinson/48/755_2.png) danrobinson:

> This makes me wonder why it should even be a requirement that Plasma XT checkpoints can only be operator-initiated.

This is a really good observation. Anyone could aggregate checkpoints, as long as they put up the required bond!

![](https://ethresear.ch/user_avatar/ethresear.ch/danrobinson/48/755_2.png) danrobinson:

> This might be a good reason to look at alternative ways of expressing the bitmaps in cryptoeconomic aggregate sigs.

The nice thing about this as that the EVM doesn’t even have to “understand” what the bitmaps represent. Someone could publish a bitmap along with the string “every coin ending with 2 or 3”, and it would (theoretically) work. Of course we’d rather have some semantics that the Plasma Cash client can understand, but it shows what options we have.

---

**danrobinson** (2018-05-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png) kfichter:

> The nice thing about this as that the EVM doesn’t even have to “understand” what the bitmaps represent. Someone could publish a bitmap along with the string “every coin ending with 2 or 3”, and it would (theoretically) work. Of course we’d rather have some semantics that the Plasma Cash client can understand, but it shows what options we have.

I think it eventually has to—you need to prove that the recipient of the checkpointing was on notice, so in the event of a challenge, the EVM needs to be able to evaluate whether the published representation of the set being checkpointed included a particular coin.

(Another reason evaluating these needs to be computationally simple is of course that every coinholder needs to interpret every checkpoint, at least sufficiently to know that their coins are not included in it.)

---

**kfichter** (2018-05-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/danrobinson/48/755_2.png) danrobinson:

> you need to prove that the recipient of the checkpointing was on notice

Makes sense, recipients *must* be able to know whether their coins are being checkpointed or not.

---

**danrobinson** (2018-05-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/danrobinson/48/755_2.png) danrobinson:

> If that works, then operators can’t even prevent users from checkpointing their state (although, since they can prevent users from transacting, this isn’t a particularly significant win).

Actually, you could probably use this for a mass move from one Plasma chain to another that doesn’t require the cooperation of the first chain operator. So you could maintain the liveness of your Plasma Cash coins even if the operator goes rogue, at the on-chain cost of only around 1 bit per coin. So efficient mass checkpointing, [mass exit](https://ethresear.ch/t/optimistic-cheap-multi-exit-for-plasma-cash-or-mvp/1893/3), and moving could all be enabled by basically the same mechanism.

---

**yuzushioh** (2018-05-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png) kfichter:

> If more than this max number of challenges are open at any one time, then the checkpoint is invalidated. This basically ensures that not everyone needs to challenge and we don’t overload the root chain with challenges.

I am just curious what would happen or how would one handle the situation/attack when for example there are more people, who own their coin in the plasma chain and are malicious, than the max number of challenges (256) and submit invalid challenges at the same time. They might be able to invalidate the correct checkpoint by doing.

---

**kfichter** (2018-05-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/yuzushioh/48/1120_2.png) yuzushioh:

> They might be able to invalidate the correct checkpoint by doing.

Yeah, unfortunately this is a part of the design. The cost of this attack is 256 * bond, so we just need to parametrize the bond such that this attack isn’t worth it.

---

**peara** (2018-05-09):

What about using a bloom filter?

Users are only allowed to checkpoint their coins, maybe limited at 200 coins at a time. With a bloom filter of 8000 bits and 10 hash functions, the collision rate is 1/3000000. If the total number of coins is less than 1 billion, I think this is usable.

---

**kfichter** (2018-05-09):

My main problem with bloom filters here is that we could get an accidental “1” (false positive). In that case, the operator would lose a bond. I need to check the math on how to parameterize the bloom filter to be more efficient than 1bit/exit, but I have a feeling it might not be worth it.

---

**peara** (2018-05-09):

Assume that the submitted Merkle root is from a Sparse Merkle Tree like in Plasma Cash, in case of a false positive, the operation just need to submit a non-inclusion proof for that, isn’t it?

---

**peara** (2018-05-09):

I think the design can be changed a bit.

Only users can checkpoint their own coins. The plasma contract will stored successful checkpoint, one per address, as `[blockNumber, merkle_root, bloomfilter, exceptions]`. Then user only need to store history of their coins from `blockNumber`, start with a Merkle proof for the checkpoint.

The drawback is the cost for checkpointing might be high. Especially if there are too many false-positive in the bloomfilter.

---

**ldct** (2018-05-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/peara/48/1293_2.png) peara:

> Only users can checkpoint their own coins

I would worry that this loses performance in the case where there are say 2^{20} \approx 10^6 users each owning one coin; ideally one would like them all to create a checkpoint with 1 merkle root and a 20-bit aggregate signature, but with the new restriction you must create 2^{20} checkpoints on-chain

---

**kfichter** (2018-05-09):

Allowing users to checkpoint their own coins will probably be a special case of the checkpoint anyway.  There’s no reason why someone else (not the operator) can’t submit a checkpoint, so it makes sense that if the operator is misbehaving, then users might submit checkpoints for themselves. This gets more efficient as the number of coins per user increases.

---

**danrobinson** (2018-05-09):

I just realized that a similar mechanism is alluded to on page 5 of the [original Plasma paper](https://plasma.io/plasma.pdf) as a mitigation to the mass exit problem:

> These fraud proofs enforce an interactive protocol of fund withdrawals. Similar to the
> Lightning Network, when withdrawing funds, the withdrawal requires time to exit. We
> construct an interactive game whereby the exiting party attests to a bitmap of participants’
> ledger outputs arranged in an UTXO model which requests a withdrawal. Anyone on the
> network can submit an alternate bonded proof which attests whether any funds have
> already been spent. In the event this is incorrect, anyone on the network can attest to
> fraudulent behavior and slash the bonds to roll back the attestation. After sufficient time,
> the second bonded round allows for the withdrawal to occur, which is a bond on state
> before a committed timestamp. This allows for a withdrawal en masse so that a faulty
> Plasma chain can be rapidly exited. In coordinated mass withdrawal events, a participant
> may be able to exit with less than 2-bits of block space consumed on the parent blockchain (i.e. root Ethereum on-chain in worst case scenarios).

This design still does have the problem that someone can be forced to respond on-chain to an off-chain challenge without receiving a bounty (which isn’t a problem for Plasma XT if it’s just used for checkpointing on Plasma Cash).

---

**tawarien** (2018-05-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png) kfichter:

> My main problem with bloom filters here is that we could get an accidental “1” (false positive). In that case, the operator would lose a bond. I need to check the math on how to parameterize the bloom filter to be more efficient than 1bit/exit, but I have a feeling it might not be worth it.

My suggestion would be to invert the bloom filter. First provide a description of all coins allowed for inclusion into a certain checkpoint.

For example: all coins or coins which id starts with 00 etc…

Then provide a bloom filter that contains all coin ids from the set for which **no** signature is present. This has the benefit that on a false positiv in the bloom filter a valid signature is discarded (instead of the generation of an invalid one) which is indistinguishable from the situation where the owner has never created it and as such, no problem arises from a false positiv.

Another aspect is that the bloom filters size is related to the coins that are **not** signed (but could have been) in a checkpoint instead of to the ones that are meaning if their is a high participation rate then the bloom filter can be very small

---

**kfichter** (2018-05-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/tawarien/48/302_2.png) tawarien:

> Another aspect is that the bloom filters size is related to the coins that are not signed (but could have been) in a checkpoint instead of to the ones that are meaning if their is a high participation rate then the bloom filter can be very small

Yep, this could be an interesting optimization. I’d be very curious to see what kind of participation checkpoints have! My guess was we’d actually see pretty limited participation.


*(14 more replies not shown)*
