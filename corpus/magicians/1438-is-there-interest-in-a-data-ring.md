---
source: magicians
topic_id: 1438
title: Is There Interest in a Data Ring?
author: tjayrush
date: "2018-09-23"
category: Working Groups > Data Ring
tags: []
url: https://ethereum-magicians.org/t/is-there-interest-in-a-data-ring/1438
views: 1859
likes: 5
posts_count: 16
---

# Is There Interest in a Data Ring?

Has anyone suggested a ring around the issues related to the Ethereum data (particularly off-chain usage of that data)? We had a short session at the Berlin council, and I’ve spoken to a number of people who’ve expressed interest, so I thought I’d ask. Is it too late to start a new Ring before Prague?  Here are some of the issues we could discuss (these are off the top of my head - not even sure if all of them make sense):

- Is there a long-term solution to the ever-growing data on chain? Can it possibly grow unbounded forever?
- Can the nodes provide better fine-grained control of what data is stored by the nodes?
- Is the community in danger of being “captured” by efforts such as EtherScan, Infura, Google Big Table, CloudFlare which are fully centralized?
- Can off-chain data providers be forced to prove they’ve not manipulated the data they deliver?
- What minimum data requirements do different types of users need:
* dApp devs
* Regular everyday non-dev users of smart contract
* Everyday users who don’t use smart contracts
* Auditors / Accountants
* Industry analists
- Does each different user type need the same or different solutions?
- What happens to existing solutions (blockchain explorers) when the chain shards?
- Will solutions we build apply to multiple different chains (Polkadot, Plasma)?
- Will each Plasma chain have its own explorer?
- Does it make sense to have different solutions for different standards (i.e ERC20 explorer, 721 Explorer)?
- Are there viable business models for providers of already consented-to data?
- Should there be business models and/or ‘data marketplaces’ or does that lead to haves and have-nots?
- How can the nodes be improved related to (a) lessening storage requirements, (b) deliver more useful data, © easing extraction of data for specific uses.
- Can the RPCs be improved? New end points? Missing or extraneous params to existing end points. Are the RPCs on all clients consistent? Are the RPCs well documented?

This is totally just a start. Any help you’all can give is appreciated, of course. Maybe there’s two tracks here. One about the on-chain data and other about the extraction and use of off-chain data.

Even if we don’t have time to form a ring, perhaps we can have a birds-of-a-feather ad-hoc meeting at the Prague council.

## Replies

**Ethernian** (2018-09-23):

Look like the Data Ring is on intersection between “Signaling Ring” and “CoreDev Ring”

There is no CoreDev ring currently. Are they all in [ethresear.ch](http://ethresear.ch)?

There few topics that can be tackled by specialized group of interesting people. If there are any, lets call it **DataRing** ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=9)

Let review it in details:

- [CoreDev] Is there a long-term solution to the ever-growing data on chain? Can it possibly grow unbounded forever?
- [CoreDev] Can the nodes provide better fine-grained control of what data is stored by the nodes?
- [Global] Is the community in danger of being “captured” by efforts such as EtherScan, Infura, Google Big Table, CloudFlare which are fully centralized?
==>unclear what danger do you mean
- [Oracles?] Can off-chain data providers be forced to prove they’ve not manipulated the data they deliver?
- [DataRing] What minimum data requirements do different types of users need:

dApp devs
- Regular everyday non-dev users of smart contract
- Everyday users who don’t use smart contracts
- Auditors / Accountants
- Industry analists

**[DataRing]** Does each different user type need the same or different solutions?

*==> You mean different client?*

**[CoreDev]** What happens to existing solutions (blockchain explorers) when the chain shards?

**[CoreDev]** Will solutions we build apply to multiple different chains (Polkadot, Plasma)?

**[CoreDev, DataRing]** Will each Plasma chain have its own explorer?

*==> I think, yes. **DataRing** can aim to establish common data interchange standart*

**[DataRing]** Does it make sense to have different solutions for different standards (i.e ERC20 explorer, 721 Explorer)?

*==> What do you mean by solution?*

**[DataRing]** Are there viable business models for providers of already consented-to data?

