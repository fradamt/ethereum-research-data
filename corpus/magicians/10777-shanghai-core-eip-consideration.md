---
source: magicians
topic_id: 10777
title: Shanghai Core EIP Consideration
author: timbeiko
date: "2022-09-09"
category: Magicians > Process Improvement
tags: [hardfork]
url: https://ethereum-magicians.org/t/shanghai-core-eip-consideration/10777
views: 12221
likes: 49
posts_count: 47
---

# Shanghai Core EIP Consideration

**Note: edited after discussing on [AllCoreDevs 147](https://github.com/ethereum/pm/issues/616) to reflect consensus amongst client teams.**

After The Merge, we will have a 5 week period from Sept 23 to Oct 27 without any AllCoreDevs or Consensus Layer calls. Despite not having formal weekly check-ins, it would be good to keep making progress on planning the Shanghai network upgrade. Here is a proposal for how to organize this in a more asynchronous way.

1. EIP Champions use the shanghai-candidate topic to signal they’d like to be considered for the upgrade. Either by creating a new discussion thread, like this, or adding the label to an existing discussion-to link, like this. This will allow people to quickly see which EIPs want to be proposed. Notify anyone who has signalled on Github that they want their EIP considered to add this tag.
2. During this period, client teams, researchers and EIP champions are encouraged to use the tagged Ethereum Magicians thread as the main place to discuss the technical details of proposals.
3. For EIPs which require more synchronous discussions, organize breakout rooms which are advertised on the EIP’s EthMagicians thread, ethereum/pm and the R&D discord.
4. On Thursdays 14:00 UTC, have optional #party-lounge sessions in the R&D discord to discuss EIPs, general planning, etc. Unlike ACD/CL calls, there is no expectation that all client teams would be present or that the scope of the upgrade would be decided in these, but they should be useful for general context sharing.

It is worth noting that the goal of this month is to move forward the technical specifications of the EIPs and for client teams to familiarize themselves with them, **not** to update/change the scope of the Shanghai upgrade. Discussions about this will resume on the next AllCoreDevs call, [scheduled for Oct 27th](https://github.com/ethereum/pm/issues/624).

For reference, the list of EIPs currently Considered for Inclusion in the Shanghai upgrade can be found [here](https://github.com/ethereum/execution-specs/blob/master/network-upgrades/mainnet-upgrades/shanghai.md#eips-considered-for-inclusion):

> ### EIPs Considered for Inclusion
>
>
>
> Specifies changes potentially included in the Network Upgrade, pending successful deployment on Client Integration Testnets.
>
>
> EIP-3540: EVM Object Format (EOF) v1
> EIP-3651: Warm COINBASE
> EIP-3670: EOF - Code Validation
> EIP-3855: PUSH0 instruction
> EIP-3860: Limit and meter initcode
> EIP-4895: Beacon chain push withdrawals as operations

## Replies

**MicahZoltu** (2022-09-09):

I would also like to see a Discord channel where we can have more fluid discussions around Shanghai planning.

---

**gcolvin** (2022-09-09):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> Use the Ethereum Magicians thread as the main place for client teams & EIP champions to discuss the technical details of proposals.
> q=is%3Aissue+breakout) and the R&D discord.

You mean the Discussions-to thread for each EIP?

---

**matt** (2022-09-09):

Proposal to include EIP-3074: [Shanghai-candidate: EIP-3074](https://ethereum-magicians.org/t/shanghai-candidate-eip-3074/10781)

---

**axic** (2022-09-09):

Added [Topics tagged shanghai-candidate](https://ethereum-magicians.org/tags/c/eips/core-eips/35/shanghai-candidate) to a bunch of Ipsilon-driven proposals.

---

**timbeiko** (2022-09-09):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> You mean the Discussions-to thread for each EIP?

I’m fine with either adding the topic to the existing threads, like [@axic](/u/axic) just did, or creating a new one if the EIP champion judges that to be better, like [@matt](/u/matt) did. The important thing, I think, is for all of the candidates to show up [here](https://ethereum-magicians.org/tags/c/eips/core-eips/35/shanghai-candidate).

---

**ralexstokes** (2022-09-09):

I think this plan makes a lot of sense and I’d support moving ahead with it.

Added `shanghai-candidate` tag to EIP-4895 discussion: [EIP-4895: Beacon chain withdrawals as system-level operations](https://ethereum-magicians.org/t/eip-4895-beacon-chain-withdrawals-as-system-level-operations/8568)

withdrawals are a must for shanghai

---

**gcolvin** (2022-09-09):

So, can add tag to things to here:  [Topics tagged shanghai-candidate](https://ethereum-magicians.org/tag/shanghai-candidate).

---

**tvanepps** (2022-09-09):

can’t we just use #allcoredevs ?

---

**ajsutton** (2022-09-10):

Definitely keen to give this a try and evaluate how it worked. More than just being able to make progress in the Devcon period, it is potentially a good step towards making more ACD discussions async. More async means more time zone, family and work schedule friendly while also creating a better record of the discussion.

---

**gcolvin** (2022-09-10):

after the dust settles

---

**gcolvin** (2022-09-10):

They don’t all show up at `https://ethereum-magicians.org/tags/c/eips/core-eips/35/shanghai-candidate`.  Try https://ethereum-magicians.org/tag/shanghai-candidate.

---

**MicahZoltu** (2022-09-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tvanepps/48/3406_2.png) tvanepps:

> can’t we just use #allcoredevs ?

I find #allcoredevs to be a good place to ask general protocol questions and get a relatively quick answer.  I am a bit loath to fill that channel with Shanghai planning discussion which I suspect will be a bit voluminous, and potential drown out other protocol questions people have.

---

**gcolvin** (2022-09-10):

Actually, everything except Beacon Chain Withdrawals is an EVM proposal, for which we already have a channel:  [Discord](https://discord.com/channels/595666850260713488/706868829900505180)

---

**timbeiko** (2022-09-13):

Thanks - updated in the first post of this thread!

---

**timbeiko** (2022-09-13):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> I find #allcoredevs to be a good place to ask general protocol questions and get a relatively quick answer. I am a bit loath to fill that channel with Shanghai planning discussion which I suspect will be a bit voluminous, and potential drown out other protocol questions people have.

I’m potentially in favour of this, but I want to make sure it’s something that client teams find valuable and start with what their needs are vs. something that’s first for everyone else and becomes a drag for client teams to keep up with ![:sweat_smile:](https://ethereum-magicians.org/images/emoji/twitter/sweat_smile.png?v=12)

---

**ajsutton** (2022-09-13):

Personally I would have thought #allcoredevs was where discussions like what goes into the next hard fork belong (ie stuff that would be discussed on an ACD call) and if we need to we’d split out a different channel for asking protocol questions. The challenge is that as part of doing core dev work there’s a need to understand the protocol and asking in #allcoredevs is good for that, but a general “learn about the Ethereum protocol” is not something core devs will be able to keep up with.

A #protocol-questions type channel is likely to become general community support quite quickly and just be too hard to keep up with. Discord just isn’t the way to scale that kind of learning - it needs something more persistent like blogs, talks etc.

---

**timbeiko** (2022-09-14):

I think we’re maybe misunderstanding each other ![:sweat_smile:](https://ethereum-magicians.org/images/emoji/twitter/sweat_smile.png?v=12) My rationale for splitting up the channel wasn’t to have somewhere the community can ask protocol questions, but a separate place where we can discuss the “project management” aspect of Shanghai. I’m fine if that’s #allcoredevs, but given that these conversations tend to have high volume, keeping that channel less active might be good.

That said, the risk of another channel dedicated to project management which is open to everyone is that it becomes even higher volume, client teams ignore it, and it’s worse than useless because it’s a productivity drag and paints a picture which doesn’t line up with whaat client teams actually want…!

---

**timbeiko** (2022-09-19):

Re: #shanghai-planning, we agreed to **not** have it until the ACD calls resume on October 27th, this way people don’t feel they need to monitor a new channel or risk missing changes to the upgrade. We can discuss whether to add the channel on the [next ACD](https://github.com/ethereum/pm/issues/624).

---

**mcdee** (2022-09-19):

[@ralexstokes](/u/ralexstokes) is [EIP-4788](https://ethereum-magicians.org/t/eip-4788-beacon-state-root-in-evm/8281) in scope for Shanghai?

---

**ralexstokes** (2022-09-19):

Not at the moment. It was introduced to support “pull” style withdrawals and we have generally agreed to go the “push” route for handling withdrawals from the CL.

Separately, it would unlock a lot of use cases for staking pools, etc. so I’d love to see some version of this EIP land on-chain eventually. I’d also support inclusion into Shanghai but I’d want to hear more demand in the context of the other priorities before putting more time into moving it along myself.


*(26 more replies not shown)*
