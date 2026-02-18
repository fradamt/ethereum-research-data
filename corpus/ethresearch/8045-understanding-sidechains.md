---
source: ethresearch
topic_id: 8045
title: Understanding sidechains
author: barryWhiteHat
date: "2020-09-29"
category: Layer 2
tags: [sidechain]
url: https://ethresear.ch/t/understanding-sidechains/8045
views: 12367
likes: 33
posts_count: 20
---

# Understanding sidechains

NOTE: The views expressed here are my own and do not necessarily represent or reflect the views of others or my employer.

Thanks Albert Ni for review and discussion.

## Intro

Layer 2’s importance to Ethereum is growing by the week, and everyone knows it.

However, “layer 2” is an imprecise label. Right now, when people say “layer 2”, they tend to mean “not on Ethereum layer 1”. But the way something interacts with Ethereum layer 1 matters a lot. Different solutions that are all considered “layer 2” can have wildly different properties. Arguably, layer 2 should only refer to certain things with certain properties (e.g. we probably all agree that something that lives on AWS is not layer 2, but there are projects that arguably have similar security guarantees which are considered layer 2). But maybe that’s a topic for another day.

For this post I want to dig into the properties of sidechains.

Sidechain basically means a system where a set of validators checkpoint the latest state of the chain to a smart contract. These checkpoints are then used by a bridge contract to allow users to deposit and withdraw. There is usually a leader election process among the set of validators to determine who can create blocks. Examples of leader election mechanisms include proof-of-authority (POA) consensus, and Proof of Stake.

Sidechains have played an important role in the the ethereum ecosystem. They’ve been a stopgap solution for scalability and usability while the research community was still working on better solutions. Products like xDai at hackathons have highlighted the need for better UX which has trickled into the rest of the space.

However, sidechains **do not have the security properties the broader Ethereum community expects**. That doesn’t mean they should never be used. If people using sidechains are fully aware of the lack of certain properties, and still want to use them, that’s their prerogative. It may be worth the tradeoffs. It gets dangerous when people are not aware. The hope of this post is to provide information. If everyone was already aware of these properties, then another post about it can’t hurt. But if this helps people realize mistaken assumptions, that’s a good thing.

What are the security properties sidechains lack? Almost all sidechains do **not** provide:

- Censorship resistance
- Finality
- Guarantees about owning funds

If you want more of these properties, seeking alternatives to sidechain-based solutions is one path forward. It is also possible to improve on these dimensions while still using the core sidechain architecture.

My hope is that an open discussion of these properties will benefit everyone.

## Censorship resistance

It should not be controversial to say that sidechains have weaker censorship resistance properties than (well designed) blockchains. Otherwise, there would be no need for blockchains. However, let’s break this down a bit further.

If N validators are involved in a sidechain, and a transaction can be censored as long as M validators agree to do so, then N-M is the number of validators that need to collude in order to censor a block. This leads to a tricky balance where making it harder to censor transactions makes it easier to censor blocks. Given that both transaction censorship and block censorship are undesirable, this makes it fundamentally difficult for sidechains to have strong censorship resistance properties.

This concern extends to when proof-of-stake is used. It potentially gets worse as the numbers involved are weighted by stake, which means the number of distinct entities required to reach certain thresholds is likely even lower (at best, stake is perfectly uniformly distributed, in which case it’s just like the non-proof-of-stake case).

## Data Availability Guarantees

We know that N-M validators are able to create a block. We also know that all other validators need to have data about the whole state in order to validate the new state. So if N-M validators are malicious, they can

1. Create a new block
2. Refuse to share the data with the honest validators
3. Effectively remove N - (N-M) = M honest validators from consensus. Thus capturing the system.

How likely is this to happen? It obviously depends on many situation specific details, but we can start by considering what the incentives are for a rational validator to share data with all other validators. For traditional proof-of-authority, there is likely to be a reputational cost to not doing so. With proof-of-stake based sidechains, there may be stake at risk. However, it’s not easy to make this work, because there is no way to prove that some data was left unavailable without someone else putting all the data on chain. If this sounds like optimistic rollup, it is, which means sidechains with better security properties essentially reduce to optimistic rollup.

In most sidechains, validators receive some form of payment for being validators. For honest validators, this reward is shared among N validators. For dishonest validators, this same reward is shared between N - (N-M) = M (most importantly M < N here), so the there is incentive for validators to not share updated state with others.

