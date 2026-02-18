---
source: ethresearch
topic_id: 966
title: Cryptoeconomic "ring signatures"
author: vbuterin
date: "2018-01-30"
category: Proof-of-Stake > Block proposer
tags: [ring-signatures]
url: https://ethresear.ch/t/cryptoeconomic-ring-signatures/966
views: 7380
likes: 8
posts_count: 43
---

# Cryptoeconomic "ring signatures"

[@JustinDrake](/u/justindrake) has a proposal to use ring signatures to make a private-lookahead block proposer [here](https://ethresear.ch/t/fork-choice-rule-for-collation-proposal-mechanisms/922):

1. During epoch N-1, any validator can submit a linkable ring signature proving they are a validator into the chain
2. The ring signatures are randomly shuffled
3. During epoch N, the ring signatures are randomly shuffled, and validators can reveal the private data used to make the signature, thereby revealing that they created some given ring signature and so that they have the right to create a block at some given time

Here is an alternative that’s purely hash-based. Suppose we have two hash functions, H1 and H2, eg: H1(x) = SHA3(0x01 + x), H2(x) = SHA3(0x02 + x). Assume the existence of functioning and highly efficient mixers (eg. coinjoin). When validators join, they are required to commit, using some mechanism using hash function H1 (possibly a Merkle tree), to a mapping i \rightarrow V_i where V_i is the secret number that they will need to reveal during epoch i.

During epoch N-1, anyone can submit a value into the chain, along with a medium-sized deposit (eg. 100 times the staking reward); the intention is that they submit H2(V_N). The submitted values are shuffled. During epoch N, a validator can reveal that they have a right to create a block by submitting V_N, along with a proof (eg. Merkle branch) for the commitment. V_N can be checked against the previously submitted hash directly, and the commitment can be checked; both checks must pass for the block to be valid and for the validator to recover their deposit.

Note that even if the validator’s block does not make it into the chain, the validator can get their deposit back at any point in the future by submitting a suitable V_N and proof. It is possible for anyone to “clog up” the system by submitting invalid values, but this is expensive; the only non-money-losing strategy, aside from not participating, is to submit the single correct value for H2(V_N) during epoch N-1.

I suspect it may be possible to create a ring sig alternative that’s *purely* hash-based, because we are dealing with an easier problem: it’s ok for the link to be revealed during the second step, so it’s more like a “ring hash” than a “ring signature”; will keep thinking more about this. Maybe there’s something in the existing commitment scheme literature?

## Replies

**denett** (2018-01-31):

I like the scheme, but don’t we get a lot of overhead transactions in each block?

If we have like 2000 validators we will get 2000 secret numbers per per epoch. For relatively fast finality we probably want an epoch in the order or 100 blocks, that will result in 20 transactions per block.

Maybe better to use the secret numbers for 10 epochs in a row. Then you only get 2 transactions overhead per block without losing a lot of privacy.

---

**vbuterin** (2018-01-31):

> Maybe better to use the secret numbers for 10 epochs in a row. Then you only get 2 transactions overhead per block without losing a lot of privacy.

The problem is that after the connection between the secret and the sender is revealed in the first epoch, it’s no longer private for the remaining nine.

---

**denett** (2018-01-31):

Sorry I was not clear. I mean that you start with 2000 secret numbers. Shuffle them randomly and use 1000 of them spread over 10 blocks using 100 secret numbers each. After 10 blocks you start over with 2000 new secret numbers.

---

**vbuterin** (2018-01-31):

Even still, if the commitments to 10 secret numbers are given in one deposit, and one of those secret numbers is then tied to an account, you know that the 9 other numbers are also probably tied to that account.

---

**JustinDrake** (2018-01-31):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> During epoch N, a validator can reveal that they have a right to create a block by submitting V_N, along with a proof (eg. Merkle branch) for the commitment

Won’t two such proofs for the commitment (H1-Merkle branches) share the same H1-root, hence an immediately proposed block will be associated with previously proposed blocks by the same validator?

---

**vbuterin** (2018-01-31):

> hence an immediately proposed block will be associated with previously proposed blocks by the same validator?

Yes. There’s no lookbehind privacy here; everything is revealed the moment the block is broadcasted.

---

**iddo** (2018-01-31):

You can have H2 without H1 by using signatures instead?

If the validator set of epoch i-1 is {pk_1, pk_2, …, pk_t} then the jth validator can send H2(sign_{sk_j}(epoch i)), and later create the block by sending the preimage (i.e., the signature sign_{sk_j}(epoch i)).

You need to send H2 from another account, but that’s true in the scheme with H1 too, so the usefulness of this idea isn’t so clear because of linkability analysis?

With signatures, the same validator can then send H2(sign_{sk_j}(epoch i+1)) without extra interaction, and so on (assuming a randomized signature scheme, otherwise you can add nonce).

This works even if the validators are selected from the global stake and didn’t commit to anything in advance, unfortunately the overhead is large, and with lookbehind privacy and linkable ring signatures (the scheme of Justin Drake) the overhead is even larger.

The private scheme with honest forks has somewhat better anonymity because only the validator knows that he’s participating in the epoch (but doesn’t have  lookbehind privacy so the anonymity is incomparable to the ring signature scheme). Support for light clients is possible but it’d need interleaving of more than one epoch.

---

**denett** (2018-01-31):

Every validator sends just 1 secret number.

So we have 2000 validators with all the same deposit amount, every validator sends in 1 secret number before epoch 10N. 100 numbers are used in epoch 10N, 100 numbers are used in epoch 10N+1, … ,100 numbers are used in epoch 10N+9. A secret number is only used once, so we have used a total of 1000 numbers in 10 epochs. The other 1000 will not be used. Before epoch 10N+10 we have received 2000 new secret numbers and we start over.

So only 5% of the validators will get a block in an epoch. This is not enough to reach finality if we are using blocks as votes, so we will need to use the current Casper scheme or something like you proposed in [this post:](https://ethresear.ch/t/initial-explorations-on-full-pos-proposal-mechanisms/925)

*“When a block is created, a random set of N validators is selected that must validate that block for it to be possible to build another block on top of that block. At least M of those N must sign off.”*

For simplicity I used equal deposits, but we can allow validators with bigger deposits to send multiple secret numbers. These numbers must off course be send in different transactions for them to be unlinkable.

---

**JustinDrake** (2018-02-01):

Below is a construction which incorporates ideas from the linkable ring signature scheme and the above cryptoeconomic hash scheme. It has the benefit of simultaneously providing lookbehind privacy (in addition to lookahead privacy) and not relying on linkable ring signatures.

**Construction**

When validators join they commit (e.g. with a Merkle tree) to a mapping i \mapsto V_i where the V_i are secret. During epoch N-1 anyone can submit a collaterised pair (E, V_N) where E is an ephemeral key and V_N is meant to be the appropriate committed secret. The pairs are shuffled to form a random ordering of the ephemeral keys, one ephemeral key per period. We distinguish two scenarios:

1. The number of pairs is no greater than the number of validators. In this case proposing a block only requires signing with the ephemeral key for the corresponding period. Here the collateral is immediately returned.
2. The number of pairs is greater than the number of validators. In this case proposing a block additionally requires a proof that the purported V_N matches a validator commitment. Here the collateral is only retrievable if such a proof can be provided.

**Discussion**

The above scheme provides lookbehind privacy in scenario 1) but not in scenario 2). To disincentive scenario 2) it suffices to make the collateral large enough so that submitting a “fake” pair (i.e. one where V_N cannot be matched to a validator commitment) has highly negative expected returns.

