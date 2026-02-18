---
source: magicians
topic_id: 959
title: "\"Nodes to start syncing at a given block hash\" - Is this idea worthy of an EIP?"
author: tjayrush
date: "2018-08-05"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/nodes-to-start-syncing-at-a-given-block-hash-is-this-idea-worthy-of-an-eip/959
views: 1295
likes: 3
posts_count: 9
---

# "Nodes to start syncing at a given block hash" - Is this idea worthy of an EIP?

I am trying to think of ways to encourage more people to run more nodes. I think this will happen if one of two are true: (1) it gets easier to run a node, (2) nodes produce useful data. The two issues are related.

One of the reasons why the node is hard to run on a local machine is the size of the data if one wishes to have access to useful data. For my use case, useful data means enough data to fully audit and account for an Ethereum addresses (or collections of addresses). I can’t do that without `--tracing` enabled, which means 100s of GB of data.

Having to store 100s of GB of tracing data is required even if the account I wish to audit didn’t first appear on the chain until recently. For example, if I only want to audit a smart contract that was deployed at block 6,000,000, I still have to store the entire trace history of all accounts prior to block 6,000,000.

Would it be possible for the nodes to start syncing at a given block hash? Say I wanted to start syncing at block 6,000,000, and I know through other means that block 6,000,000 was hash 0x123…  I know it’s not possible now, but is it conceptually possible to do this? After starting at block 0x123…, I would then be willing to participate fully in the network. Later, if I’ve extracted the data I need, I could restart the node at a later block. In other words, the node could fully verify the blocks (after the first one I specify) and then, after I’m done extracting what I need, I can throw away the block’s data.

This would allow me to account for my addresses (in an ongoing manner) but with a minimal imposition on my machine. It seems to me, that if people could more easily extract useful (i.e. accounting) data for their accounts, they might be more likely to run nodes.

Other than the ‘getting the block hash from some other source’, is there a fundamental reason (security-wise) why this wouldn’t work?

## Replies

**jpitts** (2018-08-05):

Setting aside the notion of syncing at a given block hash (which is outside of my expertise and can’t comment on), I think it is a great idea to work on providing new services around nodes in order to incentivize the running of those nodes.

As you have proposed, there is the incentive to run a node for reasons specific to the operator.

On the other hand, there are potentially new types of nodes which would generate revenue and support the operator. These nodes might be for providing ML or analytics to smart contracts, or oracles of various kinds.

---

**fubuloubu** (2018-08-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png) jpitts:

> These nodes might be for providing ML or analytics to smart contracts, or oracles of various kinds.

Great point. I think even in general, this might be useful for trading: being able to query data through different accounts in a very specific and quick way will be very useful on an asset trading platform. Especially when the state gets larger and sharding is a thing etc…

It can essentially be creating a veraion of the Bloomberg terminal, but open and freely accessible, a p2p version where data streams are paid for with micropayments (blah blah blah…)

Someone has to be working on that aspect.

---

**tjayrush** (2018-08-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png) jpitts:

> there are potentially new types of nodes

Just registered `gophanode.io`.  Gopha == Geth Optimized Phor Auditing.

---

**Ethernian** (2018-08-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tjayrush/48/23_2.png) tjayrush:

> Would it be possible for the nodes to start syncing at a given block hash?

I haven’t checked it, but `parity`  in warp mode has two options:

`--no-ancient-blocks`

and

`--warp-barrier=[NUM]`

looks like it is possible to warp back to target block and then stop to download ancient blocks.

Unsure if it is compatible with `--tracing-enabled`, but if not, could be a nice `RFE`

---

**tjayrush** (2018-08-06):

When I start my node with --tracing on I get this message:

`Warning: Warp Sync is disabled because tracing is turned on.`

What’s an RFE?

---

**Ethernian** (2018-08-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tjayrush/48/23_2.png) tjayrush:

> Warning: Warp Sync is disabled because tracing is turned on.

![:frowning:](https://ethereum-magicians.org/images/emoji/twitter/frowning.png?v=12)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tjayrush/48/23_2.png) tjayrush:

> What’s an RFE?

RFE = request for enhancement.

I mean: open issue in parity’s github.

BTW: why do you need traces, once more? Could you just catch events instead?

---

**tjayrush** (2018-08-07):

We’re doing deep auditing which means every transaction including those ending in error (that’s why we can’t only listen to events) plus deep traces all the down to the bottom of the call chain (which is why we need traces).

The reason I was asking about an EIP vs. an issue on Parity is because I think the RPCs between the various clients should be kept in sync so tools such as mine can move from one client to another with minimal effort. It seems the RPC should be consistent across clients. And, remember, the original goal was more people running more nodes, so both Geth and Parity would be made easier to run if people could start at specific blocks and still get a full ‘audit-ready’ history of transactions.

---

**jpitts** (2018-08-07):

I updated the title of this topic so that readers can more easily know what it concerns.

Let me know if I didn’t get it right!

