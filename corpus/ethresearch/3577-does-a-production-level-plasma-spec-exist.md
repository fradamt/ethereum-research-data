---
source: ethresearch
topic_id: 3577
title: Does a production-level Plasma spec exist?
author: kladkogex
date: "2018-09-27"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/does-a-production-level-plasma-spec-exist/3577
views: 4302
likes: 12
posts_count: 21
---

# Does a production-level Plasma spec exist?

There is quite a bit of  confusion about Plasma recently.  There are multiple Plasma flavors considered and researched. From reading this message board my humble conclusion is that there is not yet a production-level spec for Plasma.  There are research-level specs or proof-of-concept specs but not a detailed production-level spec. This is totally fine imho since people are trying different things, approaches, zksnarks etc.

What is really strange though is there are multiple companies claiming that they do production level Plasma. I am really confused what are these guys developing if there is no spec yet. Investors are investing zillions of dollars in Plasma. What are they investing - into research/prototype specs that still need to be polished, or in a production-level spec that has all security subtleties perfected?))

So let me ask a question on behalf of many people interested in Plasma - is there a production level  Plasma spec, security of which is approved by [@vbuterin](/u/vbuterin) and other people at ETH foundation?

Imho it would be nice if ETH releases a public statement regarding Plasma, something like “we have prototype specs, and expect a production level spec 6 months from now”, or “we have a production level spec, and here is a link to it”.

It cheaper and faster to build an insecure system than to build a secure system. If there is no official guidance on Plasma, it almost certain that insecure systems will be first to market.

## Replies

**MihailoBjelic** (2018-09-27):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> What is really strange though is there are multiple companies claiming that they do production level Plasma. I am really confused what are these guys developing if there is no spec yet. Investors are investing zillions of dollars in Plasma.

Can you name some of those companies/projects?

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> So let me ask a question on behalf of many people interested in Plasma - is there a production level Plasma spec, security of which is approved by @vbuterin and other people at ETH foundation?

To the best of my knowledge, no.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Imho it would be nice if ETH releases a public statement regarding Plasma, something like “we have prototype specs, and expect a production level spec 6 months from now”, or “we have a production level spec, and here is a link to it”

I think the later makes sense (once we are there), but remember that there will never be a single Plasma spec, Plasma is more of a design philosophy/set of guidelines.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> It cheaper and faster to build an insecure system than to build a secure system. If there is no official guidance on Plasma, it almost certain that insecure systems will be first to market.

Yes, and it’s kind of concerning if one of those projects **actually** goes live (although I think chances are slim, they just want to grab naive investors’ money). Then it could make some mess and damage the reputation of Plasma. That’s why I think the Eth community will/should discuss and review such projects (one of the reasons I’ve asked you to name them).

---

**johba** (2018-10-06):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> What is really strange though is there are multiple companies claiming that they do production level Plasma.

All Plasma designs have vulnerabilities or at least specific UX tradeoffs that need to be addressed. Some companies put a PoS model on top and claim a kind of “security by obscurity”. These companies need to be called out.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> is there a production level Plasma spec, security of which is approved by @vbuterin and other people at ETH foundation?

I’d leave Vitalik and EF out of it, as their involvement has allowed for the Plasma-hype in the first place. Rather I suggest to define the requirements that a spec would need to satisfy to be considered ready for “production”.

Ultimately, any Plasma design will have to prove itself in production deployment.

---

**sg** (2018-10-07):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> If there is no official guidance on Plasma, it almost certain that insecure systems will be first to market.

Congratulations for your upcoming fund raising. Your SKALE Network seems like EVM-ecosystem scaling solution. And I personally guess the withdrawal procedure will be done by ParityBridge-like somehow trusted(federated) withdrawal module.