*Should*  there be business models and/or ‘data marketplaces’ or does that lead to haves and have-nots?

*==> Question unclear*

**[CoreDev]** How can the nodes be improved related to (a) lessening storage requirements, (b) deliver more useful data, © easing extraction of data for specific uses.

**[CoreDev, DataRing]** Can the RPCs be improved? New end points? Missing or extraneous params to existing end points. Are the RPCs on all clients consistent? Are the RPCs well documented?

*==> **DataRing** can create a spec and let implement **CoreDev** adopt it.*

---

**tjayrush** (2018-09-23):

Thanks so much for your comments.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> [CoreDev] Is there a long-term solution to the ever-growing data on chain? Can it possibly grow unbounded forever?

The core devs would implement this, yes, but we can discuss the various options. I may have missed it, but I don’t remember seeing any EIPs related to this. It ties in with the next item.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> [CoreDev] Can the nodes provide better fine-grained control of what data is stored by the nodes?

Again, I don’t see any EIPs concerning this issue. As an example, I can choose to run `--pruning archive` or not and I get either 1.5 TB or much, much less. Can I have `pruning archive:4000000`? In other words, archive, but only back to block 4,000,000. It’s obviously possible because you can go from **no** archive to **all** archive. Can we get partial archive? Or how about '–pruning archive:six weeks back` where the node constantly keeps six weeks of full history. In that six week (or ten, or 52, or whatever), the user can extract whatever data they want from the node, and be able to reclaim space that is needlessly kept now. This group can help the CoreDevs understand how useful this would be. Obviously, they don’t see that given the lack of any EIPs related to something like this.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> [Global] Is the community in danger of being “captured” by efforts such as EtherScan, Infura, Google Big Table, CloudFlare which are fully centralized?
> ==>unclear what danger do you mean

Most of my concerns are about the data *after* it’s been extracted from the chain, as is done with the recent Google Big Table effort. Google may be building that database for the world out of the kindness of their heart, but my guess is that they hope people will build applications on that data. Over time, the more people rely on using convenience tools such as APIs built on off-chain data, the more Google has the potential of capturing those applications making it impossible for them to move to other solutions. Google’s pitch: Check out this amazing data, it’s been agreed to by the entire world, ignore the fact that it’s only available through our APIs due to the astronomical size of the data otherwise.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> [Oracles?] Can off-chain data providers be forced to prove they’ve not manipulated the data they deliver?

