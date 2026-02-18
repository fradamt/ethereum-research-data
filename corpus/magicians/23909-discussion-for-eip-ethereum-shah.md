---
source: magicians
topic_id: 23909
title: "Discussion for: EIP Ethereum Shah"
author: ameensol
date: "2025-04-28"
category: EIPs > EIPs informational
tags: []
url: https://ethereum-magicians.org/t/discussion-for-eip-ethereum-shah/23909
views: 462
likes: 10
posts_count: 9
---

# Discussion for: EIP Ethereum Shah

Link: [Add EIP: Ethereum Shah by ameensol · Pull Request #9704 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/9704)

## Replies

**spengrah** (2025-04-29):

> The Shah SHOULD be elected by the Ethereum community, using a combination of ETH voting, social signalling, and core dev ratification.

For even the soft power held by this role to be considered legitimate by the core devs and the broader Ethereum community, this selection mechanism needs to be more specific and actionable.  Any debate about the legitimacy of the selection process, at any point, would completely undo any focus and efficiency gains of having this role in the first place.

We can use the EOF scenario to illustrate this. Let’s say we had a Shah and the contention over EOF began. Next, the Shah decides to remove EOF from the next hard fork. If the Shah selection process were not clear, specific, and widely considered legitimate, it would be all too easy for EOF proponents to question the Shah’s legitimacy. This would probably result in a significantly worse debacle than what actually occurred.

I don’t currently have an answer for exactly how to define the selection process, but I am open to collaborating on this.

---

**kdenhartog** (2025-04-30):

This is definitely the root issue. To me, the underlying issue below this is there’s no recognized “ring” for the application layer within the space that the Shah could legitimately represent the interests of.

If we had some semi-official long term WG or ring formed for DApp layer and Wallets (or separate would be ideal, but putting them together is simpler to start) like we’ve got for core devs it would be more clear who they represent. The coordinator for that group seems like that natural fit for this role and if we wanted to centralize it to start rather than vote on it the person hired for [this role](https://x.com/TimBeiko/status/1864661871904870585) seems like the natural fit for this.

Speaking as a wallet dev though, I have no clue who that person actually is though.

---

**wjmelements** (2025-04-30):

Executive authority does help with decisiveness. An individual might be less fickle than group consensus. However there is nobody I would trust with this power. I also don’t think something like the EOF catastrophe would have been prevented; the changing of the Shah can juggle CFI statuses more aggressively than a vbuterin blogpost.

The procedure for changing the Shah is underspecified. I would like to see a minimal initial governance specification with slashing if the Shah doesn’t address proposals.

---

**TimDaub** (2025-04-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> However there is nobody I would trust with this power.

You’re maybe not supposed to. Up to [@ameensol](/u/ameensol) what he actually intended with his proposal. But to me there could also be a Biden-like Shah, who is really just an oracle that people pledge their commitment to absolute power in the face of in-decisiveness. In that case the Shah can even have dementia, it wouldn’t matter as long as there’s rough consensus to follow whatever the oracle mumbles. Tbh I even think that if you instantiate the Ethereum Shah as the most competent, most effective king of decisions then you’re setting yourself up for “removing the king” as soon as they start to make bad decisions in the eyes of some.

Consider what’s worse: The EOF debate for 1y or the dementia-ridden Shah saying: “I sense that EOF=bad” or “MORE EOF, WE NEED MORE EOF”? I actually think the oracle having a preference could lead to higher effectiveness. And I trust that core devs would anyways just do whatever the fuck they want ![:smiley:](https://ethereum-magicians.org/images/emoji/twitter/smiley.png?v=12)

---

**TimDaub** (2025-04-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/spengrah/48/10353_2.png) spengrah:

> question the Shah’s legitimacy

Sorry but isn’t the entire point of a king to not question their legitimacy? (I actually also don’t know, I have very little practical experience in dealing with kings)

---

**TimDaub** (2025-04-30):

Maybe it is also the badly named EIP that plays with the idea of having a ruler for a nation, but I think if you see “Ethereum Shah” and then you draw parallels to nation states then you’re missing the bigger picture. I’d actually caution to fully derange just bc someone said “King” or “Shah” or whatever. I don’t think Ameen wants to suggest that.

Ethereum is akin to a decentralized cloud infrastructure or whatever, and usually these types of companies have CEOs who can make decisions quickly. So I think it’s completely reasonable for Ameen to ask to put a product manager in charge essentially

---

**spengrah** (2025-04-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timdaub/48/5038_2.png) TimDaub:

> Sorry but isn’t the entire point of a king to not question their legitimacy? (I actually also don’t know, I have very little practical experience in dealing with kings)

I mean, “Shah” — to the degree that it connotes “king” or “dictator” — is the wrong label for this role, which to me seems much more like a servant leader that synthesizes perspectives and is empowered by the community to make decisions based on that synthesis.

But since they have [no authority to force execution](https://spengrah.mirror.xyz/f6bZ6cPxJpP-4K_NB7JcjbU0XblJcaf7kVLD75dOYRQ) of the result of their decisions, the only way those decisions are relevant is if the community (including Core Devs, etc) follow them. Which they will only do if they perceive the role and surrounding processes as legitimate.

---

**TimDaub** (2025-05-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/spengrah/48/10353_2.png) spengrah:

> But since they have no authority to force execution of the result of their decisions, the only way those decisions are relevant is if the community (including Core Devs, etc) follow them. Which they will only do if they perceive the role and surrounding processes as legitimate.

I agree but the emphasis has to be that the process to elect the leader for a limited term has to be legitimate. I think to question a legitimately elected leader‘s features after a legitimate sortition would start to break the system. So I‘d caution to eg select the king by competence. IMO the king is supposed to be more a random oracle than a godly and always perfectly informed decision maker

