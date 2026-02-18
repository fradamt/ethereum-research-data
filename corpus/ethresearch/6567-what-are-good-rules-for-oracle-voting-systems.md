---
source: ethresearch
topic_id: 6567
title: What are good rules for Oracle voting systems?
author: Econymous
date: "2019-12-02"
category: Miscellaneous
tags: []
url: https://ethresear.ch/t/what-are-good-rules-for-oracle-voting-systems/6567
views: 2393
likes: 2
posts_count: 5
---

# What are good rules for Oracle voting systems?

So for the actual voting, there will not be a smart contract. So there is no transaction per vote.

The oracle platform I want to make initially will be a centralized application. That’s okay. That’s just to prove the concept of the decentralized/distributed supply.

The only transactions that happen (I think) are when an account needs to be slashed, and when a truth needs to be told.

My oracle platform works with a voting system. People vote on the “truth” of something in the real world.

But there are different types of truths and I wanted to be sure I covered all my bases and a that I’ve thought of the best ways to accommodate the format of both.

So there are “one time truths”, like “Who won the basketball game on October 31st?” That will be decided one time.

But then there are “ongoing truths”. “What’s the weather at location x,y,z?”

For the first, I can imagine that participants in the voting process will have to vote on what they’ve observed by a certain time. After that, anyone who hasn’t voted  or voted incorrectly against the majority is slashed.

For the second, I imagine a “window of time” to submit answers and potentially a “tolerance gradient” associated with slashing.

I think I could be missing another concept for time. There’s “once” and “ongoing”. Maybe there’s something else. Assuming a voting system is always fair, what else can oracles do? What other rules systems need to be implemented?

## Replies

**miles2045** (2019-12-02):

Collusion-resistance, i.e. voters cannot easily prove to others how they voted. Check out the thread here on MACI.

Best of luck.

---

**mikedeshazer** (2019-12-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/miles2045/48/701_2.png) miles2045:

> Check out the thread here on MACI.

Link (originally missing in your response) : [Minimal anti-collusion infrastructure](https://ethresear.ch/t/minimal-anti-collusion-infrastructure/5413)

And also thanks for sharing! I’m currently working on an oracle project, and have added a [reference](https://github.com/mikedeshazer/OrFeedSmartContracts/blob/a7d297741137fb5c952638ac481304bf55083601/README.md) to MACI as it’s a good option to have.

Further, regarding oracle voting systems, it really does depend on what the needs are of the application consumers and developers.

For example, a board of directors in a company in a DAO might want to appoint themselves as the sole voting party regarding validating and/or reporting a result provided by an oracle.

Meanwhile, for options/other derivative contract settlement, there could actually be regulations in certain jurisdictions that specify who can be the provider of pricing data (See:  Bucket Shops wiki.)

Royalists is Thailand might want a single semi-divine party to be the sole-voting power.

Meanwhile, most Western libertarians would like the oracle’s data for an election to involve MACI or simply a system in which everyone gets an equal vote.

Therefore, flexibility to change the provider or validator process in a predetermined way that participants are aware of from the beginning is essential. As “good” is relative, it will always depend on the people using the system.

---

**Econymous** (2019-12-03):

Thanks. I will build what I know.

I’ll share the source once I’m done.

I just have this very interesting token supply(smart contract design) that has an interesting whale immunity to it. And I think it would be perfect for solving a technical trust issues somewhere in blockchain.

---

**Econymous** (2020-03-21):

Here’s what I’ve got.

https://pastebin.com/Ue8fvh1p

Now I’m looking for strong usecases for the oracle.

Sports events are dead it seems. But I’m sure something else is comprable.

I was thinking eSports, but that’s simply not as sexy.

