---
source: ethresearch
topic_id: 1548
title: "Everybody gets a blockchain: Part 1 Alice and Bob's chains"
author: yhirai
date: "2018-03-29"
category: Sharding
tags: []
url: https://ethresear.ch/t/everybody-gets-a-blockchain-part-1-alice-and-bobs-chains/1548
views: 1873
likes: 10
posts_count: 11
---

# Everybody gets a blockchain: Part 1 Alice and Bob's chains

I started thinking about a sharding scheme where everybody gets their chain. The phrase “everybody gets their chain” came first to my mind, and I’m trying to stretch it out.

Alice’s (PoA ~~proof-of-authority~~ proof-of-Alice) chain represents Alice’s subjective view. Bob’s (PoB–proof-of-Bob) chain represents Bob’s subjective view. As usual, the agents are identified with cryptographic signatures.

Before jumping to the general case, let me think about a symmetric two-party case.

All chains use the same address space (maybe the same as Ethereum’s). Alice’s chain has a genesis block that says the chain follows proof-of-Alice. Alice’s chain contains only blocks with Alice’s signature. Each block defines a post-world-state that associates each address with a balance (unit: Alith).

Bob maintains a chain too.  Bob’s blocks define post-world-states that associate each address with a balance (unit: Roberth).

Initially, Bob doesn’t trust Alice’s blocks because Alice can create a parallel history at her will.  And worse, Bob has no way to punish Alice for equivocating.  Alice doesn’t trust Bob’s blocks either.

They want to interact somehow, and create a merged block:

- on Alice’s chain, moves 100 Alith from Alice’s account into a lock that Bob can leak every time he creates a block on his chain.
- on Bob’s chain, moves 100 Roberth from Bob’s account to a lock that Alice can leak a bit every time she creates a block on her chain

For the payout, only “blockheaders” are checked.  Of course, one cannot go too quickly than the other.  Alice can spend only a bit more Roberths as Bob spends Aliths (and the other way around).

Moreover, if ever Bob sees forking blocks with Alice’s PoA, Bob can destroy Alice’s deposit on Bob’s chain. (Of course Alice can do the other way around if she catches Bob forking.)

What if Bob doesn’t produce any blocks?  Then Alice can never spend Roberth (though, **maybe she can still spend “Alice’s Roberth”**). Perhaps, Bob has lots of Roberth, and he wants to keep the chain going so that the value of Roberth is kept somehow.

What if Alice doesn’t accept Bob’s transactions?  Maybe this should be punishable with Alice’s deposit in Bob’s chain.  At least Alice can publish her transaction, and tell the world that Bob is censoring.

Next question: Bob wants to pay Alith to Charlie, but Chalie doesn’t trust Alice’s chain.  Chalie only trusts Bob.  What should happen? (**Maybe Bob can still spend “Bob’s Alith”.**)

## Replies

**kladkogex** (2018-03-30):

What exactly do you mean by “leaking bits” ?![:smiling_imp:](https://ethresear.ch/images/emoji/facebook_messenger/smiling_imp.png?v=9)

---

**yhirai** (2018-03-30):

Let’s say 0.1% of the locked amount each time.

---

**yhirai** (2018-03-30):

Somehow I think this is missing; “when any chain accepts Alice’s transaction, the chain requires the proof that Alice’s chain contains the transaction.”  Then her transactions are sorted sequentially on her chain. Her chain’s sequential order is secured by Alice’s deposits on other chains.  When Alice double-spends on any chain, she risks loseing her deposits on all chains.

---

**RockHoward** (2018-03-30):

This smells a lot like Holochain. I worry that security by exception handling is problematic as bad things happen to good people on occasion and the punishment of banishment and/or loss of everything is rather severe. Still there is definitely the potential to use something like this approach to scale up pretty insanely.

---

**clesaege** (2018-04-02):

Your proposal looks a bit like circles UBI https://github.com/CirclesUBI/docs/blob/master/Circles.md (except everyone gets to have its own blockchain), I suggest you take a look for inspiration.

---

**yhirai** (2018-04-03):

I saw the Holochain whitepaper, and it soulds similar when it says “agent-centric”.  For `git`, double-spending is not an issue.

---

**yhirai** (2018-04-03):

Thanks for the inspirational link.  I wondered if they have really solved Sybil problems.  And then I start wondering what I would do.

Perhaps there must be a way to tax others, but not based on violence.  Something like block rewards but more local, and generalized.

---

**clesaege** (2018-04-04):

The sybil problem seems quite solved to me.

If you add some fake accounts, they will be able to exchanges their faketh again youreth. So you don’t have incentives to do so. You have however incentives to add real ones in order to increase the liquidity of your tokens.

There may be others problems, we’d need some cryptoeconomic experiments to see if this works in practice.

---

**yhirai** (2018-04-04):

Sounds like it’s my turn to flesh out.

---

**yhirai** (2018-04-05):

The security of Bob’s chain is at most Bob’s assets on the other chains.  A briber can talk Bob into forking, and compensate for his loss on the other chains.

So the assets on Bob’s chain will be priced accordingly.  This generates arbitrage opportunity for Bob, who knows more about his fork’s future behavior.  Bob knows more about Roberths future value than anybody else.  Isn’t it securer if Bob owns all Roberths and Alice owns all Aliths?  Why do Alice and Bob exchange their tokens as described?

