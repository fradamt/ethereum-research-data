---
source: ethresearch
topic_id: 13450
title: "Brainstorm: application level solutions for TornadoCash sanction"
author: xinbenlv
date: "2022-08-19"
category: Privacy
tags: []
url: https://ethresear.ch/t/brainstorm-application-level-solutions-for-tornadocash-sanction/13450
views: 2130
likes: 2
posts_count: 5
---

# Brainstorm: application level solutions for TornadoCash sanction

Yesterday in [AllCoreDevs 2022-08-18](https://youtu.be/jJaCaS0WbIw) meeting there were discussions about how should protocol level react in light of the Tornado Cash when there were sanction requirements.

My suggestions is that protocol level to remain **strongly censorship resilient**, but leaving the censorship / auditability and **regulatory options on the application levels**. here are a few options:

1. By registration: EIP-5485 (draft) provides a possibility for a smart contract to  declare their legitimacy lineage. Just like if a company issues a security and want to sell it to public in the US jurisdiction they have to be “register with SEC”. On the other hand, if a DAO want to stay self-sovereign they could deny external source of legitimacy. Then other smart contracts can determine if and how they want to interact with those aforementioned EIP-5485 compliant contracts differently based on their jurisdiction they observed.
2. By auditability similar to ZCash provides: user can generate an auditable readonly key and auditors can use that key to read tx source/dest or writeable key to confiscate fund

Or a combination of them two.

Look forward to hearing other ideas in the room.

## Replies

**MicahZoltu** (2022-08-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/xinbenlv/48/9201_2.png) xinbenlv:

> By auditability similar to ZCash provides: user can generate an auditable readonly key and auditors can use that key to read tx source/dest or writeable key to confiscate fund

Tornado built this and made it easily available to users.  The US government completely ignored it and sanctioned all of Tornado anyway, without giving users any option for exiting in a non-privacy preserving manner.  This shows that attempting to pre-comply won’t help, so I think we should just not bother building any such tooling.

---

**xinbenlv** (2022-08-20):

[@MicahZoltu](/u/micahzoltu) thank you for the feedback. IIUYC, I hear you say TornadoCash built some pre-comply feature.

I love to check source code to learn what you referred to. Unfortunately it seems the source code on github is removed. Where can we find technical description or specs that describes the behavior you refer to? I criticize source code censorship.

That said, my sense is that without something like EIP-5485 and without court /SEC establish their on-chain presence, I am not fully convinced by my limited knowledge that the application-level jurisdiction observation could be achivable. Only ZCash-like individual account auditability might not be suffucient.

Therefore, I think there is still a gap in solution that is worth building. And just to make it clear, it’s not just about compliance to some country. I predict some DAOs or other form of societies may also want to establish their own decentralize soverenty.

The proposal here is to provide a solution for  countries or not countries but groups of people (e.g. the passengers of May Flower or spaceship to the Mars) *the freedom to assert their soverenty and exerscise their jurisdiction* and everyone else’s *freedom of vote by feet to comply or ignore such jurisdiction*, and then the freedom of *everyone* to determine whether to operate with each other, but they can all live in the same chain worldview without a fork/chain censorship.

---

**MicahZoltu** (2022-08-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/xinbenlv/48/9201_2.png) xinbenlv:

> I love to check source code to learn what you referred to. Unfortunately it seems the source code on github is removed. Where can we find technical description or specs that describes the behavior you refer to? I criticize source code censorship.

Source code is replicated here: [GitHub - tornadocash-community/tornado-verified-forks: List of verified forks from tornadocash official repos](https://github.com/tornadocash-community/tornado-verified-forks) Tornado Classic UI is the one you probably want to look at.  Alternatively, you can just view the site on IPFS: ipfs://bafybeicu2anhh7cxbeeakzqjfy3pisok2nakyiemm3jxd66ng35ib6y5ri and click the “Compliance” button at the top of the page.

---

**xinbenlv** (2022-08-20):

That is good to know. Will do. Thank you [@MicahZoltu](/u/micahzoltu)