Again, I’m referring to off-chain data. (I think of Oracles going the other way from outside to in – I’m talking about inside to out.) . For example, I can use EtherScan’s API to retrieve a list of transactions on my account, but they simply send that data to me. I might build an accounting or auditing solution on that API, but how do I know that EtherScan has not made a mistake or is purposefully altering the data? And, getting back to the ‘capture’ issue, if (as is true of EtherScan) they make additions to the data (for example adding `is_error` flags to transactions without being explicit, moving your app to another API will that much more difficult. If instead, APIs that provided off-chain data were explicit about how they derived that data, moving to other providers would be easier. In the best of all worlds, the nodes themselves would be easy enough to run and the access to the data from the node would be useful enough that we wouldn’t need third party APIs such as EtherScan and Big Table.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> [DataRing] What minimum data requirements do different types of users need:

> dApp devs

These users want deep analytics on everything that happens on thier dapps across test and main nets.

> Regular everyday non-dev users of smart contract

This user wants to know where their money is and wants to keep a (potentially close) watch on the smart contract she interacts with.

> Everyday users who don’t use smart contracts

This user just wants to know where their money is.

> Auditors / Accountants

This user wants full details of everything including all incoming and outgoing transactions (both internal and external) as well as all events.

> Industry analists

This user wants cross-block summary statistics, etc.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> [DataRing] Does each different user type need the same or different solutions?
> ==> You mean different client?

I mean different users have different needs. As a way to increase the number of people who run nodes (which would be beneficial to everyone), the nodes could provide more options to different types of people.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> [CoreDev] What happens to existing solutions (blockchain explorers) when the chain shards?

Does anyone see any conversation anywhere about this issue? Whenever I ask people (in person) they literally say “Don’t ask.”  How is EtherScan preparing for sharding? How is Infura preparing for sharding? How are the other open source blockchain explorers preparing or sharding? How about privacy-laden transactions when we start incorporating Z-cash like transactions?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> [CoreDev] Will solutions we build apply to multiple different chains (Polkadot, Plasma)?

Why core devs? I’m talking about blockchain data. If things work out as they seem to be headed, everyone’s data is going to be coming from multiple sources. Does anyone actually think that’s going to work?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> [CoreDev, DataRing] Will each Plasma chain have its own explorer?
> ==> I think, yes. DataRing can aim to establish common data interchange standart

Is this Polkadot? (I’m not sure.)

[quote=“Ethernian, post:2, topic:1438”]

- [DataRing] Does it make sense to have different solutions for different standards (i.e ERC20 explorer, 721 Explorer)?
==> What do you mean by solution?
[/qutoe]

Will there (or should there) arise different explorers/data solutions for the different standards? I.e. will there be different solutions for 721 land records vs. 721 game assets vs. 721 artwork vs. whatever?  Would 721 explorers be different (or should they be) than ERC20 explorers?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> [DataRing] Are there viable business models for providers of already consented-to data?
> Should there be business models and/or ‘data marketplaces’ or does that lead to haves and have-nots?
> ==> Question unclear

The two previous questions try to get at the idea of a common good or community good. Is the `consented-to` data a community good? Should the community, who’s spent all these resources to achieve the amazing feat of coming to agreement on world-wide data, allow themselves to end up in a place where they have to pay for the very data they created? Does the value of the data disappear if the only way we can get to for accounting or auditing purposes it is through a third party such as EtherScan or Google? This is particularly true if Google captures us and doesn’t prove to us that they haven’t manipulated the data. For me, it almost gets to the point where I ask why we’re coming to agreement on the data anyway if we have to ask Google for accounting-quality data.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> [CoreDev] How can the nodes be improved related to (a) lessening storage requirements, (b) deliver more useful data, (c ) easing extraction of data for specific uses.

The core devs aren’t doing this. I think they don’t see it as a problem (this is based on the fact that we see articles arguing why 1.5 TB is not a problem).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> [CoreDev, DataRing] Can the RPCs be improved? New end points? Missing or extraneous params to existing end points. Are the RPCs on all clients consistent? Are the RPCs well documented?
> ==> DataRing can create a spec and let implement CoreDev adopt it.

The one thing here that I think would be a good place to start is to try to get the Parity and Geth RPCs related to tracing to agree. If you want to build audit-quality or accounting-quality data, you really need traces. Parity’s traces are pretty good here, Geth’s not so much.

---

**Ethernian** (2018-09-23):

#### Unfortunately have no time to review all your answers, there are selected comments:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tjayrush/48/23_2.png) tjayrush:

> The core devs would implement this, yes, but we can discuss the various options.

Why should CoreDevs implement what DataRing decides? Intensives are unclear.

========

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tjayrush/48/23_2.png) tjayrush:

> I don’t remember seeing any EIPs related to this. It ties in with the next item.

It is another problem: EIP needs a proposal, No proposal, no EIP.

It is suboptimal and should be changes (I am working on proposal), but it is true for now.

========

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tjayrush/48/23_2.png) tjayrush:

> [CoreDev] How can the nodes be improved related to (a) lessening storage requirements, (b) deliver more useful data, (c ) easing extraction of data for specific uses.

The core devs aren’t doing this. I think they don’t see it as a problem (this is based on the fact that we see articles arguing why 1.5 TB is not a problem).

No, they do! Creating additional interfaces and functionality for business demand is the way for DevCore Client devs to increase the market share of their client and earn money. It is how the business works, IMHO.

**DataRing** may analyse business needs for querying data and create better specification in cooperation with CoreDevs.

---

**jpitts** (2018-09-24):

I’m definitely interested! These are all hugely important issues, wrapped up under the simple term “data”. There are few stakeholder groups in the community evaluating the issues surrounding data and making recommendations for improvements.

At the root of evaluating the significance of blockchain data is the barrier formed by cost. Cost to store. Cost to transfer. Cost to make the information meaningful and useful.