But I’ve seen [this article](https://www.prnewswire.com/news-releases/skale-labs-raises-9-65m-to-launch-the-skale-network-accelerate-dapp-performance-with-new-blockchain-infrastructure-300724289.html) and it says “SKALE will be the first implementation of the Ethereum Virtual Machine (EVM) on a Plasma chain”.

So there is quite a bit of confusion that SKALE is EVM Plasma, but sounds like it has exit mechanism. Do you plan to use expensive EVM inside EVM construction? Or, is it Plasma?

---

**kfichter** (2018-10-17):

Not really production level, but something I’ve been workshopping a little lately: https://www.learnplasma.org/en/resources/#plasma-mvp-specification

Feedback would be very appreciated. Definitely needs more detail on the child chain side of things and client interaction.

---

**kladkogex** (2018-10-17):

[@sg](/u/sg) - thank you for your message and congratulations on the fund raise!  There has been admittedly a bit of confusion in the way we got described in the press. We do not consider ourselves Plasma. In my humble opinion Plasma is a very specific thing which includes a Plasma operator that operates an UTXO chain as well as a set of exit algorithms that are executed if the Plasma operator becomes malicious.

At Skale we are building a network of ETH-compatible side chains that use fast PoS-like consensus. Miners will be able to add servers to our network and stake Skale tokens to make money. Out of this large network of servers we will be able to build side-chains on demand by randomly picking servers, and then rotating them from time to time. A dapp developer will be able to pay in Skale tokens and get a side chain for her application.

Nowadays for some people (including investors) Plasma is more of a generic term everything that speeds up transactions ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9) If they want to keep calling us Plasma, we do not really argue too much …  ))

---

**kladkogex** (2018-10-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png) kfichter:

> Not really production level, but something I’ve been workshopping a little lately:

It looks like OmiseGo is the leader in terms of Plasma implementation on the moment. For me OmiseGo are the good guys, in a sense that they are trying to make things secure.

So in this spec, what happens if I start with a $100 UTXO, and do a 100,000 transactions sending 1 cent to myself (to my other address).

I then randomly pick out of these transactions 1000 spent UTXOs  and try to fraudulently exit all of them.

How does this work in case of OmiseGO? Who is going to be the party challenging the exits and how is this party going to be paid?

---

**kfichter** (2018-10-18):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> How does this work in case of OmiseGO? Who is going to be the party challenging the exits and how is this party going to be paid?

User must put up a bond on each exit, challenger receives that bond for a successful challenge. Slight oversimplification of the solution but that’s the basic idea. Incentives should be aligned such that people will just challenge stuff because it’s worthwhile to do so.

---

**eolszewski** (2018-10-18):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> So in this spec, what happens if I start with a $100 UTXO, and do a 100,000 transactions sending 1 cent to myself (to my other address).

