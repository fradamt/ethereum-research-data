---
source: magicians
topic_id: 236
title: Can we make forks less dire?
author: jpitts
date: "2018-04-25"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/can-we-make-forks-less-dire/236
views: 2096
likes: 13
posts_count: 11
---

# Can we make forks less dire?

Let’s assume that there is an expected fork because social consensus on a proposal was not reached, and that for various reasons it is likely that both forks will persist and have a similar number of active users and developers.

Would this definitely create permanent, separate universes as happened with Ethereum Classic? What are the ways to mitigate the impact of a major fork event and maintain our ecosystem encompassing multiple Ethereum-compatible networks?

One irony is that Polkadot might be an important part of such an ecosystem.

Consider the various areas of impact:

- technical governance, protocol development, dapp development
- nodes, infrastructure
- usability, for firms and for individuals
- identity, e.g. for what is considered the primary network we currently use “ETH”, “ether”, “ethereum network”, “ethereum mainnet”
- contract inter-op
- firms, multi-sigs, governance contracts, individual accounts, keys
- transaction history

Or is this just too big to even put our head around?

## Replies

**lrettig** (2018-04-25):

Thanks for bringing this up. I think this is a really interesting, important question. To me it’s pretty clear that the future is not a “one chain to rule them all” future but rather a future of many chains serving many purposes, transacting and communicating with each other. I don’t have answers to your questions but I think it’s a worthwhile area of inquiry.

---

**MicahZoltu** (2018-04-26):

I think the first hurdle we need to get past is how do we allow for each branch of a fork to have a reasonable chance at success?  Right now, since exchanges are the dominant “use-case” for most blockchain projects whoever gets the ticker symbol has a *huge* leg up on the other branches.

Hopefully, we’ll eventually see popular apps and payment processors dominating the space, in which case *they* will likely be a major driver of which chain gets preference, rather than exchanges via ticker symbols.

In a perfect world we could have contentious forks just result in a community split where both communities are happy to plod along separately with slightly different rules but there is no animosity and no preference given for one or the other.  I wish we lived in such a magical place…

---

**fubuloubu** (2018-04-26):

This is why ether needs to be used less as a store of value. Used just as a method to pay for gas, allotments of ether would be spread around a lot more and lost/stolen ether would get less painful. The great thing about tokens is that if a poor decision was made with them, someone could just make another smart contract and fork the userbase without forking the network. This is probably wishful thinking however.

Another interesting thought is how the plasma paradigm could play into this. Could you link those networks together and sibling plasma chains somehow?

I did just come back from a pub night, so this could be affecting my thoughts some ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**jpitts** (2018-05-04):