If fake pairs go through in scenario 1) the only harmed parties are the validators who have effectively forgone their proposer rights to non-validators crazy enough to risk submitting fake pairs.

---

**iddo** (2018-02-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Below is a construction which incorporates ideas from the linkable ring signature scheme and the above cryptoeconomic hash scheme.

This cryptoeconomic mixing was discussed in 2016, see for example [here](https://github.com/yaronvel/smart_contracts/tree/master/mixer). You don’t need the new mapping, it’s enough to submit E with collateral and if the number of submissions is greater than the validators then each validator will need to endorse the E that he submitted when he creates a block and thereby not lose the collateral (maybe it’s better not to shuffle in this case). Other than the overhead, if the collateral is large then it’d be demanding on honest validators (time value of money), and if the collateral is small then one malicious submission can deanonymize everyone.

---

**vbuterin** (2018-02-01):

This scheme is basically layering coinjoin into the block proposal algorithm; interesting…

I do wonder what the metagame of non-validators guessing how many validators and how many other non-validators will be participating at any given point would play out… it seems like it would probabilistically hit an equilibrium where the non-validators with the best knowledge would in expectation be earning slightly more than zero, and most of the time the number of pairs will be less than the number of validators. Though perhaps cartels might find a way to exploit the system…

---

**JustinDrake** (2018-02-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/iddo/48/669_2.png) iddo:

> This cryptoeconomic mixing was discussed in 2016, see for example here.

Thanks for pointing this out. And BTW, it’s great to have you on ethresear.ch ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) I’ve been following some of your work on STARKs.

![](https://ethresear.ch/user_avatar/ethresear.ch/iddo/48/669_2.png) iddo:

> You don’t need the new mapping, it’s enough to submit E with collateral

Good point!

![](https://ethresear.ch/user_avatar/ethresear.ch/iddo/48/669_2.png) iddo:

> Other than the overhead, if the collateral is large then it’d be demanding on honest validators (time value of money)

My suggestion is to have a large collateral. I’d argue the time value of money is already compensated by having the right to propose a block. See below for an additional way to compensate honest validators via redistribution of collateral.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> the non-validators with the best knowledge would in expectation be earning slightly more than zero

My gut feel is that we can force negative expectation for all non-validators regardless of local knowledge. Below are two improvements to the mechanism design:

1. In scenario 2) redistribute collateral that has been untouched for a long enough period (say, 1 month) to the honest validators in the corresponding epoch. This way honest validators have an additional incentive to “fish” non-validators, including via “bluffing” (skipping a few periods to make it look like there are inactive validators, and then when a non-validator tries to exploit that then hit them hard by also joining in).
2. To make the above even more effective, allow for post facto (after the epoch has started) validator commitment proofs to count towards the total pairs count. This also has the benefit of removing the position of power the last miner corresponding to the previous epoch has to add non-validator pairs up to the threshold.

Both the risk of bluffing and the risk of post facto whistleblowing act like a Damocles sword to non-validators.

---

**iddo** (2018-02-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> I’ve been following some of your work on STARKs.

Thanks:)

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> My suggestion is to have a large collateral. I’d argue the time value of money is already compensated by having the right to propose a block.

The additional collateral for mixing makes the rewards less attractive even for large stakeholders. It’s possible to claim that they should settle for less lucrative rewards (and more blockchain bloat for all full nodes) because they’d have better security, but it’s a questionable claim in general and here also due to linkability analysis between the accounts that submit ephemeral keys and the validators’ accounts (also light client support might be more secure without mixing). Besides time value of money, the larger collateral raises the bar so smaller stakeholders cannot participate, which has negative implications on decentralization.

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> vbuterin:
>
>
> the non-validators with the best knowledge would in expectation be earning slightly more than zero

If I understand correctly what you guys are saying, it’s about a non-validator who gambles that not all the validators will submit ephemeral keys for the mix, so if his gamble pans out then he creates a block and earns a reward, otherwise he loses his collateral. In the variant without lookbehind privacy this gamble is useless because you have prove that you’re a legit validator when you create the block. It isn’t really clear to me why lookbehind privacy is desirable in this context. The arguments in favor of privacy for block creators are 1) less potential for a collusion attack, and 2) less potential for DoS on a validator when he tries to submit the block that he created during his timeslot. These arguments are debatable (since there are advantages with non-private block creators), but either way it seems that lookbehind privacy is irrelevant.