Where’d you get $900 from for the other 90,000 transactions? ![:stuck_out_tongue:](https://ethresear.ch/images/emoji/facebook_messenger/stuck_out_tongue.png?v=14)

With plasma cash, you can create 10,000 tokens from this $100 and then you just submit proofs of inclusion / exclusion when it comes time to exit. Anyone can challenge an exit, but in the case of you sending coins to yourself, there doesn’t seem to be any reason for anyone to challenge given that you’re only touching your own collateral.

---

**kladkogex** (2018-10-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png) kfichter:

> User must put up a bond on each exit, challenger receives that bond for a successful challenge. Slight oversimplification of the solution but that’s the basic idea. Incentives should be aligned such that people will just challenge stuff because it’s worthwhile to do so.

Understood - thank you. I think the next step is to provide a formula for the value of the bond. It should probably be proportional to the amount being exited.

![](https://ethresear.ch/user_avatar/ethresear.ch/eolszewski/48/1902_2.png) eolszewski:

> in the case of you sending coins to yourself, there doesn’t seem to be any reason for anyone to challenge given that you’re only touching your own collateral.

Thats the problem  - you are creating lots of spent UTXOs that you can try fraudulently exit by claiming them unspent - what Kelvin says is that for every exit the person exiting is supposed to post a bond which serves as an incentive for bounty hunters to catch fraudulent exit attempts.

There is another difficult problem, which also needs to be addressed somehow.  Lets say the operator becomes malicious and everyone attempts to exit the system.

Due to performance restrictions of the main chain,  one will probably be able to have no more than one exit per second without significantly affecting the gas prices.

This means 3600 * 24 * 7 = 100,000 exits maximum in a week.

Therefore, each Plasma operator should(?) be limited to having 100,000 coins maximum unless batch exits are implemented.

May be a way to solve this is to require multiple Plasma operators and limit each of them to 100,000 coins. Then there has been

It is a hard problem, I hope it will be solved somehow …

---

**schemar** (2018-10-19):

Is this relevant? (by [@gakonst](/u/gakonst))

In the conclusion it reads:

> A reference implementation which is used in production is provided.

https://twitter.com/gakonst/status/1052495390560403456

https://github.com/loomnetwork/plasma-paper

---

**kladkogex** (2018-10-19):

Does this include an exit bond similar to OmiseGO implementation? I think it does, but does not specify the value of the bond. It should probably be linearly proportional to the amount exited.

In the case where exits from self-transfer transactions are challenged, the challengers need to potentially have a copy of the entire Plasma chain, which may be terabytes of information. This needs to be discussed I think. The Plasma operator needs to provide to the bounty hunters a way to continuously download the entire chain.

In the example where Alice creates a chain of 1M self-transfer transactions and attempts to fraudulently exit some of these transactions, there are no counterparties that will care about storing the proof of Alice spending the transactions.

Therefore, the only party that will be able to challenge Alice will be the Plasma operator itself, or the bounty hunters.  But bounty hunters will need to have an up-to-date copy of the entire chain.

The funny thing is that if, say, there are 10 bounty hunters that have to maintain a copy of the entire chain,  it is almost like having a PoA chain where there is one block producer and 10 slaves.

---

**schemar** (2018-10-19):

Unfortunately the paper does not go into detail on that topic and it’s not discussed as a possible attack. However, I could imagine that this part also solves for the attack you describe:

> Starting an exit for a coin requires providing the transaction that gave the exitor owner- ship of the coin signed by the previous owner in the coin’s history, as well as a direct ancestor of that transaction.

I haven’t had much time to think about it, but could it be forbidden to exit a coin that you sent to yourself in the parent transaction? ![:thinking:](https://ethresear.ch/images/emoji/facebook_messenger/thinking.png?v=12)

---

**gakonst** (2018-10-19):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Does this include an exit bond similar to OmiseGO implementation? I think it does, but does not specify the value of the bond. It should probably be linearly proportional to the amount exited.

Why do you believe bond pricing should depend on the amount being exited?

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> In the case where exits from self-transfer transactions are challenged, the challengers need to potentially have a copy of the entire Plasma chain, which may be terabytes of information. This
>
>
> In the example where Alice creates a chain of 1M self-transfer transactions and attempts to fraudulently exit some of these transactions, there are no counterparties that will care about storing the proof of Alice spending the transactions.

Creating a chain of 1m self transfer transactions in Plasma Cash is just Alice having a certain coin and spending it over 1m blocks to herself. At any given point if she attempts to exit at an earlierpoint than the latest spend, her exit can be challenged with a direct spend of it. No need to store the whole tx history. The challenge is just 1 merkle branch (+signatures obviously) which proves that the coin being exited has been spent.

Plasma Cash is not vulnerable to any of the attacks you describe, exactly because each coin is unique and independent from each other.

---

**kladkogex** (2018-10-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/gakonst/48/1101_2.png) gakonst:

> Creating a chain of 1m self transfer transactions in Plasma Cash is just Alice having a certain coin and spending it over 1m blocks to herself. At any given point if she attempts to exit at an earlierpoint than the latest spend, her exit can be challenged with a direct spend of it. No need to store the whole tx history. The challenge is just 1 merkle branch (+signatures obviously) which proves that the coin being exited has been spent.
>
>
> Plasma Cash is not vulnerable to any of the attacks you describe, exactly because each coin is unique and independent from each other.

Actually we are discussing Plasma MVP and not Plasma Cash ) OmiseGo spec we started to discuss above it Plasma MVP.  The same is as a understand true for Loom Network.

So for Plasma MVP, if I have a long set of transactions sending money to myself, then no-one except myself cares about these transactions.

This means that if I try to fraudulently exit some of the spent UTXOs, I will have no counterparty to challenge this, since I was both the sender and the receiver.

So the only one to challenge me will be “bounty hunters” who just want to make money from my deposit.

Do other people on this thread agree to this point of view?

If I am a bounty hunter, I need to have a copy of the entire chain since fraudulent exits may come from anywhere in the chain.

At 1000 transactions per second, a chain will produce 6 TB a year. This means that a bounty hunter will need to run a Hadoop or Spark cluster to verify exits.  You wont be able to do it on a PC.

Getting the economics right for the bounty hunters will be super important.  If they are only paid when they find fraudulent exits, the question will be to have enough fraudulent exits to support the hunters.

Lets say I want to become a full time bounty hunter and run a Spark cluster to catch bad guys. I will probably want to make $200K a year and also pay for the cloud costs. The question is, how I am I going to make this $200K a year if I am only paid when someone does fraudulent exit attempts and I catch them ? The better job I do, the less fraudulent exits will be attempted, the less money I will make.

May be the Plasma operator needs to do some mockup fraudulent exits to feed the bounty hunters?))