An overall concept to keep in mind is it is very difficult to diagnose data availability attacks. To honest nodes, they are often indistinguishable from sync problems.

## Finality

Imagine a series of state transitions as follows

state_1 => state_2 => state_3

Where each => involves a bunch of transactions being applied as part of updating state. Finality is the idea that once applied, a transaction cannot be undone.

Sidechains checkpoint blocks after they have been agreed upon via the consensus on Ethereum mainnet. This may lead one to think that sidechain finality basically is equivalent to Ethereum finality. Specifically, that in order to revert blocks on a sidechain, you would need to revert blocks on Ethereum. **This is not the case**.

This is because Finality is about reverting transactions, not about replacing an old state with a new one. So N-M validators are able to perform the following transition:

state_1 => state_2 => state_1

(replacing state_3 with state_1, thus reverting the supposedly finalized state_2 without requiring Ethereum mainnet reversion).

## Guarantees around ownership of your funds on a sidechain

Assume there exists a state where state_1 = \{\text{Alice}:1000, \text{Bob}:0\}

So Alice has 1000, and Bob has 0. What happens if Bob is malicious and controls (or can effectively collude with) a super majority of POA validators?

Then, Bob can simply perform the state transition state_1 => state_2 where state_2 = \{\text{Alice}:0 , \text{Bob}:1000\}

Of course, this is tantamount to stealing all the funds from Alice and giving them to Bob.

Thus, a sidechain’s defense reduces to saying N-M validators could never be convinced to process such an illegal state transition.

This is well known (or so I believe), but I think it’s useful to remind everyone how this works. Your confidence in a sidechain reduces to your confidence that a supermajority of a sidechain would never do something like this. Most analysis of a sidechain’s security should focus on this.

Now, there may be groups of people (validators) that you would trust in this way. Just like many of us trust various centralized service providers for many things. Sometimes that’s worth the trade offs. It’s just important to be clear that that is the trade off being made.

## Issues with governance as defense

An argument is sometimes made that “we can just use governance to solve everything mentioned so far”. This is flawed in that it basically says the whole system degrades to governance. One reason this argument especially concerns me is that it means the other attributes of the sidechain are theater (in which case, why have those attributes at all?). For instance, if governance is the final fallback to protect against the prior issues, then that means proof-of-stake, proof-of-authority, etc., don’t actually matter. The governance of the system is the real proof-of-authority. And, of course, the governance of the system can then still run all the aforementioned attacks.

## Where might the properties of sidechains be especially useful?

Aside from the auxiliary properties of sidechains, such as faster block times leading to better UX (though databases give this too ;)), there are some situations where the specific properties of sidechains are arguably especially well suited to the desired properties of the system. For example:

1. If you specifically want N-M validators to be able to perform arbitrary state transitions. Enterprise applications who want to have a master control switch are an example.
2. Where M = 0 and you want N validators to be able to perform arbitrary state transitions. For example, in a 4 party game. Though one issue here is that 1 validator can unilaterally halt the chain.

## Final thoughts

It used to be the case that sidechains were the only viable solution for certain use cases that wanted to retain a level of Ethereum compatibility and interoperability. Now, as other layer 2 scaling solutions mature, it is a good time to consider how sidechains can be made more compatible with those solutions.

Some additional features / properties that would be great for sidechains to incorporate:

1. Implement mass migrations without a fee to ensure users can exit without being “stuck” due to costs.
2. Replace the leader election mechanism with something with stronger anti-censorship properties (proof-of-stake seems to be the wrong direction to go in here – see Against proof of stake for [zk/op]rollup leader election)
3. Require coordinators to place the diff between two states on chain.
4. Add fraud proofs to prevent illegal state transitions.

As optimistic rollup tech and the optimistic VM (OVM) mature, the tradeoff space for projects will change. Thus, now seems like a good time to refresh on sidechain properties and their associated tradeoffs.

## Replies

**lsankar4033** (2020-10-02):

Excellent starting point in building awareness around this; I think there’s not enough education around the nuance of the risks users take on with many sidechain/bridge solutions.

> If N validators are involved in a sidechain, and a transaction can be censored as long as M validators agree to do so, then N-M is the number of validators that need to collude in order to censor a block. This leads to a tricky balance where making it harder to censor transactions makes it easier to censor blocks. Given that both transaction censorship and block censorship are undesirable, this makes it fundamentally difficult for sidechains to have strong censorship resistance properties.