---

**kladkogex** (2018-02-02):

A coin tossing scheme (“common coin”) is where parties in round X agree on a random number. I suspect that running  commoncoin at each round will satisfy the lookahead privacy as defined here. The parties can use a deterministric threshold signature

to sign the current block number,  the hash of the signature will determine the blockproposer. The block proposer  will include the signature when submitting the block.

The mathematical question really is whether one can design a better common coin algorithm assuming presence of a blockchain. I strongly suspect that what we are discussing here can be reformulated as common coin with some additional assumptions.

One possibility would be to use the common coin algorithm of

[Micali](https://people.csail.mit.edu/silvio/Selected%20Scientific%20Papers/Distributed%20Computation/BYZANTYNE%20AGREEMENT%20MADE%20TRIVIAL.pdf) which is used in Algorand.

With block chain you could make it simple in the following way: Micali algorithm is using regular signatures. Instead of signatures,  each validator could hash a random number R N times in a chain sequence where N is the number of blocks in an epoch. The resulting hash

Then at each block, each validator would reveal a next level pre-image in the hash chain. This pre-image would be used as a signature in Micali algorithm to derive a random bit. So the blockchain would essentially be used to implement one-time signatures and plug them into the Micali algorithm.

---

**JustinDrake** (2018-02-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/iddo/48/669_2.png) iddo:

> It isn’t really clear to me why lookbehind privacy is desirable

Lookbehind privacy is desirable to limit adaptive attacks. Below are various examples, though imagination is the limit when it comes to adaptive attacks:

- Miners in the main shard responsible for including collation header in blocks can decide (e.g. through bribing or collusion) to not include collation headers based on the identity of the proposer. Without lookbehind privacy this attack is facilitated because the proposer’s identity would be leaked at the time of collation proposal. This is at best a discouragement attack, and could be used for censorship or consensus attacks.
- Validators in the child shard can decide (e.g. through bribing or collusion) to not build upon specific collation header chains based on the identity of the corresponding proposers, i.e. go against the default fork choice rule. This could be used to increase the probability of a collation header chain reorg, e.g. for the purpose of discouragement, censorship or consensus attacks.

---

**denett** (2018-02-02):

A block proposer solution that has both lookahead and lookbehind privacy can be achieved via something like a “block coin”

It basically works as follows:

- The block coin is an ethereum coin that will be fairly distributed among the validators based on the deposit amount.
- The validators can use coinjoin/mixers so nobody knows who owns which block coin.
- A block coin can be used to put one ephemeral key into the waiting set.
- For every block a random ephemeral key is drawn from the waiting set that can be used for signing the block.

There are some details to be filled in like:

- How many block coins do we want in distribution? To little and the mixers won’t work. To many and validators can hoard them and use them all at once to have temporary more influence.
- Coins tend to get lost, we do not want to run out of block coins. So maybe let the block coins expire after a certain time and be redistributed among the validators.

As an added bonus we can have the shard collation proposers be drawn from the same waiting set.

---

**kladkogex** (2018-02-02):

Looks like this is related to Mental Poker protocols - essentially you use crypto to securely shuffle cards,  so that until a party reveals her card other parties do not know which party has which card

[Mental Poker](https://en.wikipedia.org/wiki/Mental_poker)

---

**iddo** (2018-02-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Lookbehind privacy is desirable to limit adaptive attacks. Below are various examples, though imagination is the limit when it comes to adaptive attacks:

These scenarios seem just as plausible without lookbehind privacy, the attackers can always censor the block that was created if they don’t like the contents of the block, the only distinction with lookbehind privacy is that the attackers cannot censor the block just according to the identity of the proposer who created the block. If Alice and Bob are proposers who would create the same block, then the contents of the block are likely to be much more relevant for censorship attacks (rather than the identities Alice/Bob). Also, with lookbehind privacy in place, maybe the attackers have nothing against the validator identity but don’t like the account that submitted the ephemeral key E so they’d censor the block that E created (as you say imagination is the limit). If you think that cartel censorship is a significant concern then there are more important design choices, namely not relying on a mostly static set of validators who’d create blocks in the next epochs.

---

**kladkogex** (2018-02-02):

So here’s how this can be done using Mental Poker [see (this article for details)](http://crpit.com/confpapers/CRPITV21AZhao.pdf)

1. Each validator has a commutative encryption key
2. Each validator encrypts the sequence of numbers 1,2,3,4,5,6,7,8 … using commutative encryption. As a result, each number gets encrypted by keys of all validators, and the resulting value is stored in a smartcontract.
3. The encryptions are shuffled so each validator V is dealt an encrypted value E. For each encrypted value, all other validators decrypt the value. The result y is then passed to V, who decrypts it using its private key and gets the plaintext number x
4. At this point everyone has been dealt a plaintext number, but no one knows numbers assigned to other parties.
5. At the time when a block needs to be proposed by a particular validator,  the validator submits a proof proves that y is an encryption of x

This is in fact, similar to what Justin proposed, but uses commutative encryption to make things more secure.

---

**iddo** (2018-02-02):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> So here’s how this can be done using Mental Poker

It’s useless here because the mix doesn’t need to output private randomness, only public randomness. So it’s enough to use collective coin flipping (or secure coin flipping with honest majority) with or without cryptoeconomics.


*(22 more replies not shown)*
