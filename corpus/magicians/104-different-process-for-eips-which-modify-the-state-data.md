---
source: magicians
topic_id: 104
title: Different process for EIPs which modify the state data?
author: jpitts
date: "2018-03-28"
category: Magicians > Process Improvement
tags: []
url: https://ethereum-magicians.org/t/different-process-for-eips-which-modify-the-state-data/104
views: 1087
likes: 3
posts_count: 8
---

# Different process for EIPs which modify the state data?

GitHub user [fubuloubu](https://github.com/fubuloubu) commented on [Meta EIP 956](https://github.com/ethereum/EIPs/pull/956) that the EIP process should not be concerned with signaling changes to state. This leads to an interesting question: should there be a different process for deciding on modification to the state data?

> Perhaps the addition of a line stating that EIPs are not meant to propose changes to the state of Ethereum, only the Protocol itself, might assuage this concern of “bailout” proposals being a problem.
>
>
> You could still suggest an EIP that implements a process for state changes and communicating them to other clients through the Ethereum Protocol, but that should be it’s own discussion regarding the benefits/difficulties with that approach (like we had on 867). The EIP process should not be concerned with signaling changes to state, that is up to the wider community. We already have mechanisms for this e.g. hard fork.
>
>
> https://github.com/ethereum/EIPs/pull/956#issuecomment-376939093

Could it be helpful for there to be a new type of Standards Track / Core EIP which covers modifying the state data?

Considering the controversies surrounding rescuing stolen or stuck ether, Core EIPs which involve modifications to the state data may require a more deliberative acceptance process than Core EIPs which involve modifications to the protocol. Such a decision process involving state modification may not only be technical in nature, but involve ethics, philosophy, and law.

## Replies

**DanielMReed** (2018-03-28):

I agree this should be created, however I think it should be seperated form the EIPs completely, allowing EIPs to go back to being focused technical discussions of proposal changes. Right now adding even the mention of backwards state changes causes too much noise for the important changes to be disucssed.

---

**fubuloubu** (2018-03-28):

What are the benefits and deficiencies in the current process of “hard-forks-as-a-signal” for adoption of a change to state?

I mean, in my head (not sure how feasible this would be) Parity wallet users could band together and suggest a change to state to move the funds and/or restore the library code so they can access them again. Obviously this proved impractical (that’s why it wasn’t done) but it is possible and serves as a thought experiment of how the current process works.

Is it sufficient?

---

**MicahZoltu** (2018-03-29):

I’m against changes to the process.  As it stands currently, client developers can propose a change by releasing a new client.  Economic participants can then either choose to go along with that change or not.  Essentially what this leads to is users delegating decision making power to client developers they trust to make decisions on their behalf as to how the protocol will progress. If the client developers do something that drives users away, then those users will find other client developers to follow.

---

**MicahZoltu** (2018-03-30):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/c/919ad9/48.png) CryptoHokie:

> What about in the case of two client implementations disagreeing on a proposal. Is the default position to simply have them fork if they don’t agree, and see if they get hashpower / staking support?

A fork in that case is “working as intended”.  Hash/staking power is irrelevant, what matters is which chain economic participants choose.  This means which chain do businesses accept in exchange for services.

---

**lrettig** (2018-03-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png) jpitts:

> Such a decision process involving state modification may not only be technical in nature, but involve ethics, philosophy, and law.

I agree that this sort of decision is at least as political (/ethical/philosophical/legal) in nature as it is political. This is a good candidate to fall under the remit of the “Ethereum Philosophers” initiative.

---

**phiferd** (2018-04-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png) jpitts:

> Such a decision process involving state modification may not only be technical in nature, but involve ethics, philosophy, and law.

True, but to be clear, protocol changes will not necessarily be free from discussions of ethics, philosophy, and law.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> client developers can propose a change by releasing a new client

Clients certainly do have the ability to release a new version that makes some state changes, but I don’t see any reason why all such changes will split along client lines or why client teams will necessarily be interested in only supporting one side of the fork or the other. As with the DAO, clients may want to delegate the decision to their users.

Also, if multiple clients want to support the same changes, then they will need a way to decide what changes should be made, when they should be applied, and what options should be presented to the user. If they don’t agree on this, we’ll end up with one fork per client.

The process for doing this could be outside of the EIP process (and maybe it should be), but there will probably need to be *some* process (submission, evaluation, feedback, voting, etc) that has a number of similarities with the EIP process and shares many of the same stakeholders.

---

**fubuloubu** (2018-04-09):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/phiferd/48/106_2.png) phiferd:

> but there will probably need to be some process (submission, evaluation, feedback, voting, etc) that has a number of similarities with the EIP process

I disagree here. I think there is already a process in place (as evidenced by the DAO hack), and that process is already fairly robust and comprehensive through miner and user signaling on hard fork events. This allows economic signaling of support versus a purely governance-based mechanism, which I think is more robust overall.

Perhaps identifying what the current process is and discussing it’s shortcomings is a better path forward than another governance mechanism like EIP.