I didn’t quite follow this: can you sketch out the relationship b/w tx censorship cost and block censorship cost a bit more?

---

**DZack** (2020-10-05):

I’d hesitate to impose the properties you list on all constructions with the “sidechain” label, since unfortunately, “sidechain” is at least as imprecise a term as “layer 2” [(cc Jorge Stolfi)](https://www.ic.unicamp.br/~stolfi/EXPORT/projects/bitcoin/posts/2015-06-10-my-sofa-is-a-sidechain/main.html). Many (including yours truly) informally refer to optimistic rollup constructions as a type of sidechain, and as you hint at, ORUs don’t have any of the limitations you discuss (if they’re designed accordingly).

I tend to think we should just all get in the habit of always using qualifers w/ “sidechain”, i.e, “trustless/non-custodial sidechain,” “POS sidechain,” “federated sidechain,” etc.

---

**adamstallard** (2020-10-20):

Let’s take two scenarios with different values (v) for the number of validators nodes that are malicious: one where N - M < v < M, and one where N - M < M < v

If a transaction is submitted that the malicious validators want to censor, and they have N - M < v < M nodes, they can only reject the block containing it.

If they have N - M < M < v nodes, they can do better than rejecting the block: they can submit a new block that excludes the transaction, and the remaining N - M validators don’t have enough weight to reject it.

Does this fit what you had in mind, [@barryWhiteHat](/u/barrywhitehat)?

Maybe in the section called “Censorship Resistance” it should read M where it reads N-M (and vice-versa)–or else those terms could be swapped in the section called “Data Availability Guarantees.” If N-M validators are needed to collude to censor a block (as it says in “Censorship Resistance”), then M (not N-M as it says in “Data Availability Guarantees”) validators are needed to create a block–right?

---

**adamstallard** (2020-10-20):

Why do we think that a Proof-of-Work blockchain has a lesser chance of having >33% or >67% colluding attackers than a Proof-of-Authority blockchain?

We’d run into the same problems if Proof-of-Work had those levels of collusion, right?

---

**barryWhiteHat** (2020-10-20):

Its not that one costs a lot and once costs little. Its that you can not make both expensive you can only choose one to cost a lot. Let me give an example.

Lets say we have n = 7 m = 2. This means that there are total of 7 validators and 2 of them need to agree in order to include any transaction in a block. This means two things

1. You have to get 2 validator to agree to include any transaction. EASY
2. if 7 - 2 = 5 of them disappear (or agree to censor all transactions) then no more blocks can be made. HARD

So if we say that getting 2 validators to agree is too easy ie we want to make it harder to get transactions included we can reduce m = 5 and n = 7.

So now you have to get

1. 5 validators to agree in order to include a transaction. Its harder to censor transactions. HARD
2. 7 - 5 = 2 of them need to disappear in order to censor a block. But its also harder to censor blocks. EASY

---

**barryWhiteHat** (2020-10-20):

If proof of work finality of a block is forever being proved. Every time you build upon a block that is proving that block , and all blocks before it are finalized in your view. If you have 33% or 66% malicious they can make an invalid chain or they can perform invalid state transitions. But they need to continue doing this forever. This is a cost that they must pay of maintaining 66% hash power of the rest of the network. If they stop doing this the honest miners will eventually catch up to the malicious tip of the chain and invalidate it.

TLDR it comes down to how you recover from failure modes. With proof of work you can recover from this with side chains its more difficult.

---

**adamstallard** (2020-10-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/barrywhitehat/48/4436_2.png) barryWhiteHat:

> If you have 33% or 66% malicious they can make an invalid chain or they can perform invalid state transitions. But they need to continue doing this forever.

This is a good answer. It’s easy to imagine in PoW how the blockchain can regain decentralized control after a temporary malicious takeover by concentrated power, but there’s no defined way for a PoA chain to regain decentralization once it’s lost. The remaining validator nodes could plausibly claim that there was no collusion. The network would be reduced to a battle of some community members claiming censorship happened and some denying it.

---

**thor314** (2020-10-22):

So I’m not sure if I’m understating the importance of what’s being said, as it sounds like this mostly boils down to, if N-M validators are malicious (or just M), bad things happen (plus some common misunderstandings). I didn’t see any mention of the (un)?trusted bridge to and from sidechains, which I don’t totally understand, but I’ve read that they basically reduce to the same N-M validator problem, with some caveats for waiting for finality on each chain to be considered valid. I claim what’s been said:

- if M of N validators are mally, there’s transaction censorship vulnerability
- If N-M validators are mally:

there’s block censorship vulnerability
- there’s data availability attack vulnerability (which is hard to detect by honest validators)
- Bob, member of the big bad supermajority (N-M?) cartel, can steal Alice’s funds (this would be true POA or POS afaik)

There’s a misunderstanding that sidechain finality <=> ethereum finality, when actually the forwards direction implication is *much* slower/weaker
Some people misbelieve that (presumably off-chain) governance mitigates N-M risk, when really, governance is a reduction of on-chain consensus to an off-chain layer of POA

So from that, I claim  most of the criticism boils down to:

> a sidechain’s defense reduces to saying N-M validators could never be convinced to process such an illegal state transition.

Plus highlighting those misconceptions.

---

**xiaohanzhu** (2020-11-12):

What you described is the level of security of blockchain in general.  For this argument ETH is not secure at all as the sum of all assets on ETH is already more than ETH’s market cap.  Not to mention the 50% attacks cost for ETH (ETH 2.0 will have exactly the problems you described as well)

---

**abramsymons** (2021-02-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/barrywhitehat/48/4436_2.png) barryWhiteHat:

> This is a cost that they must pay of maintaining 66% hash power of the rest of the network. If they stop doing this the honest miners will eventually catch up to the malicious tip of the chain and invalidate it.

I do not think this is true. I thought that honest miners will leave their viewpoint of truth and continue mining on top of what malicious miners mined when the malicious chain get longer. Am I wrong?

---

**kladkogex** (2021-02-03):

Any Proof of Stake blockchain has centralization issues.

And no one to my knowledge satisfactorily solved them. In fact, many people simply ignore trivial questions.

People keep on bringing up irrelevant numbers, like how many software agents a PoS blockchain runs.  It does not matter if it runs a zillion of them, if this zillion is executed by a single party.

ETH2 currently can be stopped from finalizing by action of just 4 parties.

This means that decentralization of ETH2 is roughly currently equivalent to a chain of 12 nodes! Twelve!

Therefore, idolizing security of the main net makes little sense.

In fact, a world with many blockchains is much more secure because at least stopping one does not affect the others!

---

**blazejkrzak** (2021-02-18):

One thing worth to mention that at current gas limits you run (n) of sidechains and whole blocks on eth1 are filled to the roof.

I cant exact say its 10 or 15 of them, but if we stick to this approach you will be having rollups on top of rollups.

Also for example OVM has problem of sequelizer that is very centralized. I doubt that any really decentralized solution will come up near soon.

---

**igorbarinov** (2021-07-24):

More than 300 days from the post

No censorship, no attack, no collusion in the real life on sidechain. All the risks are still in theorycraft plane.

[@barryWhiteHat](/u/barrywhitehat) anything new to add to the post? new risks we should evaluate?

---

**Shymaa-Arafat** (2021-07-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/igorbarinov/48/4892_2.png) igorbarinov:

> new risks we should evaluate?

This is not about side chains, but it is a risk about (I think) about the ratio of myopic or malicious and how it’s calculated through the way to the final step in Vitalik Buterin recent post about reorgs



    ![](https://ethresear.ch/user_avatar/ethresear.ch/shymaa-arafat/48/6377_2.png)

      [Is this really a Binomial distribution?-I believe the formula is not accurate](https://ethresear.ch/t/is-this-really-a-binomial-distribution-i-believe-the-formula-is-not-accurate/10134) [Sharded Execution](/c/sharded-execution/35)




> Regarding the article
>
> I have some doubts about the formula in here
>  [Screenshot_2021-07-20-22-20-19-75]
> -First of all, the formula presented is missing a parameter say “M” to represent the number of groups ( committees we have), where the probability P of myopic represents having say “X” malicious such that
> P=X/NM
> So there must be something wrong in this formula
> -True at the end the shuffling algorithm chooses one at random, this could mean to divide the resulting probability by 1/M, but …

Ps.

Take care that I use M,N differently, in the current actual values M=32, N=6125



      [gist.github.com](https://gist.github.com/gakonst/f7756debc09a75ce6c54eb526be14e52)





####



##### prob.py



```
import math

def choose(n, k): return math.factorial(n) // math.factorial(k) // math.factorial(n-k)
def prob(n, k, p): return math.exp(math.log(p) * k + math.log(1-p) * (n-k) + math.log(choose(n, k)))
def probge(n, k, p): return sum([prob(n, i, p) for i in range(k, n+1)])

committee = 6125
half = committee / 2

for p in [0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51]:
```

   This file has been truncated. [show original](https://gist.github.com/gakonst/f7756debc09a75ce6c54eb526be14e52)

---

**barryWhiteHat** (2021-07-27):

The fact that centralized exchange x has not been hacked / exit scammed does not mean that all centralized exchanges have the same security properties as ethereum.

There have been more people writing about what side chains don’t have the security properties we are used to.



      [Dankrad Feist – 20 May 21](https://dankradfeist.de/ethereum/2021/05/20/what-everyone-gets-wrong-about-51percent-attacks.html)





###



What everyone gets wrong about 51% attacks










https://vitalik.ca/general/2021/05/23/scaling.html

---

**kladkogex** (2021-07-31):

Well, people that run other chains are simply in no way inferior to people that will run ETH2 POS.

This entire discussion is to a large degree pointless, since users will ultimately decide what they want to use.  Clearly, if someone thinks there will be one single blockchain for the entire world, it is not going to happen.

---

**barryWhiteHat** (2021-08-02):

I am not an ethereum maximalist. I am just saying that l1 block chins and side chains have very different security properties.

I think the side chain definition is about bridged assets. If assets are bridged from another block chain then the security of these assets is defined by the bridge rather than by the security of the side chain consensus or the security of the l1 they are bridged from.

---

**kladkogex** (2021-08-02):

Hey Barry,

Several months ago ETH foundation decided to go with the model where there is ETH main net and a number of rollups.  Then most people I know at ETH foundation started to strongly promote rollups vs blockchains.

I personally think that rollups vs blockchains  is a way more complex subject for several reasons:

a) first, rollups have a centralization problem which is addressed only for the case of outright fraud but not for the case of manipulation, front running, and MEV extraction. This makes rollups much worse than chains. For instance, at SKALE we solve the problem of MEV totally using threshold encryption.

Our chains wont have any MEV problems. Try to do it with rollups.

b) second optimistic rollups have a big issue of the economic model that needs to provide viable ecosystem for fraud-proof submitters. This economic model has never been published. We do not know how this thing runs, which is ironic having that several optimistic rollups claim to run now in production.

c) third ZKRollups have a computational and engineering problem running complex smart contracts.  People essentially run ZKRollups under the belief that within the next two years a genius will come up with a magic solution to speed up ZK rollups.

A way more reasonable future in my view is ZKRollups becoming a niche for the foreseeable future due to computational complexity problems. From this perspective, I do not share the optimism that ETH foundation has, and frankly do not see where the optimism comes from.

d) Fourth optimistic rollups have a huge problem with long withdrawal times.   A typical user will not want to wait a week.

e) Fifth, rollups still require users to pay. Yes, maybe 10 times less than mainnet. But why, if it can be free on an application-specific chains.

f) Sixth, performance of rollups is still severely limited by having to post transactions on the main net, which is aready congested

e) Seventh, I do not understand the argument why application-specific chains are less secure than the mannet. In my view, the security is comparable if essentially the same community of validators run different networks. Runnin many blockchains can make the total system way more secure by localizing damage.

g) And then finally, ETH foundation should not take a stance to support or reject a particular technology outside of the main net.

It would be much better to stay neutral from the beginning and let people design different things and users try them. Now ETH foundation has evolved from saying that rollups are good and other chains are bad into saying something like this. “Chains are OK for now, optimistic rollups are better, and ultimately everything will run on ZKRollups” .

Well Linux Torvalds has never tried to decide whether Ubuntu is better or worse than RedHat.

---

**Econymous** (2021-08-27):

How can I get started learning how to build a sidechain with assets from mainchain?

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Any Proof of Stake blockchain has centralization issues.
>
>
> And no one to my knowledge satisfactorily solved them. In fact, many people simply ignore trivial questions

I’m glad you saw my recent post.