This is to link to [@danfinlay](/u/danfinlay)’s “Strange Loop” proposal for users to signal and (potentially) coalesce around Ethereum-based networks that suit them.



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danfinlay/48/4187_2.png)
    [Strange Loop: An Ethereum Governance Framework Proposal](https://ethereum-magicians.org/t/strange-loop-an-ethereum-governance-framework-proposal/268) [Process Improvement](/c/process-improvement/6)



> Repasting from the possibly more dynamic github here: https://github.com/danfinlay/ethereum-strange-loop
> Ethereum Strangeloop Proposal
> Motivations
> Hard forking allows protocol evolution, and other potentially valuable community services (cough, funds recovery), but contentious forks today can divide network value and create excessive overhead for that blockchain’s community.
> Currently, one stance that is popularly presented is “no forks” as the simplest solution to keeping one chain, but if fo…

---

**fulldecent** (2018-05-20):

There is no solution.

The solution is to not make contentious forks. I am working with traditional entities like governments and industry to adopt Ethereum. Traditional entities usually only consider hyper ledger. If we want to avoid the threat of extinction then we need to act like a failed fork is a risk of extinction.

Here are some initiatives I support, which are related to this discussion:

- Repeal and replace https://github.com/ethereum/EIPs/blob/master/EIPS/eip-155.md
 What happens when an Ethereum-foundation-supported fork fails? We will have the old version and the new version with the same ID. This is an existential threat. At present, every time there is a contentious fork we need to change the rules. Last time, Ethereum Classic started and we created EIP-155. Next time there is a fork they will both use the same chain ID, again, and we’ll need to scramble to fix it. Nobody is going to fork Ethereum and choose a new chain ID, everybody wants /their/ fork to be canonical. SOLUTION: do not use chain IDs, use genesis block IDs and make a new genesis block on each fork. I can write this up into a formal specification.
- Immutability Enforcement Proposal, stop dicking around and accept it as draft, then debate it on merit. I’m working with banks and government to record official records on blockchain. Remember that in most of the world Ether is an asset not a currency. The United States Food and Drug Administration does not care if you lost EVM-gas-utility-tokens (i.e. Ether) on a Parity wallet. The US FDA cares that records recorded on the blockchain will stay there.
- Encourage alternate EVM implementations and improve the Yellow Paper so that it is actually implementable.

---

**phiferd** (2018-05-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> The solution is to not make contentious forks

First, anyone can fork at any time. Users, miners, and developers can choose to follow them, or not. The people that decided not to follow the fork don’t get to choose for the people that do and vice versa. Saying that we shouldn’t allow contentious forks overestimates the control that “we” have and is a bit like saying the US could avoid contentious elections by just getting everyone to agree that we should all just be Democrats. Problem solved.

Second, is the issue with contentious forks or forks that make irregular state changes? Although these two sets certainly intersect, they are not the same. What if (by whatever measure is accepted) a fork with the irregular state change is deemed to be uncontentious?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> The United States Food and Drug Administration does not care if you lost EVM-gas-utility-tokens (i.e. Ether) on a Parity wallet

No, they don’t, I’m sure. ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)  However, what if they’re affected? Are you still confident they won’t care?

I think it’s critical for everyone to understand the costs of a *split chain*, but I don’t see how rejecting all irregular states changes necessarily follows from that observation.  What if a particular irregular state change would prevent a split chain?

---

**fulldecent** (2018-05-29):

- Hiding ulterior motives and pretending that there is technical problem with the Immutability Enforcement Proposal
- Not doing what you are supposed to do because of personal reasons, and then NOT resigning honorably like @pirapira did

Personally, I am offended by the above two items. If you are instead offended by the words I’m using then sorry my word choice has been suboptimal.

---

**fulldecent** (2018-05-29):

ALL contentious forks have a serious cost, I’m not just focused on irregular state changes.

The US FDA will not have funds in a Parity wallet. But imagine if the FDA were to regulate that certain information about drugs should be “on the main net Ethereum blockchain” (a gross oversimplification). In this case, the FDA would need to maintain an up-to-date opinion on which fork was canonical. Every time we propose a hard fork there is a risk that FDA or some other entity does not recognize the new version.

We (each community member, not just Magicians) should not… --> We should support hard forks only if there is a SERIOUS benefit. And if there is any chance it is contentious then SERIOUS should be >> $2B USD.

---

On the other hard, the FBI might have funds in a Parity wallet. And the FBI can detain people if the community enacts a change which discriminately takes money which is in the custody of the FBI. Very unlikely scenario here.

---

**phiferd** (2018-05-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> The US FDA will not have funds in a Parity wallet

Not sure what you mean here – obviously, the Parity multisigs are not the only way things can go wrong with an application/data on the Ethereum blockchain.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> But imagine if the FDA were to regulate that certain information about drugs should be “on the main net Ethereum blockchain”

If that information is authoritative and referenced many other applications, yes – a contentious hard fork will be problematic.  However, it’s not hard to see that an issue with that information (e.g. incorrect information) that, for technical reasons, cannot be amended could be a major issue for the FDA.

My point is only that saying “we shouldn’t pursue contentious hard forks because the FDA wouldn’t want us to” makes the assumption that there is no scenario in which they wouldn’t be the ones *pushing* for a contentious hardfork. Why is that necessarily true?

In fact, **the more critical the data is that they are storing on the blockchain, the more likely they (or anyone) will be to push for a hardfork** in the event that some issue arises that cannot be resolved in any other way.

Also, note that the type of problem we’re talking about here can’t be solved just by having insurance.

---

**fulldecent** (2018-06-03):

Here is the only important point I have, restated.

- Any change to the Ethereum client which is incompatible with the current software is a hard fork.
- Hard forks cost up to $2B if a bunch of people dislike the new feature.
- So the feature better be worth a lot more than $2B.

