---
source: ethresearch
topic_id: 999
title: Private lookbehind for logs
author: JustinDrake
date: "2018-02-04"
category: Sharding
tags: []
url: https://ethresear.ch/t/private-lookbehind-for-logs/999
views: 3215
likes: 3
posts_count: 18
---

# Private lookbehind for logs

This post continues the exploration of a core theme in the [sharding category](https://ethresear.ch/c/sharding) around the separation of ordered data (called “logs”) and state. We detail a protocol-level collation proposal mechanism where logs benefit from short-term private lookbehind. Short-term private lookbehind is meant to be a general approach to curb short-term adaptive attacks (censorship, collusion, bribes, blackmail, discouragements, …).

Progress has been made designing private proposal mechanisms (see [here](https://ethresear.ch/t/fork-choice-rule-for-collation-proposal-mechanisms/922) for a scheme with private lookbehind). As [noted by @iddo](https://ethresear.ch/t/cryptoeconomic-ring-signatures/966/19) the privacy of these mechanisms extends only as far as the collation header, not the collation *body*:

![](https://ethresear.ch/user_avatar/ethresear.ch/iddo/48/669_2.png)[Cryptoeconomic "ring signatures"](https://ethresear.ch/t/cryptoeconomic-ring-signatures/966/19)

> attackers can always censor the block that was created if they don’t like the contents of the block

We seek to address that concern.

**Construction**

For the purpose of simplicity we assume [log shards](https://ethresear.ch/t/log-shards-and-emv-abstraction/747) where collation bodies consist fully of logs (the scheme extends more generally). To propose a collation body B a validator does the following:

1. Keeps B secret and broadcasts the time-lock encryption E(B) of B with a time-lock set to LOG_LOOKBEHIND_PERIODS
2. Includes a short zk-proof in the collation header that E(B) is the faithful time-lock encryption of a collation body B that produces a collation root matching the collation header

(An alternative to time-lock encryption is to have a cryptoeconomic scheme where the validator is highly incentivised to make the decryption key available onchain within a certain time period, similar to the [fair exchange without a third party](https://ethresear.ch/t/fair-exchange-without-a-trusted-third-party/255) construction.)

**Discussion**

The above construction allows for logs to benefit from short-term lookbehind privacy, i.e. the content of the logs is not immediately publicly disclosed. (Notice that users may have immediate private knowledge of the inclusion of the logs they care about, especially in the context where logs can be included in exchange for out-of-band compensation.)

By their nature, adaptive attacks may be a cat-and-mouse game between attackers and defenders (like ad blocking). Individual applications can setup their own mitigations, but having a global strategy *feels* like a big step in favour of defenders. Combining private lookbehind for both collation headers and collation bodies feels effective if `LOG_LOOKBEHIND_PERIODS` is set large enough to cover the time to reach some decent level of finality.

Notice the construction only naturally applies to logs (as opposed to transactions) because of the tight state coupling between transactions.

## Replies

**iddo** (2018-02-04):

If Alice creates the block B1 but first only publishes E(B1), and then Bob creates the block B2 that extends B1, then Bob can be damaged either by accident or by malicious behavior. For instance, Bob may include in B2 some complex transaction tx1 that spends a lot of gas and rewards him with a high fee, only to discover later (after E(B1) is decrypted) that the account that created tx1 has already depleted all of its ETH in another transaction tx0 that was included in B1, and therefore Bob wasted his block capacity on tx1 instead of other pending transactions that would have allowed him to earn revenues.

---

**JustinDrake** (2018-02-04):

“block”, “transaction”, “gas” are concepts native to the current paradigm where ordered data and state are tightly coupled. I find it helpful to think in the context of a log shard because that’s the extreme scenario (no state whatsoever), and it forces you to think differently.

![](https://ethresear.ch/user_avatar/ethresear.ch/iddo/48/669_2.png) iddo:

> to discover later (after E(B1) is decrypted) that the account that created tx1 has already depleted all of its ETH

This scenario doesn’t immediately apply because there is no native concept of ETH in a log shard (keeping track of account balances is a form of statefulness). One approach to compensating validators for inclusion of logs is via out-of-band payments handled elsewhere (e.g. in the main shard, or in some other stateful shard). I wrote a bit about this in the [“Transaction fees” section here](https://ethresear.ch/t/log-shards-and-emv-abstraction/747):

> The collation limit induces a fee market, and fees for inclusion of logs can be paid for out-of-band, e.g. using payment channels from users to validators. (I am exploring an offchain design similar to Raiden where users can pre-purchase generic “stateless gas” to trustlessly compensate any validator for including logs in collations. This is the topic of another post.)

In this model of out-of-band compensation you can also have private knowledge as noted in the original post:

> users may have immediate private knowledge of the inclusion of the logs they care about, especially in the context where logs can be included in exchange for out-of-band compensation.

---

**kladkogex** (2018-02-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Keeps BB secret and broadcasts the time-lock encryption E(B)E(B) of BB with a time-lock set to LOG_LOOKBEHIND_PERIODS

Nice simple idea!

How are you going to make sure that the format of plain text logs is not corrupt  ?))

As an toy example, lets assume that your logs are supposed to be in JSON format, but when decrypted they turned out to be binary format ?) So if the logs are supposed to be in a particular format, you also need a proof that plaintext is properly formatted.

Probably the way to solve this is to encrypt at a single message level, so essentially you have a list of encrypted values.

Another possibility is to have a rule where if a block turns out to be improperly formatted after decryption, it is considered void an ignored.

Another question is what time of  [time lock decryption](https://www.gwern.net/Self-decrypting-files) are you planning to use?

An interesting possibility would be to have a “useful”  time-lock encryption scheme that would work in the following way:

The time lock key would be derived by solving an efficient compression encoding problem for older blocks.  In other words,   as a byproduct of time-lock decryption you would compress older blocks and save storage.

Another possibility would be to somehow relate the time lock key to optimization/rebalancing of Merkle hashes or Merkle mountain ranges of older blocks.

---

**iddo** (2018-02-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> This scenario doesn’t immediately apply because there is no native concept of ETH in a log shard (keeping track of account balances is a form of statefulness).

Even if you could have good solutions to avoid damaging honest validators due to bad luck or malice, you still hurt the potential of low-latency blocks. With a dapp that uses data from the latest blocks to signal all its users, if only E(B) is published then you introduce extra latency (that privileged users could avoid by obtaining private knowledge of B).

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> In this model of out-of-band compensation you can also have private knowledge as noted in the original post:
>
>
>
> users may have immediate private knowledge of the inclusion of the logs they care about, especially in the context where logs can be included in exchange for out-of-band compensation.

Let’s say Alice is a user and she creates the transaction tx0, and Bob is a validator who includes tx0 in B and publishes E(B). Alice wants to give the private knowledge that tx0 was included in B to Carol and Dave. So first Alice needs Bob to prove to her that tx0 is really included in B, the easiest way is by sending B privately to Alice (if you want ZK proofs then we go down the rabbit hole). After that Alice sends the private proof to Carol and Dave, but it turns out that Dave has an incentive to give the private proof to the cartel of validators that’d censor E(B) because they don’t like tx0.

---

**kladkogex** (2018-02-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/iddo/48/669_2.png) iddo:

> Let’s say Alice is a user and she creates the transaction tx0, and Bob is a validator who includes tx0 in B and publishes E(B). Alice wants to give the private knowledge that tx0 was included in B to Carol and Dave. So first Alice needs Bob to prove to her that tx0 is really included in B, the easiest way is by sending B privately to Alice (if you want ZK proofs then we go down the rabbit hole). After that Alice sends the private proof to Carol and Dave, but it turns out that Dave has an incentive to give the private proof to the cartel of validators that’d censor E(B) because they don’t like tx0.

An alternative would introduce some kind of an online protocol, where a party first commits to including a block by signing the  Merkle root of the block, and only then the block itself is revealed to the party.  If the party censors out a block it previously committed to, her deposit is slashed.

---

**iddo** (2018-02-04):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> If the party censors out a block it previously committed to, her deposit is slashed.

Not sure what you mean by “the party”, there can be Sybil identities and collusion.

You shouldn’t slash a deposit willy nilly because you suspect that a block was censored, and you need to define precise rules. Maybe the validator was honest and only apparently censored the block that he didn’t see on time due to network lag (if you have a way to tell then you already solved distributed consensus).

---

**JustinDrake** (2018-02-04):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> How are you going to make sure that the format of plain text logs is not corrupt  ?

The collation body deserialisation process takes as input an arbitrary binary blob of data, and outputs an array of binary logs (splitting into logs can be done for example with an explicit `LOG_TERMINATOR`). There is no invalid input to deserialisation (other possibly than the binary blob being too large). As for the binary logs, these are also all valid by construction because they are not interpreted at the protocol layer.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> what time of  time lock decryption are you planning to use?

I am hoping something on the order of 1 minute would be sufficient. Dfinity-style committee-based  consensus allows for near-finality in a matter of seconds (and is something the Ethereum team is considering). It suffices for the time lock decryption to cover time to reach near-finality.

![](https://ethresear.ch/user_avatar/ethresear.ch/iddo/48/669_2.png) iddo:

> With a dapp that uses data from the latest blocks to signal all its users, if only E(B) is published then you introduce extra latency

Yes, there’s a fundamental latency tradeoff for fully public applications. The good news is that the added latency doesn’t have to be that high (see above). Many applications are either not fully public, or can tolerate a bit of latency. Note the scheme is *not* meant to be a one-size-fit-all solution; I am imagining some shards will want the lookbehind privacy enabled, and other shards will not.

![](https://ethresear.ch/user_avatar/ethresear.ch/iddo/48/669_2.png) iddo:

> So first Alice needs Bob to prove to her that tx0 is really included in B, the easiest way is by sending B privately to Alice

A far better way for Bob to prove to Alice that her tx0 is included in B is to share a Merkle proof from tx0 to the collation root. This proof is O(log n) vs O(n), and doesn’t leak much private information.

![](https://ethresear.ch/user_avatar/ethresear.ch/iddo/48/669_2.png) iddo:

> it turns out that Dave has an incentive to give the private proof to the cartel of validators that’d censor E(B) because they don’t like tx0

Yes, adaptive attacks have this cat-and-mouse property. A cartel of validators can even go as far as bribing for private information to leak. The scheme is not meant to eradicate adaptive attacks. Instead, it is intended to make adaptive attacks (much) harder, ideally to the point where the time to organise an adaptive attack (the “adaptation latency”) is higher than the time to finality.

---

**iddo** (2018-02-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> A far better way for Bob to prove to Alice that her tx0 is included in B is to share a Merkle proof from tx0 to the collation root. This proof is O(log n) vs O(n), and doesn’t leak much private information.

OK so you want to publish E(B) together with the Merkle root hash, where E is time-lock encryption and B is the full Merkle tree, and after E(B) is decrypted the protocol requires it to be consistent with the published root hash (time-lock encryption is supposed to ensure that the decryption can be done without relying on the proposer who published E(B), otherwise commit/decommit scheme is enough). Here is a non-exhaustive list of problems, 1) freeloading/incentive issues regarding whether all validators and full nodes should compute the time-lock puzzle on their own or rely on single points of failure that compute it for them, 2) if there are single points of failure then those can collude with the cartel that censors blocks, 3) an adversarial proposer can encrypt E(B) using a higher difficulty than what the protocol specifies, so that only he will know the solution in the time and he can do timing attacks and give the solution to specific validators and create forks, 4) timelock puzzles are insecure against an attacker that can do sequential computation faster, 5) decentralized proof-of-stake is supposed to be green and less costly than PoW but nodes that don’t rely on single points of failure will need do perform the intensive puzzle computations all the time.

---

**JustinDrake** (2018-02-04):

Thanks Iddo for analysing the scheme for weaknesses ![:+1:](https://ethresear.ch/images/emoji/facebook_messenger/+1.png?v=12)

To help me address some of your points let me propose a new hybrid construction that combines the time-lock encryption and commit/decommit schemes.

**New construction**

To propose a collation body B a validator does the following:

1. Keeps B secret and broadcasts the time-lock encryption E(B) of B with a time-lock set to LOG_LOOKBEHIND_PERIODS
2. Includes a short zk-proof in the collation header that E(B) is the faithful time-lock encryption of a collation body B that produces a collation root matching the collation header
3. Commits collateral promising to reveal the decryption key for E(B) in the time window LOG_LOOKBEHIND_PERIODS +/-  LOG_REVEAL_BUFFER

In the optimistic case the validator reveals the decryption key and decommits to receive the collateral back.
4. In the exceptional case the validator does not reveal the decryption key in the time window. Half the collateral is burned, and the other half is provided as a bounty to the first validator who constructs a collation revealing the decryption key.

Notice that in both cases data availability of B follows from the availability of E(B).

![](https://ethresear.ch/user_avatar/ethresear.ch/iddo/48/669_2.png) iddo:

> OK so you want to publish E(B) together with the Merkle root hash, where E is time-lock encryption and B is the full Merkle tree, and after E(B) is decrypted the protocol requires it to be consistent with the published root hash

Yes that’s right. That’s what I meant with “[…] that produces a collation root matching the collation header”.

![](https://ethresear.ch/user_avatar/ethresear.ch/iddo/48/669_2.png) iddo:

> freeloading/incentive issues regarding whether all validators and full nodes should compute the time-lock puzzle on their own or rely on single points of failure that compute it for them

In the new scheme computing the time-lock puzzle is the exceptional case, and should only be done by validators who want to receive the bounty. Validators and full nodes can now simply wait for the decryption key to be revealed, either by the original validator or the bounty hunter.

![](https://ethresear.ch/user_avatar/ethresear.ch/iddo/48/669_2.png) iddo:

> if there are single points of failure then those can collude with the cartel that censors blocks

I don’t think this applies in the new construction. See above; there are no single points of failure.

![](https://ethresear.ch/user_avatar/ethresear.ch/iddo/48/669_2.png) iddo:

> an adversarial proposer can encrypt E(B) using a higher difficulty than what the protocol specifies

This is not allowed by construction. When I wrote “the faithful time-lock encryption” for the zk-proof the word “faithful” encompasses proving the difficulty was set correctly.

![](https://ethresear.ch/user_avatar/ethresear.ch/iddo/48/669_2.png) iddo:

> timelock puzzles are insecure against an attacker that can do sequential computation faster

In the new construction this is largely irrelevant because brute-forcing timelock puzzles is the exceptional case, and the race is between validators only.

![](https://ethresear.ch/user_avatar/ethresear.ch/iddo/48/669_2.png) iddo:

> decentralized proof-of-stake is supposed to be green and less costly than PoW but nodes that don’t rely on single points of failure will need do perform the intensive puzzle computations all the time

The cost of PoW is addressed in the new scheme. There is no single point of failure, and nodes do not need to compute the costly timelock puzzle because the key will be revealed eventually.

---

**kladkogex** (2018-02-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/iddo/48/669_2.png) iddo:

> Maybe the validator was honest and only apparently censored the block that he didn’t see on time due to network lag (if you have a way to tell then you already solved distributed consensus).

Thats true … BTW if one uses asynhcronous consensus such as atomic broadcast, then as long as 2/3 nodes are good, the rest of the nodes can not censor things in any way. So atomic broadcast protocols are a good way to address censorship imho

---

**kladkogex** (2018-02-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Includes a short zk-proof in the collation header that E(B)E(B) is the faithful time-lock encryption of a collation body BB that produces a collation root matching the collation header

Is each log going to be signed by the party that submitted the log? I though that each log entry in the block would include a signature … Then a decrypted block would not be valid if the signatures for entries would not match …

If the encrypted blob is just a binary blob as you mentioned, then it seems that you could do it without zk-snarks.

You could do the following:

1. The decryption key could be  constructed by a series of consecutive memory-bound hashes, so it is hard to speed up this thing on a GPU
2. The block would be encrypted using authenticated encrypton (such as AES-GCM).   If during decryption the authentication phase of AES-GCM fails, then one would consider  the block as empty.

What I am saying is that zk-snarks are may be an overkill, if you find out that the block was not faithfully encrypted you could simply consider block contents empty …

---

**NicLin** (2018-02-05):

I might have missed some details here. But in the new construction wouldn’t the other validators or cartels have the incentives to censor the revelation of decryption key so they can then claim the bounty?

---

**kladkogex** (2018-02-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/niclin/48/1326_2.png) NicLin:

> might have missed some details here. But in the new construction wouldn’t the other validators or cartels have the incentives to censor the revelation of decryption key so they can then claim the bounty?

Here is an alternative:

If a validator does not reveal the key after a certain  number of blocks, one can simply assume the block to be empty - no bounties.

There is a bit of a problem with chain re-orgs - the validator needs to keep monitoring the chain to make sure that the key is revealed in the currently winning chain - this problem exists in the original proposal too …

---

**denett** (2018-02-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/iddo/48/669_2.png) iddo:

> decentralized proof-of-stake is supposed to be green and less costly than PoW but nodes that don’t rely on single points of failure will need do perform the intensive puzzle computations all the time.

If you require the next block to include the decryption key of the previous block, only one node has to do the PoW in case the decryption key was not released.

---

**iddo** (2018-02-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Includes a short zk-proof in the collation header that E(B) is the faithful time-lock encryption of a collation body B that produces a collation root matching the collation header

Possibly succinct NIZK will be better. The original RSA time-lock puzzle doesn’t necessarily need to have succinct proof, though the prover would need to show knowledge of prime numbers with primality test as part of the NIZK, which will be quite complex and expensive to put on the blockchain. The scheme with only commit/decommit is more practical, but still isn’t attractive for dapps that’d prefer small interval between blocks. Also it isn’t so clear whether your improve or harm the prospects of the cartel, for example the cartel can prevent you from submitting the decommitment into their blocks unless you give them a side payment so that you’d avoid losing your security deposit. As you say, you can implement a shard with this scheme for extra privacy, and there can be other shards without it, and we would see how many users prefer to use this scheme,

![](https://ethresear.ch/user_avatar/ethresear.ch/denett/48/2237_2.png) denett:

> If you require the next block to include the decryption key of the previous block, only one node has to do the PoW in case the decryption key was not released.

Without the ZK proof that the time-lock puzzle is well-formed the rules may specify that all nodes that follow the protocol should verify the puzzle, to discourage validators from submitting invalid puzzles. With the ZK proof you’re right, though it still isn’t so easy because the puzzle takes a long time to compute so the validator should start working on it ahead of time, so it may prefer to delegate this work to some other server (in proof-of-stake the validator can run on Raspberry Pi etc.). Also the validator may just decide that it’s too demanding to create a block when the decommitment wasn’t revealed, or just be inactive for whatever reason, and then the next validator would suddenly need to perform this work? And unfortunately the work required to create the ZK proof is also demanding (to put it mildly).

So this work has some resemblance to PoW in Bitcoin, because each validator needs to perform an intensive computation to create his block (in principle it’s less severe than Bitcoin’s PoW because the block creator needs to perform the computation only for his timeslot, in practice such NIZK isn’t possible yet).

---

**iddo** (2018-02-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> This post continues the exploration

Another problem: if some transaction tx0 is included in the Merkle tree of the block B_1  but the tree is hidden until it’d be decommitted later, then the validator that creates the next block B_2 doesn’t know whether tx0 is already in B_1 so he may include it again, which implies that there’d be wasteful duplicate data in the blocks…

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> NicLin:
>
>
> might have missed some details here. But in the new construction wouldn’t the other validators or cartels have the incentives to censor the revelation of decryption key so they can then claim the bounty?

If a validator does not reveal the key after a certain  number of blocks, one can simply assume the block to be empty - no bounties.

There have been (arguable) suggestions to punish inactive validators who didn’t create a block in their timeslot. Anyhow this mitigates but doesn’t remove the incentive of the cartel to censor the decommitment because the validator won’t earn his reward if he cannot decommit, so the cartel can demand a side payment or just include the non-decommitted transactions in their own blocks and earn more in fees.

---

**denett** (2018-02-06):

Maybe we could just skip the PoW part and if the decryption key is not released, the next validator will create a fork. This has to be disincentivized of course, maybe by some kind of reward sharing scheme. Now the block proposer will all ways release the decryption key, otherwise the block is just forked away.

p.s. This post was withdrawn for some reason, so I am reposting it.

