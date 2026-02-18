---
source: ethresearch
topic_id: 3187
title: Plasma chains with enforced consistency between multiple parent chains
author: vbuterin
date: "2018-09-02"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/plasma-chains-with-enforced-consistency-between-multiple-parent-chains/3187
views: 2285
likes: 5
posts_count: 10
---

# Plasma chains with enforced consistency between multiple parent chains

Suppose you want to have a Plasma chain with multiple parent chains, where the Plasma chain contains assets that come from all of these chains (this can be useful for applications like running a decentralized exchange between these assets, without requiring either chain to contain a light client of the other). At first this seems simple to implement: just put a Plasma root contract on each chain, and then have each contract recognize only the assets on the Plasma chain that corresponds to assets on that particular root chain.

But this leads to a problem: how do you ensure consistency between the root chains? For example, suppose that there is a Plasma chain with the ETH and ETC chains as roots, and ETH and ETC as the two assets. Suppose block X of the Plasma chain contains a transaction sending ETH from A to B and sending ETC from B to A (this is a decentralized exchange swap). A malicious operator colluding with B can attack by creating block X, then publishing the root into the ETH chain but *not* into the ETC chain (or publishing some alternative root X’ into the ETC chain that does not contain that transaction). This causes the ETH side to be fulfilled but not the ETC side.

