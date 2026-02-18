---
source: magicians
topic_id: 3974
title: "EIP-2502: µTopic Delegation"
author: 3esmit
date: "2020-02-03"
category: EIPs
tags: [governance, democracy]
url: https://ethereum-magicians.org/t/eip-2502-topic-delegation/3974
views: 965
likes: 1
posts_count: 17
---

# EIP-2502: µTopic Delegation

Hey, I would like to invite people interested in Liquid Democracy to EIP-2502, which goal is to solve Liquid Democracy by implementing a common but specializable Trust Network.

The document can be previewed here https://gitlab.com/status-im/docs/EIPs/blob/eip-2502/EIPS/eip-2502.md

I want that users be able to set only once their delegate for all democracies (e.g. cold wallet to hot wallet) and in the specific democracies have their specific delegates for very specific tasks (if needed).

I also want to allow developers to become the “default delegate” for their specific democracies, in order to allow early development to happen without bothering token holders, but meanwhile keeping the veto capabilities of token holders, therefore keeping an equilibrium in trust required.

This EIP dont defines the democracy/governance/proposal schemes, but it guides on how these pieces should relate with µTopic Delegation.

## Replies

**Ethernian** (2020-02-03):

[@3esmit](/u/3esmit),

could you please give more details on topic evolution?

How can they merged, spited, identified as duplicate and so on.

Thanks!

---

**3esmit** (2020-02-03):

Hi! Thanks for the question.

The topics are unique by their address. The only identified topic is the root topic.

If you want to run a democracy and want to inherit from the Trust Network, you create your own Micro Topic and set the root topic (or a children of it) as parent.

Topics cannot be merged, splited, and duplicates are meaningless, or this dont apply here.

The democracy contract, or the proposal executor contract is who will define what topic should be used, so if the democracy contract wants to support multiple topics, it must have its mapping to the topic and the ACL for that topic.

---

**Ethernian** (2020-02-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/3esmit/48/2255_2.png) 3esmit:

> Topics cannot be merged, splited, and duplicates are meaningless, or this dont apply here.

Yeah… I see the problem here.

It is not how real-world discussions evolves. Topics get started in different communities, independently from each other, under different Ids and with different subjects and (slightly) different meanings. Then imagine they get discussed and then voted in the combined community: is this a new topic then? If yes: how it gets created? If not: how voting results from two different get combined?

Topic management and its life-cycle is important in the democracy. Just voting is not enough, IMHO.

---

**3esmit** (2020-02-03):

The topics are created when they are needed. For example, if you need a new topic for controlling a specific subject of a DAO, you can create. If thats not needed after a time, its up to the DAO rules to specify the life cycle.

The goal of this EIP is not to define how DAOs or voting works, but how they can use a common trust network, and how this trust network relates to sub topics (the specific topics for a DAO). It relates to voting, but does not define it, only specifies how Influence can flow between accounts using this Trust Network defined in the EIP itself.

For example, a sub topic could even be an upgradable contract, and the subtopic can be controlled by a democracy, which then could vote to change the behavior of voting. The democracy itself can be upgradable.  The democracy would need a subtopic if it spawns a subdemocracy (for controlling a subproject), but all is defined up to the democracy rules.

I am writing a democracy contract, which uses this trust network, but I dont think worth specifing it, as its not a “interoperability” issue, I mean, the democracy and its delegation topics are part of the same project, which will have its own documentation.

There are other parts, like Voting, which can be EIPed, but would be a different EIP, and there is also EIP about it which we can use instead.

---

