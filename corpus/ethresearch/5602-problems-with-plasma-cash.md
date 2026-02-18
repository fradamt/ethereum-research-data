---
source: ethresearch
topic_id: 5602
title: Problems with Plasma Cash
author: kladkogex
date: "2019-06-11"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/problems-with-plasma-cash/5602
views: 2959
likes: 0
posts_count: 4
---

# Problems with Plasma Cash

Here are some usability and security problems that in my humble opinion do not make Plasma Cash fit for real life.  Theoretical constructions is one thing, real life product that satisfies product-market fit is totally another thing.

1. The entire idea of mass exits is infeasible.  For a Plasma chain of 100 million users, it would take  10(!) years for all of users to exit having the current state of the main net.  The gas fees would go enormously high during this period of time.
2. Non-inclusion proofs grow linearly with time.  If the proof size is 1K and block time is one second, a coin which is 10 year old needs 300GB of a proof.  Paying with 10 coins and receiving 10 coins of change back then amounts to transferring 6TB(!) of proof per transaction. Try this with your internet provider. A single payment would take days in this situation.
3. Users are required to download process and verify gigabytes of Merkle roots per transaction.
4. Payments are extremely hard to make because the receiving party needs to have the exact change, and there is no way to split the coins.
5. There is no one economically interested to prevent self-spent-coin challenges.  In particular, one can make one billion utxos by just paying the same $1000 coin to yourself.
Then out of these UTXOs one can randomly try exiting 1000 of them to make $1M.

Since there is no counterparty, one can only rely on third party “validators” to catch the thief. But these “validators” can be bribed by the thief, and it is enormously hard to become a “validator”, since you need to have the history of the chain FROM THE BEGINNING OF TIME.  In fact, a Plasma chain plus 10 “validators” is not much different to a side chain.

1. The economic model for the “validators” is not feasible.  One cant pay policemen a share of thiefs money, otherwise police departments in cities like Palo Alto, would become bankrupt.  If a particular Plasma chain has no fraud attempts for a while, the “validators” will lose their source of income, and will have to simply purge the multi-terabyte data stores they need to protect the chain.

## Replies

**benj0702** (2019-06-11):

My thoughts on these:

1. This would be correct (though the numbers are off–would take more like 10 days using this) intuition for a mass exit using regular exits, but is solved by cooperative migrations–users cooperatively can exit many coins succinctly, exiting a merkle root of those states directly into a deposit for another plasma chain.
2. Your estimates are big here, for an exclusion proof to be 1K that would be a block with 2^32 = 4 billion transactions.  4 Billion state channel rebalances is a crazy big block.  Though yes, the linearity will need addressing (in time).  Cooperative checkpointing schemes and ZKPs both can solve it.
3. Not sure if you’re referring to the issues in #2 again?  Otherwise transactions are just a merkle proof.
4. This has been solved for many months with plasma cashflow.
5. False, this is the whole point of plasma cash–that attack is impossible, only the first $1000 exit is finalizable.  (MVP has this attack but not cash)
6. Not applicable because of 5.  However note that watchtowers in general can take a fee over time, not just disputes.

---

**sina** (2019-06-12):

