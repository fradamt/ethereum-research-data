---
source: ethresearch
topic_id: 1401
title: Cryptoeconomics in Kleros
author: jonchoi
date: "2018-03-15"
category: Economics
tags: []
url: https://ethresear.ch/t/cryptoeconomics-in-kleros/1401
views: 2170
likes: 3
posts_count: 8
---

# Cryptoeconomics in Kleros

Was discussing with Federico, and bringing it to ethresearch per his request ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

Clement,

Great talk at ethcc. Couple of thoughts I’d love to share with you. I work on cryptoeconomics at EF, and found your presentation fascinating (especially the historical framing). Added Schelling and the Federalist Papers to my reading list.

1. "What people would think vs what I think” – While I do think that the coordination problem as an incentive mechanism is quite clever, it may not work in all cases, especially if there are times when a juror thinks “I can see how most people in my juror set would support person A, but if they could hear my argument for person B, they may change their mind,” then the protocol would encourage the juror to agree with the consensus rather than vote her mind.
This would work in most cases but may inadvertently reward “groupthink” in the subtle cases.
2. Cryptoeconomics – I was beginning to think about how this model would scale in each of low value, medium value and high value disputes. In high value disputes, subtlety may require deliberation and the early version of the protocol may not be suitable. In low value disputes (even the $500 web dev case), to pay for 5 jurors say $20 of their time, it would eat up 20% of the value in “legal costs.” This has a few problems. Good actors are used to centralized parties being able to recoup all costs in case of successful dispute resolution. In order to do that, the counter party will have to be penalized, which will require a financial stake to do work (i.e. web dev, which could be an interesting solution). Also, depending on how much kleros tokens are required to be a juror, the “yield” of being a juror may not be enough ($1000 stake for $20 yield per case for example is starting to become unattractive to the “lazy” segment of people)… especially net of the risk of getting “slashed.” In which case, it attracts jurors that are ideologically driven rather than are purely financially driven. This may leave medium value disputes around ICO funding or other high value crypto (and/or all digital) transactions the most compelling initial use case.

Would love to hear what you think about these topics.

Super excited for your team’s progress. Do agree that this is a layer that should be abstracted away from most networks as an outsourced model.

Best,

Jon

## Replies

**clesaege** (2018-03-16):

(copy of the answer by mail)

1. For this case, it should be solved by the appeal mechanism. Jurors won’t know who would be drawn in appeal and the drawn jurors will be able to see an explanation of the votes of previous sessions.
2. Yeah, we could have deliberation for complex cases. But I’d see it more as an adversarial approach of the parties trying to show the best evidence supporting their cases and try to refute opposite party reasoning.
For small value, the Arbitrable contract can require both parties to deposit the fees and reimburse the winning one. This way it could work even if the dispute resolution fees are higher than what is at stake. There will still be disputes due to information asymmetry where both parties would think they would win. But making the dispute resolution process a negative sum game would incentive parties to settle.
Note that it’s not really getting slashed, as except if all jurors vote in a manner incoherent to the final decision, one juror loss is another juror gain. So for jurors it’s a positive sum game (due to arbitration fee) which should encourage participation.