Without designing for open and low-cost access, we open up the possibility of new monopolies or other barriers forming around the tremendous amount of data that will be generated by blockchains and L2 networks.

---

**Ethernian** (2018-09-24):

All in all I see demand for **DataRing** too but we should think more about intersections with other Rings.

The challenge is:

- We should define a core area, where DataRing should be able to produce meaningful results independently from other Rings.
- For other questions, where cooperation with other Rings is necessary, incentives should be clear.

BTW, it sounds like a good assessment question for new Rings.

---

**tjayrush** (2018-09-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png) jpitts:

> At the root of evaluating the significance of blockchain data is the barrier formed by cost. Cost to store. Cost to transfer. Cost to make the information meaningful and useful.

The costs might be born by each member of the community if we can think of ways to promote more people running more nodes that produce much better access to the data. The trouble with cost, I think, comes from the ‘blockchain explorer’ mentality where all the data is extracted from the chain and then somehow re-delivered to the end users. If the node could be made more light-weight and at the same time deliver higher quality results, more people would run more nodes and the costs would be spread out.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png) jpitts:

> Without designing for open and low-cost access, we open up the possibility of new monopolies or other barriers forming around the tremendous amount of data that will be generated by blockchains and L2 networks.

Intuitively, it seems to me that the only workable way to insure ‘low-cost’ is for each participant to bear the cost of the data themselves, but only the cost burden created by their own activity. To me, this translates to “more people running more nodes,” which translates further to “the nodes have to be more flexible and provide better access to the data.” Once people realize the absolute glory of the available on-chain data, and it becomes easier to access, they will gladly run nodes.

---

**tjayrush** (2018-09-24):

One key distinction might be “on-chain” data vs. what I call derived (or “off-chain”) data. For example, the raw block data that goes in to make up the block’s hash, I would call “on-chain”. A list of addresses that appears in a given block can be directly derived from the block, but it is no-where explicitly represented. It is this ‘derived’ data that will, as Jamie puts it, create opportunities for monopolies. The DataRing can concern itself with both the “on-chain” data (which will depend on action by CoreDevs) and the “off-chain” data which wouldn’t.

There’s probably a huge number of intersections with the WalletRing too as they are inherently users of the data. For them, things like token balances are both on-chain (if they are running their own nodes) and off-chain if they are not and are relying on some third-party API (as some do). That reliance on the third party APIs would be one of my main concerns.

---

**DaveAppleton** (2018-09-24):

I think that there is certainly a space for limited explorers. I built ERC223 and ERC20 explorers to meet the needs of specific users (will open source when I finally get round to cleaning them up).

---

**tjayrush** (2018-10-27):

Is there anyone at the Status Hackathon this week who would like to help me flesh out the agenda for the Data Ring? Or, alternately, is anyone already working on an agenda for the Data Ring?

The data ring agenda is here: I will try to add some stuff there today, but if you have additional agenda items, please let me know here or directly edit that file.

https://hackmd.io/d3GqzRa4TpO_oDg2wah1_A

---

**yiseul** (2018-10-27):

![:heart_eyes:](https://ethereum-magicians.org/images/emoji/twitter/heart_eyes.png?v=9) I’m interested in joining the ring and do I have to sign up or can just show up in the venue? (once it’s fixed)

---

**jpitts** (2018-10-28):

I would just come on over to the event, we want to know how many are coming but will not turn participants away ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**valo** (2018-10-29):

Where is the category that was mentioned about the data ring topics?

---

**tjayrush** (2018-10-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/valo/48/968_2.png) valo:

> Where is the category that was mentioned about the data ring topics?

[@jpitts](/u/jpitts) Can you help us get a ‘data ring’ category in the Eth Magicians discussion group?

---

**tjayrush** (2018-10-29):

Notes on discussion about the Eth Magicians Data Ring: [Council of Prague Data Ring: Notes from Session 1](https://ethereum-magicians.org/t/council-of-prague-data-ring-notes-from-session-1/1715)

---

**jpitts** (2018-10-30):

The Working Groups / Data Ring is now set up…

https://ethereum-magicians.org/c/working-groups/data-ring