We can solve this problem with [Lamport’s 99% fault tolerant consensus](https://vitalik.ca/general/2018/08/07/99_fault_tolerant.html). Suppose the Plasma chain has its own native currency, and deposits in the native currency form a proof of stake system, with bonded validators. We add the following rule. In order for one of the root chains to accept a block header, it must be signed by a validator; the index of the validator used is used as a randomness seed to pick out a random other 40 validators. The inclusion transaction must also specify an inclusion timestamp, T, and it must be submitted between time T and time T+D (eg. D = 1 hour). The same inclusion transaction can then be published into the other root chains within the same time window, or, if k validators from the random subset co-sign, it can be published into the other root chains before time T + k * D. If the block is included into one root chain, any honest validator can thus add their own signature and cause it to be submitted into the other root chains within the additional time window of D seconds by which their signature extends the deadline.

This does require a trust assumption of Plasma chain validators, but it is a very limited one, requiring only ~1-10% of validators to be honest depending on the risk tolerance level and the validator set size (it can be less or more than 40 as desired).

## Replies

**HarryR** (2018-09-02):

Lets take the case of proxy tokens, I don’t know what else to call them and maybe you can find a snappier name, but a proxy token is where the original asset X is locked on chain A - then an equivalent number of ‘X on A’ tokens are redeemed on chain B by providing proof that they’ve been locked. Anybody who has any number of `X on A` tokens on chain B can burn them, then provide proof of ‘Alice burned N “X on A” tokens on chain B, and I am Alice’ to chain A to redeem N tokens of type X. You can specify some constraints to describe the system, such that for any number N of X tokens only N (or fewer) exist in a usable form at any place at any given point in time, and obviously “N of X from A on B” and “N of X from A on C” are different types of proxy tokens, but you could transfer “M of X from A on B” tokens to chain C, then prove you burned those on chain C to redeem M of X on chain A etc. as there are only ever M token and M proxy tokens at any point in time (where the original M tokens are locked, and the proxy tokens must be burned to transfer from chain to chain, or to redeem on original chain).

To re-iterate the example above:

- On Ropsten I lock 100 ETH to be redeemed on Kovan, lets call them ‘rETH’
- On Kovan I prove the 100 ‘rETH’ have been locked, to redeem 100 ‘rETH-k’ tokens
- On Kovan I burn 100 ‘rETH-k’ tokens to be redeemed on Mainnet
- On Mainnet I prove the 100 ‘rETH-k’ tokens were burned, and redeem 100 ‘rETH-m’ tokens
- On Mainnet I burn my 100 ‘rETH-m’ tokens to be redeemed on Ropsten
- On Ropsten I prove the burn, to redeem 100 ETH.

I think that’s similar to the problem you’re describing, where Ropsten only knows that you burned 100 ‘rETH-m’ tokens on mainnet, which could have only gotten there if you proved burn elsewhere.

But how do you guarantee that I can’t redeem 200 ETH on Ropsten via some fault-tolerance or other attacks?

And what about the case where duplicating the number of tokens will be more than the equivalent value slashed on one chain? Or if causing a fault on one chain allows me to redeem the same tokens in three or more other places.

---

**vbuterin** (2018-09-02):

So what I describe absolutely does not let you put Ropsten tokens onto Kovan. Only the Plasma chain can hold tokens of other chains in this construction.

---

**HarryR** (2018-09-03):

One thing I should probably add is that, even with Lamport’s ‘99% fault tolerant consensus’, it fails to account for real world value of what’s bonded versus what’s at risk, and assumes that it’s impossible for all validators to collude (they’re all running the same software right? and if a vulnerability is discovered which gives a single attacker remote access to all validators, or the ability to sign with their keys, then it potentially allows one entity to trigger a one-off event where all validators collude against their will).

Anyway, lets take an attack scenario where the rules are adhered to:

- Designated validator Eve, she performs an asset swap each round, going from asset A to asset B and visa versa ad infinitum, losing nothing more than the slippage between two rounds and the fees, times however many rounds it takes to succeed.
- After being picked with probability of 1/40, she publishes two blocks X_1 and X_2 to ETH and ETC, in a way where she ends up with both the original capital and that of the counterparty.
- To ‘win’, Eve needs to DoS the chain where she submitted the fake/incorrect X_i to for a duration of D in a way which time still progresses on that chain.
- As soon as a challenge is submitted on that chain, she needs to prevent that transaction from being included in the next block, Eve does this by submitting many high-gas use transactions from many different accounts - both filling up the blocks and being higher priority/reward for the miners.
- She needs to prevent any challenge transactions from being mined for duration of D, this will likely prevent any other transactions from being mined during that period too.
- She now starts playing the gas-price game with challengers.
- Because each validator is using a single account, each of their transactions are processed in-sequence, which means they can’t play the gas-price game with her as their first transaction will be stuck in the backlog until after D as passed.

So, the problems there are:

1. the base cost of D is known, at the moment that’s 720 ETH per hour (and 480 soon…)
2. each validator’s first challenge transaction gets stuck because of the nonce, unless they have logic to overwrite that transaction with a higher gas price
3. if Eve succeeds, and the validators play the increasing-gas-price-game with her, after T+D they will be penalised with rejected transactions.

So the cost of the attack would be ({Block Reward \over Block Rate} \times Duration) \times GasGameIncrease, where GasGameIncrease is calculated similarly to continuous interest over {Duration \over BlockRate} periods, e.g. if the validators don’t have logic to increase their gas price and re-submit then it would be 1, and if it’s a deterministic algorithm (say, calculate average cost of having it included within 20 blocks) then you can simulate it to find the rate. This gives you a quantitive value for how much you need to swap at each round where the cost of the attack versus the reward of winning makes financial sense.

Secondly, just as an aside, the challenge window of T+D means that you can’t do anything that relies on data which could be challenged until the window has passed, so if you want to perform a sequence of operations where you must wait for the challenge, you need a D interval between them which slows your rate to 1 \over D sequential operations per second unless all validators sign every block - where it becomes 1 \over {D \over k} where k is the average number of validators which sign each block.

In the best case scenarios where everybody is honest this is cheaper, but introduces a long finality window for sequential operations, and in the worst case scenarios where not everybody is honest the finality window decreases.

Furthermore, this reduces the cost of an attack to that of attacking the cheapest parent chain for a duration D, and during D all other plasma chains which share the same root which is being attacked will also be under attack - so, essentially, for multiple Plasma chains, the cost of attacking all of them at the same time is that of attacking the cheapest common parent chain for D. That doesn’t sound like a very good security guarantee TBH - get one, get them all etc.

---

**vbuterin** (2018-09-03):

> assumes that it’s impossible for all validators to collude (they’re all running the same software right?)

Oh I definitely hope there are multiple implementations and people are running different setups. So perhaps the assumption is achievable for larger plasma chains, but harder to bootstrap for smaller chains.

Agree that successfully DoSing any chain can cause atomicity to break.

> Furthermore, this reduces the cost of an attack to that of attacking the cheapest parent chain for a duration D, and during D all other plasma chains which share the same root which is being attacked will also be under attack - so, essentially, for multiple Plasma chains, the cost of attacking all of them at the same time is that of attacking the cheapest common parent chain for D. That doesn’t sound like a very good security guarantee TBH - get one, get them all etc.

I’m not sure this is true. If one root chain gets successfully attacked, then the attacker can steal assets based on that root chain, but security doesn’t break with respect to assets based on any other root chain.

---

**kfichter** (2018-09-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> with bonded validators.

Just to confirm - would you slash validators who sign off on the inclusion transaction if a block isn’t included by `T + k * D`?

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> If one root chain gets successfully attacked, then the attacker can steal assets based on that root chain, but security doesn’t break with respect to assets based on any other root chain.

Yeah, I think the worst you’d be able to do is steal funds reliant on the atomic swap or steal any assets that are stored on the attacked root chain (just like in any Plasma implementaton, I guess).

---

**vbuterin** (2018-09-10):

> Just to confirm - would you slash validators who sign off on the inclusion transaction if a block isn’t included by T + k * D ?

Penalize some, definitely not slash fully.

---

**adamskrodzki** (2018-09-12):

> @vbuterin
> A malicious operator colluding with B can attack by creating block X, then publishing the root into the ETH chain but  not  into the ETC chain

I believe this problem can be solved by proper infrastructure on both chains

Both parent chains (ETH, ETC) need to know each other block hashes. It is doable. You can build Smart contract on each chain where You submit hashes of an other chain. To submit hash of ETC in ETH smartcontract You need to proof that this ETC hash contains (in smart contract) some former hash from ETH (via merkle proof)

Once You have on every chain smart contract that knows hashes of both chains You can build two step process of

submiting the plasma block

1. Only operator can submit a plasma hash “Candidate”
2. To change “Candidate” to “Confirmed” on let say ETH, Anyone (not only operator) need to provide Merkle proof of inclusion of “Candidate” in ETC chain.
3. Once hash is “Confirmed” it can be used in exit procedures.

Sounds to me like a lot of gas need to be used to submit such hashes, so I’m not sure if it is practical, but i believe it’s feseable

---

**vbuterin** (2018-09-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/adamskrodzki/48/1910_2.png) adamskrodzki:

> Both parent chains (ETH, ETC) need to know each other block hashes.

Yes, with this it becomes trivial. My construction was meant to work in cases where the two chains are not capable of learning each other’s hashes.

---

**adamskrodzki** (2018-09-28):

But why to put such constrain (that  two chains are not capable of learning each other’s hashes) if Ethereum like chain is already capable of learning other ethereum like chain hashes. Isn’t it better to build such infrastructure so it will be cheaper to do.

I believe that would open set of powerful tools for Ethereum based plasma chains and on-chain access to past state of blockchain.