There are some good criticisms mixed in along with some conflations of different ideas. I’ll try to address these as if you’re referring to Plasma Cash and the space of various derivatives. In the below points, if I say “Plasma Cash”, please read it as “Plasma Cash, and variants” ![:slightly_smiling_face:](https://ethresear.ch/images/emoji/facebook_messenger/slightly_smiling_face.png?v=12).

> Mass exits

1. I believe Plasma Cash variant constructions eliminate the need for mass exits[0]. You may be thinking a different flavor of Plasma? I agree that this can get confusing . My understanding is that in Plasma Cash, a user never needs to exit their coins to keep them secure, it’s only when someone else tries to invalidly exit your coins that you need to contest their exit before the challenge period ends.

> History proofs are big

1. There are various explorations into how to mitigate history sizes, from Plasma XT[1] checkpointing to various crypto-magic techniques including RSA accumulators[2] and various zk-s*ark techniques[3][4][5] that do things like reduce the history proof size or even eliminate its need.

> Verifying a transaction is expensive for the receiver

1. Maybe this is the case for some Plasma variants, but not for others. If you point out a specific case of this for a specific Plasma variant, there has probably research that has progressed that I can point you to that makes the situation a bit better . Off the top of my head, for Plasma Cash, I think basic Plasma Cash would entail this kind of processing to validate the history of coins being sent in a transaction, but there are improvements I’m discussing in the other points that make this simpler.

> Incremental payments aren’t solved

1. See Plasma Debit[6] along with the various “coinslots are a numberline, send and own them as intervals/fragments” variants of Plasma: Plasma Prime[7], Plasma Cash Flow[8], etc. The upshot is that there are various ways to handle this in the works.

> People can steal money that isn’t theirs

1. In Plasma Cash variants (which seems to be what this post is about), every UTXO that is backed by an asset on-chain is owned by a user off-chain. That user is responsible for challenging any faulty exits of their assets within the challenge period.

> Being a validator isn’t feasible

1. I’m not sure what you mean here, it seems you think that validators only get paid when bad exits are challenged, which isn’t true. I believe that most of these variants we’re talking about entail fee payments to the operator of either small increments for the variants that easily allow that, or probabilistic payments of slightly larger increments for variants where small payments are harder.

There’s a lot here spanning a huge timeline of Plasma research that has gone on, and I’m not 100% that I interpreted each of your questions correctly, so forgive me if I slipped up in a few spots; happy to discuss anything that’s unclear.

All-in-all, I think the best criticisms are of user synchrony/liveness requirements (to challenge invalid exits) and large history sizes. That being said, I think there’s a path with zk-magic and coin-interval-style variants to take care of the history size, and most users have cellphones that are always online that could easily check once-per-week that all of a client’s coins are safe (plus you could do something like watchtowers). Given this, I’m fairly confident in the state and direction of Plasma.

[0] From https://www.learnplasma.org/en/learn/cash.html: “Plasma Cash was originally designed to address the mass exit problem in Plasma MVP.”

[1] [Plasma XT: Plasma Cash with much less per-user data checking](https://ethresear.ch/t/plasma-xt-plasma-cash-with-much-less-per-user-data-checking/1926), basically checkpoints being posted on-chain that, once accepted, imply any prior history (ie. the user doesn’t need to keep any copies of history that is implied by the checkpoint)

[2] [RSA Accumulators for Plasma Cash history reduction](https://ethresear.ch/t/rsa-accumulators-for-plasma-cash-history-reduction/3739)

[3] [Validity Proofs + Plasma Cash = Simpler Exit Game/Coin History?](https://ethresear.ch/t/validity-proofs-plasma-cash-simpler-exit-game-coin-history/5333), basically using zk-s*arks to reduce the history size requirements dramatically.

[4] [Minimal fully generalized S*ARK-based plasma - #6 by vbuterin](https://ethresear.ch/t/minimal-fully-generalized-s-ark-based-plasma/5580/6)

[5] [Non-inclusion zkSNARK for Plasma Cash and Cashflow history compaction](https://ethresear.ch/t/non-inclusion-zksnark-for-plasma-cash-and-cashflow-history-compaction/4543)

[6] [Plasma Debit [ Learn Plasma ]](https://www.learnplasma.org/en/learn/debit.html) - Plasma Debit solves the issue you’re describing by making each Plasma Cash “token” slot into a payment channel with the operator. Now, paying Alice a fraction of your token becomes easier, as you can use the operator as a proxy for any increment desired (simplifying a bit)

[7] [Plasma Prime design proposal](https://ethresear.ch/t/plasma-prime-design-proposal/4222)

[8] The best link I could find was this YouTube video: https://youtu.be/-8Jp7VjspQE ; but essentially, treat the space of all coin slots as a number line, and any adjacent coins you own/send can be considered a single “fragment” that can be treated as one larger coin that is the aggregate of the values. You can now eg. split this interval of coins to send only some of them, or exit them all at once.

---

**kladkogex** (2019-06-12):

Guys - thank you for your comments. Sorry I mistakenly brought up the self-payment things - this is related to Plasma MVP not Cash, you are totally correct.

Other than that here is a subjective digest of your responses above.

1. Plasma is still in the research phase, so people claiming to run secure production versions of plasma now should not really do it. They also should not claim one can run EVM on Plasma, since shared state of smart contracts is not really exitable.  There are projects now in the wild that claim to run Plasma and claim to run EVM on it, without providing much of a spec of a security model.
2. The large witness sizes and the fact that users have monitor their coins are the too largest problems, based on your comments above.

Economically, most users will arguably want to pass monitoring to trusted third parties. Arguably, The idea of monitoring your coins yourself is a hard sell with most consumers …

So ironically the economic evolution may end up with something not much different than a sidechain, if 2-3 leading monitoring parties will be left on the  market, and then this will essentially be equivalent to a side chain with 2-3 “validators”, where the monitoring party is a “validator”.

1. Re:ZKSNARKS/ZKSTARKS I agree it is a promising direction to shorten non-inclusion proof sizes.
We looked at this at SKALE  about 3 months ago, at that time there was not much we could use with reasonable performance characteristics.  Proof generation times and computational power required are really bulky, for ZKSNARKS/STARKS, even if you do a simple thing like a single SHA-1 computation. The estimates we did at the time one would have to  run proof generation for days and weeks.  We are really interested in ZK things as a research direction, but were not able to find anything we could use at SKALE immediately to give us a competitive advantage.  At SKALE we are a startup, we dont do academic research, instead we try to wait and use things once they mature more or less …
2. I dont know much about Plasma Cashflow. I guess someone needs to do a write up how Plasma Cashflow would modify the spec that Karl proposed. The problem of paying change back is pretty big I think.

Overall, I think the idea Vitalik suggested to have a limited version of Plasma on a sidechain, like a secure vault, where people would hold small number of really-really–large-value coins does make sense. May be thats the direction to go having that the processing power of the main net is very limited  now …

