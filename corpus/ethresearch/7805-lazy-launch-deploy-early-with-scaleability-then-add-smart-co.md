---
source: ethresearch
topic_id: 7805
title: "Lazy launch: Deploy early with scaleability then add smart contract interoperability later"
author: barryWhiteHat
date: "2020-08-05"
category: Layer 2
tags: []
url: https://ethresear.ch/t/lazy-launch-deploy-early-with-scaleability-then-add-smart-contract-interoperability-later/7805
views: 2551
likes: 16
posts_count: 9
---

# Lazy launch: Deploy early with scaleability then add smart contract interoperability later

## intro

The great scaling bake off made us realize that different use cases need different scaling approaches. For example the most popular use case for scaling was transfers or exchanges. This meant developers optimized for various things like making transfers cheap. They did not think about making it cheap to give tokens to 1000’s of users.

This lead us to realized that for different use cases a different scaling solutions are preferred.

For example applications that do not interact with external contracts can use the lazy paradigm. Where basically users publish their transactions on chain but the execution is carried out by the users instead of the smart contract. For more than a brief intro see [here](https://arxiv.org/abs/1905.09274).

## What is lazy approach

Currently a user creates a transaction, sends it to a smart contract which executes that transaction. The user can then query the smart contract for the current state of the system.

[![user_compare_current](https://ethresear.ch/uploads/default/original/2X/8/835ed5d70a3c0ad03efab9510a4e88ed05a64810.jpeg)user_compare_current1058×595 27.7 KB](https://ethresear.ch/uploads/default/835ed5d70a3c0ad03efab9510a4e88ed05a64810)

This technique is limited at 15 transactions per second. We can get an improvement of nearly 700 transactions per second (for snarks its 100 TPS)if we instead of executing the transactions in the smart contract we ask the users to execute them.

[![user_compare_lazy](https://ethresear.ch/uploads/default/original/2X/a/a715cb7bca6b860e1caef8d73de60ce6025492a3.jpeg)user_compare_lazy1058×595 27.5 KB](https://ethresear.ch/uploads/default/a715cb7bca6b860e1caef8d73de60ce6025492a3)

So a list of transactions is published on chain and then executed by each user independently. They do this to reconstruct the state. Because the transactions are ordered by the smart contract each user will get the same result.

## Limitations

1. We can cannot withdraw tokens from the lazy world to regular etheruem.
2. Users have to execute a bunch of transactions.
3. You can have limited ability to inter op

## Launch strategy

A lot of projects have a launch strategy where they first launch a centralized solution and then fully decentralize it over time. This makes sense and allows teams to test and experiment.

We propose to add the lazy launch strategy

1. A project launches the lazy version where the users need to execute every transaction themselves. There is limited inter op to other lazy applications.
2. They transition to optimistic or zk rollup to provide scalability and interoperability.

## Example Projects

1. ZKP based reputation system: Here the cost of execution on chain is very expensive ~ 7 USD per operation. Seems like a lazy soft launch can allow for experimentation in the short term while inter op can be added later with scalability.
2. Games: A lot of games would happily trade off interoperability in the short term while they build a community of users. Then unlocking this later once scaling solution has been built.
3. Decentralized Social Media: Because the value of social media is inherently social it does not need to be validated on chain it can just be committed to on chain so other users can reconstruct the state. This example is especially compelling with a reputation system included.
4. Exchange: Users could deposit their erc20s but then they have to wait to withdraw them until the scaling solution is done. Also the developers could steal the funds by providing a broken scaling solution that they could hack.

## Conclusion

Lazy approach works well for things who’s value is “off chain first”. For example if I have 10 reputation in a system i can use that off chain to get into a special party or join a message board. 1 eth is only valuable when it is fungible. Would 1 eth be as valuable if it was locked inside some scaling solution where it was unclear if / when the devs would allow you to withdraw it.

We wont be able to inter op with other ethereum smart contracts. Other contracts will be able to give reputation to others.

In the mean time having an off chain first reputation systems and games makes a lot of sense while we build. It will allow us to bootstrap and learn how people use these systems while we work to scale them.

## Replies

**kobigurk** (2020-08-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/barrywhitehat/48/4436_2.png) barryWhiteHat:

> So a list of transactions is published on chain and then executed by each user independently. They do this to reconstruct the state. Because the transactions are ordered by the smart contract each user will get the same result.

I agree that this is a great method that could be adapted to some cases. It does introduce a new risk that exists only to a lesser extent now - versions of the client-side tx processor has to be matched or users will reach different states without knowing they diverged. When executing on-chain, the miners/validators provide extra protection this will not happen.

---

**barryWhiteHat** (2020-08-07):

If all of the state transition logic is defined in solidity this should not be a problem as solidity has been hardened to be deterministic.

---

**kobigurk** (2020-08-07):

Yep, that’s already a good property. But corruption or bugs are not easily caught.

---

**barryWhiteHat** (2020-08-07):

Let me just re state to be sure we are on the same page.

So the concern is that users independently executing the state may end up at a different* result and not know it. Your major concern is that they would not be able to tell that they both have different views of the world.

* This assumes some non determinism between the EVM implementations they are using.

---

**kobigurk** (2020-08-07):

Yep. I don’t think it’s a huge concern if it’s being tested properly and there are some additional consistency checks in the client, but the difference is that you don’t have the “protection of the miners” any more.

---

**lsankar4033** (2020-08-10):

I think LazyLedger as a design pattern for smart contracts is worth exploring, but I’m skeptical that projects would be willing to use it as a halfway point to L2 as there’s still perceived execution risk around L2 happening.

---

**lsankar4033** (2020-08-10):

If application developers are careful to make the client scripts mostly use `view` helper functions in the contract to compute the transitions, the room for deviation here becomes really small.

---

**weijiekoh** (2020-08-18):

The Lazy Launch pattern applied to Semaphore might look like this:

1. There is a LazySemaphore contract owned by a coordinator. It stores an identity Merkle root and only the coordinator may update it. The coordinator can update the root to any value they wish. They do so at regular time intervals (e.g. once per day).
2. There is a public database of identity commitments (the leaves of the tree). The coordinator controls this database. Ideally, this data would be available even if the coordinator disappears.
3. Anyone can download the leaves and verify the Merkle root.
4. At regular time intervals, the coordinator updates the on-chain root. This is a transaction to add, change, or remove one or more leaves from the tree. If a user wishes to add a leaf to the tree, they have to go through the coordinator. It is the coordinator’s responsibility to keep the off-chain database of leaves in sync.
5. Anyone can generate a Semaphore proof that they have the secret key associated with their leaf. The coordinator can verify the proof off-chain or off-chain.
6. LazySemaphore can be even lazier - it does not need to store any external nullifiers on-chain if it does not have to. For instance, some applications would do fine with a deterministic external nullifier. Of course, whether the external nullifier is on-chain or not also depends on whether the application needs to prevent double-signalling on-chain.
7. Trust assumptions are higher in this model. The coordinator can censor leaf insertions if the contract stores all historical roots in an immutable fashion. Nevertheless, the coordinator cannot prevent registered users from proving their membership in the tree, as long as all leaf data is available.

