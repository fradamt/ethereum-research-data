---
source: magicians
topic_id: 2480
title: Abort switch for clients in order to withdraw a planned upgrade to mainnet
author: jpitts
date: "2019-01-18"
category: Magicians > Primordial Soup
tags: [governance, forks]
url: https://ethereum-magicians.org/t/abort-switch-for-clients-in-order-to-withdraw-a-planned-upgrade-to-mainnet/2480
views: 1165
likes: 7
posts_count: 10
---

# Abort switch for clients in order to withdraw a planned upgrade to mainnet

This is to discuss the notion of an “abort switch”, which would enable a more ordered withdrawal of a planned network upgrade in installed Ethereum clients should a bug or security vulnerability require that the upgrade be delayed. In the current configuration, clients must issue an update and coordinate a software update with miners and other runners of nodes.

[@AlexeyAkhunov](/u/alexeyakhunov) on Gitter at [08:49](https://gitter.im/ethereum/AllCoreDevs?at=5c420383cb47ec3000640ddc) PST

> Regarding the upgrade switch that @karalabe brought up: I wanted to comment, but did not want to take more time on the call. I think it can be designed in a way that it does not present centralisation vector. I see it as a voting multisig with a very limited power - to skip a network upgrade. Any abuse of this power would be accountable, because we will see who pulled the trigger. Normally, the discussion and emergency call would still happen, and only after that, the key holders will “do their duty”. If someone does it before the agreement call, it is clearly seen. And, of course, the membership of the multisig is regularly reviewed, and inactive participant removed. Also, if the multisig becomes completely compromised, removal of its powers can still be done via hard-fork coordinated in the “usual” way
>
>
> And, of course, it should be opt-in from the clients
>
>
> I think we should not shy away from such mechanism. Informal structures that make these kind of decisions already exist, and we know that. Making them formal actually make the process MORE transparent, not less

## Replies

**ajsutton** (2019-01-18):

A single global abort switch introduces at least the perception of centralisation, even if there are mitigations and accountability around that.  Basically, it looks really bad and will generate a lot of bad PR. That’s not good for the overall health of the Ethereum ecosystem.

A couple of alternatives that have a very similar effect:

1. Each client creates its own abort switch contract, controlled by the developers of that client. This is much closer to the current level of control where the milestone blocks are put into the client by the client developers and users go with them. It’s basically just an automatic upgrade mechanism for the client’s network config.
2. Just implement automatic upgrade in clients. This could be for the whole client or specifically for the chain config. The main issue here is that security conscious deployments (like crypto-currency nodes) generally don’t like automatically deploying code from the internet.  Limiting the upgrade to just chain config would make that simpler without needing the complexity of querying smart contracts (it would not be able to add new milestones since they’d require additional code to support it, but it could change when implemented milestones took effect).

In either case you’d want to allow users to choose whether they use it.

---

**jpitts** (2019-01-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ajsutton/48/1102_2.png) ajsutton:

> Each client creates its own abort switch contract, controlled by the developers of that client.

This actually may go a long way toward mitigating perceptions of centralization.

As [@AlexeyAkhunov](/u/alexeyakhunov) has mentoned recently, I am not sure that perception of centralization (or what I would call a governing committee) is important, because the governing committee already exists in the form of the self-organized group of core devs. **The governance (in the sense of cybernetics) of network upgrades is simply not very well engineered right now.**

If the contract must be a single one for all participating clients, formalization of a release window for network upgrades w/ an abort switch does not even have to be as “centralized” as it currently is. Other stakeholders can be given keys to the process.

---

As a separate matter: a key design consideration is what I would call OpsEx. Operator Experience, which means that whatever is implemented has to achieve the goals within the context of those miners, exchanges, and others operating these nodes.

Some potential features of a release window switch contract:

- A multisig is maintained, not a new one for each release. Network upgrades are designated by a code, the first number / “MAJOR” in semantic versioning.
- Votes on the multisig are given to stakeholder groups as opposed to individuals, perhaps the core devs and miners are given more weight. They are called keyholders.
- The block number for the next upgrade, window length, etc. is proposed and voted on in the multisig contract.
- At any time within the window, keyholders assert that the next upgrade should be aborted. Enough votes, and the current window is aborted.
- A client can configure to ignore this release window contract.

---

**esaulpaugh** (2019-01-19):

Do you think an abort switch could hurt the predictability of hardforks or at least the perception of predictability? How do we even measure predictability or the perception of predictability or the value of either?

I’m not sure I see the cost-benefit working in favor of the switch, but I have a risk-tolerant bias and it’s inherently difficult to assess the probability of black swan events (such as a last-second (last-12 hours) vulnerability discovery).

---

**bbin** (2019-01-19):

I agree with [@AlexeyAkhunov](/u/alexeyakhunov) mostly, the centralization aspect of this is overblown and already exists in a sense. The power to abort the upgrade is fairly limited and highly accountable.

I tend to view consensus changes like client developers and other key people proposing an update, and the proposers would be the ones that can withdraw the proposal. Anyone would still be free to propose an update and deploy their own contract if they wish (compare “rouge” forks happening today).

---

**lrettig** (2019-01-19):

I support this. I don’t think it changes the existing mechanism at all, it just makes it a bit more explicit and a bit more transparent, and avoids a bit of the [“tyranny of structurelessness”](https://www.jofreeman.com/joreen/tyranny.htm) that exists today. There is already a relatively small group that makes these decisions, and node operators already trust the client developers by choosing to run their code and download their updates. (In the case of parity, there is even already an opt-in auto-upgrade mechanism.)

As long as this is opt-in for node operators I see no issue. Yes, key distribution is challenging but I agree with giving out keys to various trusted groups of stakeholders and I think we can achieve 80% trust with 20% effort, and iterate from there. Again, it should be opt-in so no one is forced to participate if they don’t want to.

If we’re worried about last-second changes we can bake in a minimum threshold of, say, a few hundred blocks, after which the trigger can no longer be thrown.

---

**ajsutton** (2019-01-19):

Reflecting on the ConstantiNOPEle scenario, it turns out that we were able to abort a fork with a little over 24 hours between deciding to abort and the fork block.  If we had a kill switch like this and the vast majority of people opted into it we would have had an extra 24 hours to discover the problem and decide to abort.

So when we think about the trade offs involved here, we need to weigh the engineering effort, perceptions and any security risks against the benefit of an extra 24 hours to make an abort decision and saving 24 hours of cat herding effort that was required.

Looking at it that way, I don’t think the trade offs are worth it.  Though, I do like the idea of clients supporting (opt-in) auto-update since that has a wider range of benefits (e.g. deploying a fix for a client specific bug or security issue).

---

**esaulpaugh** (2019-01-20):

It’s one thing to have node operators each decide whether to set an opt-in flag (like a sort of SegWit User-Activated Soft Fork type deal) and it’s quite another to *distribute keys* to a small minority who will have the ability to hold the network hostage to the status quo. Keys which could be stolen or lost. I just want to make sure we’re not considering such a thing.

Unless we want every client to fork in two, with one team that accepts one of Sauron’s rings of power and one that doesn’t.

---

**ajsutton** (2019-01-21):

> a small minority who will have the ability to hold the network hostage to the status quo

The difficulty bomb effectively rules out the status quo option long term and this doesn’t give power to force a different hard fork, just delay/abort an already installed one. Stolen or lost keys are pretty easy to handle by deploying updated clients pointing at a different contract and the worst case damage is still just that a hard fork is delayed.

So technology-wise it checks out pretty well, but your comment is a very good example of the public perception we’d be constantly battling.

---

**AlexeyAkhunov** (2019-01-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ajsutton/48/1102_2.png) ajsutton:

> So technology-wise it checks out pretty well, but your comment is a very good example of the public perception we’d be constantly battling.

Public perception can be changed via some gentle yet persistent education. Until now, the public perceptions like that are based on somewhat illusory notion that all the decision in Ethereum are made by public “referendum” of some sorts. Which is obviously not true. For the sake of efficiency, some of the limited, revokable powers are with the smaller groups of people. If the Constantinople delay were to be decided in a same way as EIP inclusion into hard-fork is decided, it would never happen on time, and that would be reckless.

Again, I am happy for this improvement (other people do not view it as an improvement, of course) not to be implemented, because hopefully it will not be required very often. ![:hugs:](https://ethereum-magicians.org/images/emoji/twitter/hugs.png?v=12)

