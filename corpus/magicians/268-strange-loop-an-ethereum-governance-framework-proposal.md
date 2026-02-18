---
source: magicians
topic_id: 268
title: "Strange Loop: An Ethereum Governance Framework Proposal"
author: danfinlay
date: "2018-05-03"
category: Magicians > Process Improvement
tags: []
url: https://ethereum-magicians.org/t/strange-loop-an-ethereum-governance-framework-proposal/268
views: 8151
likes: 58
posts_count: 27
---

# Strange Loop: An Ethereum Governance Framework Proposal

Repasting from the possibly more dynamic github here: [GitHub - danfinlay/ethereum-strange-loop: A proposal for adding a governance layer on top of the Ethereum blockchain.](https://github.com/danfinlay/ethereum-strange-loop)

# Ethereum Strangeloop Proposal

## Motivations

Hard forking allows protocol evolution, and other potentially valuable community services (cough, funds recovery), but contentious forks today can divide network value and create excessive overhead for that blockchain’s community.

Currently, one stance that is popularly presented is “no forks” as the simplest solution to keeping one chain, but if forks can be made less contentiously, and with less overhead, we should consider that system.

## Background

At the EIP0 unconference, we discussed governance and how it can work at various layers of Ethereum. While layer two solutions, and even layer one solutions can be useful, interesting, and maybe necessary in the long term, when there are bugs or contention in the protocol itself, hard forking is the only option for resolving those issues, and so my focus in this proposal is on smoothing out the process of making hard forks less contentious.

[![flow chart](https://ethereum-magicians.org/uploads/default/optimized/1X/9ffdd8e252de524e3518ccddfcef87ae72293134_2_577x500.png)flow chart1942×1682 324 KB](https://ethereum-magicians.org/uploads/default/9ffdd8e252de524e3518ccddfcef87ae72293134)

Here is a flow chart, showing which parts of the current process could be bypassed.

I do not claim that this solves contentious hard forks, but I will present a framework that allows networks of people to assemble and strongly signal the ideals of their preferred blockchain, and allow clean forks along these ideological lines, avoiding the “infinite immutability debate” loop that the Ethereum blockchain is currently in.

## Introduction

I will propose a framework for the development of some infrastructure that can be built on top of Ethereum today, with no hard forks, that can allow community members to strongly align along their blockchain ideologies. Any governance layer can be placed within this framework, and each user ultimately has control of their own client, which this framework fully respects.

I call this proposal Strangeloop as a nod to Douglas Hofstadter’s “Gödel, Escher, Bach”. A strange loop is a system that has some self reflection, and so a capacity for self improvement. By bending from within the protocol to without, I believe we can complete a strange loop, and make Ethereum the self improving yet community representative system that it should be.

As you’ll see, this proposal lives on layer 2 and layer 0, with some possible optimizations at layer 1. Since it links layer 2 and 0, it forms a feedback loop.

## Implementation

### Consistent Hard Fork Proposal Format

[EIP 867](https://github.com/ethereum/EIPs/pull/867) is merged, but no one is currently proposing their fund recoveries in this format. Part of this is because the advantage of using the format today is small: While the format is machine readable, no machines currently read it.

The first step is to create a smart contract registry for people to publish these hard fork proposals (by hash), with that hash readily available over p2p file sharing protocols.

### Client Optimization

This proposal would greatly benefit from the client developers taking the time to make it easy for their clients to consume proposals posted to this registry, and expose those fork choices as parameters to their clients, so that clients are more freely in control of their own fork choice rules. If clients implement this one generic feature, they would no longer have overhead of implementing state change hard fork proposals.

This isn’t required, but users who are fork friendly are likely to pursue clients that give them the most control over their fork choice rules.

### Fork Signaling Framework

A new smart contract format should be developed, that allows a user to define whether at that moment they are in favor of any given fork or not. This could be as simple as anyone publishing a contract that exposes one method:

```auto
function supportsProposal(address proposal) returns (bool);
// maybe shouldn't return bool, but a ternary, to support "undecided".
```

Under the hood, this user can use any method they want, either hard-coding their current opinions, delegating to a friend or a distribution of trusted others, or delegating to a democracy. It’s up to that user.

### User Client Wrappers for Fork Choosing

The last layer is a program users can use to wrap their Ethereum clients, which knows how to pass hard fork parameters to that client.

There can be many implementations of this client wrapper, and this layer should represent that user’s preference for choosing hard forks.

One simple example would be a coin voting scheme, where a user prefers to point at some carbon-vote `supportsProposal` implementation, and just goes with the coin majority.

A verion of this wrapper that I personally prefer involves delegating trust, in a liquid-democracy like way, but with the ability to assign quorums. For example:

- I’ll do any fork that I explicitly publicly supported.
- If I haven’t voiced an opinion publicly, and if 95 of the 100 stake holders I follow signal they will fork, then fork.

Or maybe:

- If any one person from team A supports it, AND any two people from team B, AND everyone from team C, then fork.

I think that this kind of transitive trust with a quorum model is powerful because it allows users to require very high degrees of consensus before agreeing to a hard fork, while also allowing users to align their fork choice rules along the ideologies that most appeal to them. As long as these communities stay aligned to their purposes, after an (ideally early) ideological hard fork, the split ideology chains should be able to live in peace and parallel, even potentially communicating via hubs and relays.

For more signaling strategies, check out:


      ![](https://github.githubassets.com/favicons/favicon.svg)

      [github.com](https://github.com/danfinlay/ethereum-strange-loop/tree/master/signaling-methods)





###



A proposal for adding a governance layer on top of the Ethereum blockchain. - danfinlay/ethereum-strange-loop










## Conclusion

Since users can implement any fork choice rule they want, and some forks are good decisions, and forks are most powerful when keeping the most people in sync at once, I think signaling with high quorum requirements could be a powerful “good enough” hard-fork governance framework for users to start iterating on what mechanisms they think are most effective for coordinating on hard forks.

## Replies

**danfinlay** (2018-05-04):

The top post was marked as spam, but [the full post can be read here](https://github.com/danfinlay/ethereum-strange-loop/).

### This is a reply to that post:

While I presented that anyone could choose their fork choice democracy, I definitely think that a user-defined liquid delegation of trust has a lot of great features.

Another use case for that model:

- A user can require the fork support of every Dapp they rely on for their fork choice rule
- Dapps can require the fork support of smart contracts they depend on as critical infrastructure in their fork choice rule.

Yes, this would put the most consensus power in the hands of the smart contracts that provide the widest ecosystem utility, but maybe it should be that way, and we can start nudging this governance layer towards the smart contracts that people choose to rely on the most, which could eventually be in part because of respect for their fork choice policies.

---

**jpitts** (2018-05-04):

Great concept and name!

The notion that users can signal their values about blockchain rules, and that the signal would result in users coalescing around chains that suit them is elegant.

Is it making it too complex to consider that more nuance should be provided in a user’s or stakeholder group’s signal on a proposal? A proposal may require more than “yay, nay, or null”, and require a specific value or set of values from users and stakeholder groups in order to have the proposed outcome.

Example (user-definable preferences in brackets):

> I support restoring the ether, but I want [10%] of the ether to be donated to [Fund A]. This proposal won’t happen if the donation exceeds 25%.

But if we can just get us to “yay, nay, or null”, that would be wonderful.

The delegation approach in Strange Loop can be organized in tandem with a proposal for how stakeholder groups will signal to the community. I expect dapps will emerge to help users understand the stakeholder groups’ signals and then set their own choices in the client.

Also, are there privacy considerations? Would this configuration be local?

---

**danfinlay** (2018-05-04):

Thanks! I named it because I was asked what it was called. All the coolest proposals have cool names anyways.

I think more sophisticated parameterization would be a fantastic feature, may be easier to add later, but makes lots of sense. Combined with the pricacy point, seems like a good use for some kind of zk-proofs, or at least a selective-disclosure identity platform in the meanwhile…

---

**jpitts** (2018-05-04):

The dapp-related repercussions are a huge part of why forks are so dire. A dependency tree feeding into a user signal could get very complex, but no doubt would be great fun for certain engineers to work on LOL.

A dapp may need to (or wish to) alter how it functions in the fork, or liquidate its representation in the fork, and will need to communicate the implications and options to its users.

Connecting a user’s dapps into their fork configuration is an opportunity to facilitate this communication.

---

**lkngtn** (2018-05-04):

This would be extremely valuable to implement, not just for contentious community splits but for routine forks as well.

In the event of an emergency hardfork that is prompted by an a protocol layer consensus bug, or a 51% attack, a pre-established web of transitive trust will allow for the community to react much quicker to resolve the issue. Being able to react quicker in the event of a 51% attack offers both a usability and security improvement for all users regardless of their views on fund recovery as a social good.

Users and developers alike face the challenge of gauging the sentiment of different groups within the community, making it difficult to make informed decisions. As the platform matures and there is more value at stake, there is an increasing incentive for sybils and sockpuppets to astroturf social media platforms, making them very unreliable signals. By pushing signaling primarily on-chain, groups can self organize (sort of like stakeholder interest daos), and individual node operators can weight the opinions of different stakeholders as they see fit.

My biggest concern is that a community split would become hostile and in the worst case slow development and reduce network effects of the platform, but if core developers generally support mostly the same technical improvements and chains maintain interoperability/compatibility the ability to “shard” social consensus is really powerful. The chain which is least contentious/opinionated from a governance perspective will probably still emerge as a common base layer/hub, but many more opinionated chains would allow the community to explore a much larger design space more rapidly.

---

**Arachnid** (2018-05-04):

Nice proposal!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danfinlay/48/4187_2.png) danfinlay:

> EIP 867  is merged

Please don’t treat this as any kind of signal - it just means it’s formatted correctly.

---

**djosey** (2018-05-04):

love it. when I think about chain splits (at least ones that happen over things like tokens being frozen), I think of value being diluted and destroyed and confusion created, while some value is recovered by the parties who needed the fix… but thinking about this type of feedback loop, it seems like, paradoxically, the more chain splits that happen, the lower that economic shock could be for each individual fork. if there were chain splits daily on miniscule issues and grievances, the community should get better and better at wrapping their head around their understanding of what chains to support and why, and what that consensus around a fork means.  you can never stop forks from happening, but if more and more chain splits happen all the time, then the desires and preferences of the majority of users who support the dominant chain would be reinforced and apparent, and likely the economic shocks of each split should drive lower and lower over time.

reduce fork friction with governance on layer 2 driving changes on layer 0… why not?

---

**danfinlay** (2018-05-05):

Depending how forky you expect the world to become, we might need to revisit [EIP 155](https://github.com/ethereum/eips/issues/155) with a `v` parameter of more than one byte, to ensure easier replay attack protection in a world with more than 114 ethereum forked chains.

We might also want to include a `new_fork_network_id` as parameter in its [EIP 867] fork proposal file.

You would want to ensure the new proposed ID was globally unique, ideally ensuring that no two forks produce the same `network_id`.

Any random oracle could be used, or maybe just `hash( hash(proposal) + previous_block_hash)`? Maybe Cosmos over to Dfinity for some random data?

---

**danfinlay** (2018-05-05):

This is a strong point, I’m going to update my flow chart to better emphasize it.

---

**danfinlay** (2018-05-06):

I’ve added a couple governance algorithm proposals to the Strange Loop repo. Posting one at a time for easy threading:

# Soft Flow

### A signaling strategy for the Strange Loop hard fork framework.

Signals can take many forms, from soft, off-chain signaling like social media, to more hard commitments, like burning assets in a way that they will only be usable on a resulting chain.

Users can publish the conditions under which they would fork. This could take the form of any smart contract, as implied by the Strange Loop `supportsProposal` method.

The implementation of this method can have policies like “all of us or none of us”, with a list of required other accounts that should signal a similar support.

The algorithm might go like this:

The WouldSupportIf procedure:

- If the account has explicitly expressed they would or would not, return that result.
- Define set D, the set of accounts that the current account that requires wouldSupportIf.
- Define set W, as the subset of D that either:

Would support the fork.
- WouldSupportIf the caller supported the fork.
- Returns true for its own wouldSupportIf procedure.

If D = W, return true.

---

**danfinlay** (2018-05-06):

# Hard Flow

### A coordination strategy for the Strange Loop hard fork framework.

An extension of Soft flow that includes on-chain enforcement.

Beyond signaling, hard economic commitments could allow accounts to unambiguously define their commitment to a particular fork.

This could be implemented by encoding `wouldSupportIf` logic in a smart contract that controls some collateral or asset. This asset could be a small deposit, or it could be a commitment for a contract to self destruct on one side of a fork.

For other accounts implementing `wouldSupportIf` flows that depend on this hard-signaling account, the account may weigh this commitment more heavily than a normal `true` from  `wouldSupportIf`, since this dependency is now more grave.

This would require a revised version of the `wouldSupportIf` method that defines the different weight the account would give a dependency if it hard-commits in different ways to that fork proposal. Since there are different ways to hard-commit, this could be a bit complicated to implement, and would benefit from some standardization.

---

**MicahZoltu** (2018-05-06):

Can a moderator flag this post as “not-spam”?  I’m unfamiliar with how Discourse moderation tools work…

---

**jpitts** (2018-05-06):

The Discord “system” account was doing this, it seems that having multiple posts to the same domain (in this case GitHub) triggered it.

I unhid them and will henceforth keep an eye on this “troll” ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=9) !

---

**Arachnid** (2018-05-06):

V can already be more than one byte. Personally, I’m a fan of changing the network id on every hard fork, no matter how uncontentious, but that’s not something we’ve historically done.

---

**andytudhope** (2018-05-10):

Very interesting stuff Dan - a far better read than the 999 thread ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danfinlay/48/4187_2.png) danfinlay:

> If I haven’t voiced an opinion publicly, and if 95 of the 100 stake holders I follow signal they will fork, then fork.

One simple question about this example (I know it is contrived and you provide some clearer and better ones in subsequent comments) but if this is one of the defaults, and a lot of people choose to use logic like this, would it not result in endless stalls?

I like the idea of user-defined liquid delegation of trust and think that the potential definitions you give there for stake holders that are required to take action likely hints at an answer ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12)

---

**danfinlay** (2018-05-10):

> if this is one of the defaults, and a lot of people choose to use logic like this, would it not result in endless stalls?

Maybe! I’m deliberately not prescribing exact governance models here. If everyone has very high consensus thresholds set for hard forking, it’s entirely possible forks never happen, and if so, that’s a very conservative community.

But like you said, this already hints at how a pro-fork community might move forward: Either by getting key stake-holders on board, or by conceding that they are a fragment of the community to whatever extent.

My personal theory is that even with high consensus thresholds, if a dependency graph were drawn, we’d see the community right now is favorable to performance improvements, and recovery forks are contentious for a variety of reasons that could be overcome with better signaling:

- Fear of forking without full community buy-in.
- Fear of forking and being liable for the recovery (fear of future coersion).
- Fear of centralized power making these decisions.

If people just spread their dependency graph widely, they could be very picky about what recovery forks they would ever support, and yet still potentially find cases that are supported widely enough that they happen could endorse without falling into any of these traps.

---

**Ethernian** (2018-05-10):

Hmm…

unknown groups of unknown actors (even not sybil protected) are voting on protocol changes.

Votes of that different voters and voter groups are summarized somehow and change will be enforced.

It is easily exploitable, don’t you think?

But I like the proposal as a technical outline

---

**jpitts** (2018-05-11):

The groups and their constituent actors and processes could easily be knowable to the users, and registered on the blockchain. They can even be confirmed in person. That is about as known as it gets on the internet.

I would say that these groups are not as much voting on a change as they are signaling which protocol attributes they conclude fit the needs or outlook of their subscribers.

The summarized somehow isn’t as arbitrary as it may seem. It can be quite clear to the user what is happening in the groups they subscribe to.

(removed an allegory that was not relevant to my points)

---

**danfinlay** (2018-05-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> unknown groups of unknown actors (even not sybil protected) are voting on protocol changes.
>
>
> Votes of that different voters and voter groups are summarized somehow and change will be enforced.

This is a misrepresentation of the proposal.

First of all: The Strange Loop framework does not require any particular governance pattern, so neither voting nor anonymity nor any assumption actually applies to it. Any governance process could be opted in to by the user of a blockchain using this tool.

I think you’re critiquing what I called “Soft Flow”, a signaling governance system for Strange Loop. In response to your concerns:

- It’s sybil resistant because each person would choose what other accounts they want to coordinate with.
- It’s not actually “enforced” in any blockchain-wide sense, only on the individual user level.

---

**Ethernian** (2018-05-16):

> It can be quite clear to the user what is happening in the groups they subscribe to.

I would like to see/accept this proposal exact as it was titled: a framework.

A framework that is still to be implemented into ready-to-use product, when exact all this **can be**’s must be provably implemented. Even a framework becomes accepted, an particular implementation must be validated later once more. No implementation of the framework should be accepted automatically just because the underlying framework was accepted.

and once more: any automatically enforcement after some boolean function mapping votes into boolean is dangerous, because it pretend to be safe and trustless, but can be easily forked out. We use word “governance”, but it is a signalling, indeed.


*(6 more replies not shown)*