For use case I see is listing disputes (items and shops on decentralized marketplaces, where malicious content is flagged and juror accept or reject the flagging, content submitter and flagged needs to put a deposit which is given to winner (submitters of items would have to pay the deposit upon submission and get it reimbursed automatically if the content is not flagged within some time period). It for me the easiest usecase are disputes are self-contained (no need of additional evidence) and we got some test data from Ink/Listia about real disputes and how their customer service solved them.

If you are interest to think on Kleros, a few problems are:

-How do you prevent jurors from disclosing their votes to influence others? We thought about using commit and reveal with early reveal penalization (proposed by Truthcoin), but this can be bypassed by a self contracting attack which basically consist of making a smart contract with oneselves saying “If I don’t vote this way, the deposit is burnt”.

See https://github.com/kleros/kleros-attacks/blob/master/early-reveal-penalization/DepositForEarlyReveal.sol

-How do you avoid pooling? If sufficient amount of jurors where to pool together, they could copy each other’s votes. The problem would be that they’d do economies of scale (analyzing evidence only once) and therefore get a competitive advantage toward other jurors. The answer could be forking and removing their stake, but the problem is that we may not even be aware of this pooling. I guess it’s a hard problem similar to PoW and PoS.

-How to deal with 51% attacks? Again we can fork, remove the stake of the attacker and contrary to previous problem the attack is visible. The problem is that a successful attacker will still get to decide the result of the disputes in contracts made before. If this right to temper judgement were to be extremely valuable to compare to marketcap of PNK, the attack can be profitable. But unlike Augur finding the potential value at Stake in disputes is way harder. What is the value of cryptokitty? Of the answer of an Oracle? If we are in the honest majority model it’s fine but if we have weaker assumptions?

Note that it’s a problem similar to 51% attacks in proof of stake, we can fork, but the AI and connect objects (like smart locks) relying on the chain would still follow the initial chain.

---

**MicahZoltu** (2018-03-16):

You can also use zero knowledge protocols to prove that you voted a certain way without actually revealing your vote.  There are an infinite number of ways to prove that you voted a certain way with zero knowledge to a human, but a contract can only be designed to handle a finite set of such mechanisms.

As Austin Williams (Augur’s resident theory expert) likes to say, commit/reveal and ZK schemes are only useful if the user with the information *wants* to keep that information a secret.  If a user wants to make their information available to someone in a trustless way you cannot stop them.

---

**vbuterin** (2018-03-16):

> If a user wants to make their information available to someone in a trustless way you cannot stop them.

This isn’t true as a general rule; coercion-resistant voting schemes do exist, though they are dependent on M-of-N trusted server constructions.

---

**clesaege** (2018-03-16):

Yeah so in this case it would be:

If a party wants to let other parties know that either:

- He voted a certain manner.
- He will loose a deposit.

We cannot stop it.

---

**MicahZoltu** (2018-03-16):

Hmm, [@vbuterin](/u/vbuterin) I would like to hear a longer form argument (or link is fine) that it is possible to force (via economic incentives) someone to keep quiet when they have information they want to share.  The premise of my argument here is that if someone has some piece of information, there is no contract you can enter with the person before hand that can be trustlessly enforced (meaning no human making a judgement call) such that they will be financially punished for sharing that information in a way that doesn’t require trusting them.

The naïve solution to this problem is to enter a smart contract with the person who holds the reveal secret in a commit-reveal scheme that asserts, "If you reveal the secret then I can prove it to the smart contract and you will forfeit this bond.  However, the holder of the secret could prove to a third party that they hold the secret and that the secret combined with the encrypted commit are X.  Since the specific implementation of this proof can be decided on after the smart contract is entered into, the smart contract cannot be designed to handle the ZK proof in advance.

---

**clesaege** (2018-03-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> If you reveal the secret then I can prove it to the smart contract and you will forfeit this bond.

Yeah, that’s what we planed to do, this is described in the Truthcoin paper (www.truthcoin.info/papers/truthcoin-whitepaper.pdf, p43). But I found out we could attack it with cut and choose: [Cut and choose against early reveal penalization - Google Docs](https://docs.google.com/document/d/1KVUrjxUkVT01ekQHhDeILr5unJdHP-UFl_dkki-xCmE/edit?usp=sharing)

and later Zack found out we could even do a simpler, but less efficient attack(https://github.com/kleros/kleros-attacks/blob/master/early-reveal-penalization/DepositForEarlyReveal.sol).

I guess ZK proofs would be even stronger attacks as they would guarantee the value of the commitment, not only guarantee that the party has economic incentives not to lie.

---

**vbuterin** (2018-03-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> The premise of my argument here is that if someone has some piece of information, there is no contract you can enter with the person before hand that can be trustlessly enforced (meaning no human making a judgement call) such that they will be financially punished for sharing that information in a way that doesn’t require trusting them.

This I agree with. But in principle it is possible to design cryptographic protocols where someone has no way of proving that some particular piece of information is correct.