---

**MihailoBjelic** (2018-10-19):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Lets say the operator becomes malicious and everyone attempts to exit the system.
>
>
> Due to performance restrictions of the main chain, one will probably be able to have no more than one exit per second without significantly affecting the gas prices.
>
>
> This means 3600 * 24 * 7 = 100,000 exits maximum in a week.

That’s why mass exits should exist.

I’m not sure how you arrived at this 1txps exit rate?

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> May be a way to solve this is to require multiple Plasma operators and limit each of them to 100,000 coins.

This is trivial to game, they only need to collude.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> At 1000 transactions per second, a chain will produce 6 TB a year. This means that a bounty hunter will need to run a Hadoop or Spark cluster to verify exits. You wont be able to do it on a PC.

This is a valid point (the numbers can vary, though).

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Lets say I want to become a full time bounty hunter and run a Spark cluster to catch bad guys. I will probably want to make $200K a year and also pay for the cloud costs. The question is, how I am I going to make this $200K a year if I am only paid when someone does fraudulent exit attempts and I catch them ? The better job I do, the less fraudulent exits will be attempted, the less money I will make.

And this as well. And on top of everything, users need to trust these entities (no one watches the watchers), which is not in the spirit of Plasma.

---

**kladkogex** (2018-10-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> I’m not sure how you arrived at this 1txps exit rate?
>  kladkogex:

It is a very rough estimate. Eth is able of < 20 TPS in general. You do not want to take more than 10% of the overal transactions, otherwise the gas price will skyrocket.

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> That’s why mass exits should exist.

I totally agree on that. It looks like without mass exits the spec should limit the number of coins (UTXOs) a chain can hold .  But then frankly, if you limit you chain to 100,000 coins it may not be useful at all unless it is used to serve population of in a small town.

---

**fubuloubu** (2018-10-20):

I’m not sure that’s true. It limits the rate at which you can conduct entries and exits, but you can take however long to conduct an exit and have a pretty good guarantee that it will still be there when you’re ready to exit. A mass exit will be annoying and take a very long time, but it doesn’t have a deadline and thus shouldn’t limit the size of the underlying network.

The rate of entry controls the growth of the network, not the amount of coins possible to trade. There is a larger limit on the coins related to the choice of tree depth and data availability solutions, but I would think this is generally much higher than 100k tokens.

---

**eolszewski** (2018-10-21):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> I totally agree on that. It looks like without mass exits the spec should limit the number of coins (UTXOs) a chain can hold . But then frankly, if you limit you chain to 100,000 coins it may not be useful at all unless it is used to serve population of in a small town.

You’re talking about exiting 100,000 coins, but nobody is even discussing how to get all those users onboarded to begin with, in the first place! How did all those users get there? Do you know how long it would take to onboard 100k unique users to the plasma chain with the current constructs that we have at present?

This is why mass transfers should exist where one party enters with a large piece of collateral and then fragments it amongst 100k users. But even in this case, that’s just a credit plasmachain - actually reimbursing the operator for all of this is another story which will likely be supported by FIAT.

---

**kfichter** (2018-10-24):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> At 1000 transactions per second, a chain will produce 6 TB a year. This means that a bounty hunter will need to run a Hadoop or Spark cluster to verify exits. You wont be able to do it on a PC.

MVP supports simple checkpointing where you just throw out everything older than two weeks. Significantly less data than you think. You’d need that much if you wanted to run an archival node.

---

**kladkogex** (2018-11-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png) kfichter:

> MVP supports simple checkpointing where you just throw out everything older than two weeks. Significantly less data than you think. You’d need that much if you wanted to run an archival node.

[@kfichter](/u/kfichter)  - how do you throw away things older than two weeks ? You could have an open UTXO which is in a very old block (e.g. one year old).  What procedure do you use for check pointing?  It is not clear to me how this could be done on an UTXO chain.

And, does check-pointing mean trusting the chain operator in some way?