**3esmit** (2020-02-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> Then imagine they get discussed and then voted in the combined community: is this a new topic then? If yes: how it gets created? If not: how voting results from two different get combined?

The lifecycle, specified in the Proposal/DAO for this would allow multiple delegate paths, so when a delegate claim the influence, it can choose what path it takes.

Other solution would be specifing this as a new delegation, however, this delegation would have multiple inheritance, and its up to the sub topic rules to define how this multiple inheritance is used.

---

**Ethernian** (2020-02-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/3esmit/48/2255_2.png) 3esmit:

> The topics are created when they are needed.

Someone who creates a topic and starts voting needs the attention of others. It is scarce.

How to keep the user attention spent on “right” things and prevent spamming? This is the “topic management” and this is the question that interested me at most.

Delegating of voting power is more a technical question and looks secondary to me.

---

**3esmit** (2020-02-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> Someone who creates a topic and starts voting needs the attention of others.

Yes, but its not covered by this EIP. This is up to the Democracy implentation. There are many ways of solving that. One way would be using something like a block explorer, or something like a message notification.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> How to keep the user attention spent on “right” things and prevent spamming?

This is also again about how the implementation is defined. I dont think a DAO would allow anyone to create a topic and start voting on it, probably to create a new subtopic it would need to be approved by the democracy as a proposal, then it would be included. But of course, is impossible to prevent someone from making a subtopic outside of the democracy, however it wont be recognized by the main democracy, it could be a sub democracy that is not connected to the main democracy, and is a different app.

To prevent spam, is also a rule of the proposal manager, for example, it could request a stake payment of the voting token to send a proposal, which is refunded after approval, or burned if rejected. The stake payment could be optional, and the higher value, the more visibility it have for the community.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> Delegating of voting power is more a technical question and looks secondary to me.

The goal of the EIP is provide a common trust network, this means that you can trust the same address for every DAO.

Thinking better about multiple inheritance, it can be useful for having delegation on topic types, not only on specific topics, and Ill think better on how to implement that.

---

**3esmit** (2020-02-03):

Imagine you have this Setup

1. Cold Wallet: Stores 100 different types of assets, all of them which have liquid democracy through the asset.
2. Hot Wallet: Stores just a bit of ether for gas and tokens for daily use
3. Address (friend) who knows a lot about economy
4. Address (Public person) who have strong reputation on security
5. Address (Family member) who knows a lot about marketing

ColdWallet —delegates—> HotWallet: So user dont have to unlock funds to make changes on delegation or to vote.

Then all DAOs, HotWallet can now define the influence destination of that funds, which for different subtopics, the user will choose a different friend, family member or public person…

The EIP defines how this relationship between topics happen, and suggests how influence normally flows between topics.

Ill research how I can make different sub topics have the same topic, so it can define the same address for all (as e.g.) “security” sub topics, instead of having to make 100 transactions, one for each dao, but still allowing a custom overwrite into specific DAOs subtopics.

Something I wanted to have is partial delegation, but this explodes in complexity due the multihop capabilities.

---

**Ethernian** (2020-02-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/3esmit/48/2255_2.png) 3esmit:

> Address (friend) who knows a lot about economy
> Address (Public person) who have strong reputation on security
> Address (Family member) who knows a lot about marketing
>
>
> ColdWallet —delegates—> HotWallet: So user dont have to unlock funds to make changes on delegation or to vote.

I think, I am still failing to understand the bigger problem you are solving (besides Cold to Hot wallet delegation).

Considering an “*Address (friend) who knows a lot about economy*”. This delegation is subjective and relative to the particular topic. In particular, I am listening to his opinion about my holding. But should someone else trust him to manage his own assets just because he claims to have my trust? Not soo easy, think. Trust is not so easy transitive. The topic change (my wallet vs his wallet) is important too.

We should dive deeper on the level of the basic sense of terms like **trust** and **voting** before we can construct a something new and reliable, Otherwise, we are reinventing “linked-in” or similar rating systems with all their disadvantages.

---

**3esmit** (2020-02-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> I think, I am still failing to understand the bigger problem you are solving (besides Cold to Hot wallet delegation).

Within the topic of **Liquid Democracy** (note that is a type of direct democracy), and Common **Trust Network**, this is what being solved by this EIP.

Dr. Shermin Voshmgir explains in depth the problem im trying to solve in this video https://www.youtube.com/watch?v=u4lnSx4s7sc

See this article about the history of Wikipedia: [Wikipedia:Trust network - Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Trust_network)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> This delegation is subjective and relative to the particular topic. In particular, I am listening to his opinion about my holding. But should someone else trust him to manage his own assets just because he claims to have my trust? Not soo easy, think. Trust is not so easy transitive. The topic change (my wallet vs his wallet) is important too

Thats why I call “influence claim”, funds are not transferred or authorized to anyone.

In the democracy I am implementing, delegating dont mean trusting, you can undelegate at any time, overwrite the vote different than delegate, there is a veto period.

---

**Ethernian** (2020-02-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/3esmit/48/2255_2.png) 3esmit:

> Dr. Shermin Voshmgir explains in depth the problem im trying to solve in this video https://www.youtube.com/watch?v=u4lnSx4s7sc

I beg your pardon, at this moment I can’t afford to spend 55min watching video to find the info you mentioned. Sorry for that.

let me provide here one quotation from [PGP User’s Guide, Volume I: Essential Topics by Philip Zimmermann](https://web.pa.msu.edu/reference/pgpdoc1.html)

(yes I am old… too old ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12) )

> Trust is not necessarily transferable; I have a friend who I trust not to lie. He’s a gullible person who trusts the President not to lie. That doesn’t mean I trust the President not to lie. This is just common sense. If I trust Alice’s signature on a key, and Alice trusts Charlie’s signature on a key, that does not imply that I have to trust Charlie’s signature on a key.

**Liquid Democracy**, as I know it, is assuming the trust is objective and transferable for much more complex topics than just signature management. Here I have my doubts.

Anyway, my doubts are a little bit offtopic here. sorry for that.

---

**3esmit** (2020-02-03):

I truly recommend watching that video, is a very insightful vision on ethereum as a whole, but mostly for what type of governance we need to build.

Also, you don’t have to watch it, just listen, like a podcast, but the presentation is like 25 minutes, the remaining is Q/A, which is also interesting.

What are your doubts? That someone cannot trust other in a very specific topic? If you address the problem clearly I can explain how you can solve it under Liquid Democracy.

I am aware of the weaknesses of Delegation, and under my version of Liquid Democracy (called µTopic Democracy) I am implementing counter measures to assert that Delegation is reversible even after approval.

I didnt wanted to enter in details here because I think is out of scope, but I am happy to discuss it if you willing, as it might be important for the design of this EIP.

First of all, we need to address **Why liquid democracy?**

There are many constraints that cause low vote engagement, such as low understanding of issues, not enough time to take care of decisions, cost associated with voting.

The strongest point is voting complexity, not everyone is aware about everything at everytime. The liquid democracy would solve that by using the influence flow of specializable delegation chains, that builds a trust network.

Delegates with many voting power can more easily reach absolute quorums (50%+1) or even qualified quorums (90%) then many individuals by their own.

**What are the weakness of delegation?**

The weakness that delegation brings is the reintroduction of trust, as you mentioned, trusting is something we don’t like here in blockchain world.

Centralization of power is another problem that is brought by delegation, we can have too few individuals with all power.

Maybe you can contribute to this list aswell? What are your doubts?

**How my version of Liquid Democracy Works?**

µTopic Democracy aims to solve the weakness of trust by requiring a veto period before execution.

The Veto Period uses a different delegation topic (veto delegation) and require a very low quorum to a proposal be vetoed. A veto can only be suggested for something that was previously approved, and takes the same duration of the voting period. However, before approval, during the voting period, anyone that delegated can overwrite the vote and undelegate, because it uses the voting end block to read delegation and token balances.

The centralization of power is aimed to be solved by allowing the micro topics to be very specific, so instead of centralizing the influence, it is redistributed through the delegation chains.

There is need of information tooling to visualize how your influence is being used by the delegates.

µTopic Democracy incentives direct voting by externalizing the gas cost to the proponent, signed votes can be included in a merkle tree, which can be counted in a tabulation period, paid by the proponent (or volunteers). Is possible to also operate on a total offchain tabulation, where you specify an proof-of-stake system (or authority with large stake to determine the voting result), which is calculated offchain, and included by this address, and can be contested by anyone simply by paying the gas cost of tabulation, similar to plasma contract security.

---

**Ethernian** (2020-02-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/3esmit/48/2255_2.png) 3esmit:

> What are your doubts? That someone cannot trust other in a very specific topic?

My problem:

The trust about a very specific topic can’t be delegated or combined with trust of another topic.

The trust about general topic can be delegated, but leads to wrong conclusions, I believe.

It becomes more clear if you take precise examples instead of abstractions.

Example:

1. Alice trusts Bob to manage HER funds. Bob claims to have delegated trust for the topic “managing Alice’s funds”.
2. Peter trusts Queen to manage HIS funds. Queen claims to have delegated trust for the topic “managing Peters’s funds”.
3. Cecile starts voting weighted by trust with Bob and Queen taking part.

How Cecil should compare trust “numbers”? Ignoring the fact topics are different?

Normalizing topics to make them comparable like “managing someone’s funds”?

unclear.

---

**3esmit** (2020-02-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> The trust about a very specific topic can’t be delegated or combined with trust of another topic.

Why it can’t?

I dont think this is useful for delegating trust for managing funds of an individual, but from a public reserve yes, not that is impossible, but its impractical, this is not created to become a trust entitlement over private funds, this is created to gather opinion (as carbon vote) and for governance of DApps.

> How Cecil should compare trust “numbers”? Ignoring the fact topics are different?

This can be easily done by a UI, its a matter of selecting the topic and visualizing your influence and your delegation, or visualizing from anyone (its transparent delegation), its a matter of rendering useful data (information) to user.

From a code perspective, the topics have no relation, or if have, they might have a common ancestor, I don’t see any issue with that, this is the intended design.

---

**Ethernian** (2020-02-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/3esmit/48/2255_2.png) 3esmit:

> this is created to gather opinion (as carbon vote) and for governance of DApps.

from your EIP

> The delegate which gets the influence is the first on the chain that vote, in the example above, if only E voted, it would accumulate the influence of all others and itself, A,B,C,D,E,F,G,I , while if D and G voted, then D would be able to claim influence of A,B,I,C,D , while G would claim from E,F,H,G .

you are talking about **accumulating**, what implies for me an “the Sum of numbers” (over possibly different topics) with unclear semantic for the result.

If you assume, anyone shares the same and unambiguous  topic structure, then I have question: “how it gets maintained”?

---

**3esmit** (2020-02-04):

Maybe we can find a better word than accumulating, but the idea is that on a delegation chain, specially in a circular delegation, any of the participants can vote in behalf of all others (if others didnt voted by themselves).

Mixing topics is not defined on the EIP, yet, but maybe I can find a way of implementing it

As I said, users can know what their influence is being used for in by the delegates, and veto it if wanted. I don’t see the issue.

