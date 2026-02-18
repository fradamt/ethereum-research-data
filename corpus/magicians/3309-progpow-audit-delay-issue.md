---
source: magicians
topic_id: 3309
title: ProgPoW Audit Delay Issue
author: souptacular
date: "2019-05-23"
category: EIPs
tags: [progpow]
url: https://ethereum-magicians.org/t/progpow-audit-delay-issue/3309
views: 18507
likes: 189
posts_count: 154
---

# ProgPoW Audit Delay Issue

Hey all! I have an important topic for discussion.

We ran into issues starting the ProgPoW audit. We had a hardware partner who specialized in ASICs who was going to work with Least Authority to perform the hardware parts of the audit. They are no longer participating in the audit so we are looking for other auditors for the hardware portion. We have some good candidates, but this effectively delays the start of the audit much more than we anticipated. Because of this I am unsure if the audit will be complete before Istanbul. On top of that I am not sure if  anyone has sorted the funding situation in order to build an open source ProgPoW miner.

We have 2 options:

1. Delay ProgPoW until the hardfork after Istanbul.
2. Have ProgPoW as it’s own hardfork to be implemented once the audit is done.

This is not an ideal situation at all, but despite our best efforts it is what we have before us.

This post was also posted in the AllCoreDevs Gitter chat (https://gitter.im/ethereum/AllCoreDevs) for further feedback.

## Replies

**sneg55** (2019-05-23):

Since when open source ProgPoW miner is a requirement for launch ProgPow on mainnet?

---

**fubuloubu** (2019-05-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/souptacular/48/720_2.png) souptacular:

> Have ProgPoW as it’s own hardfork to be implemented once the audit is done.

I think a lot of people on both sides of this issue have discussed having this proposal implemented in it’s own fork to prevent contention from interfering with the long list of proposals for the Istanbul fork.

Obviously that is not ideal, since it involves a lot of coordination outside of a fork window, but I think the next fork is likely to have something related to the Beacon chain finality gadget (unless that is it’s own fork as well). I would prefer having this one proposal be it’s own chain in between scheduled hard forks instead of pushing this to the next one.

Maybe it’s time to leverage [@shemnon](/u/shemnon)’s hard fork schedule proposal…

---

**souptacular** (2019-05-23):

How will the miners mine ProgPoW? I am less in-tune with the mining software community so I may be misunderstanding requirements.

---

**sneg55** (2019-05-23):

How they are doing it right now? Open source miners (i.e. Ethminer) is less than 10% of entire mining software market. https://hiveos.farm/statistics/

Not to mention that all major closed source miners(Claymore, Phoenix, Bminer) already announced upcoming support of progpow.

---

**souptacular** (2019-05-23):

Oh I didn’t realize! Nevermind then as far as the point about mining software goes.

---

**shemnon** (2019-05-23):

A GPU based GPL licensed miner exists for 0.9.2.  It’s not the most optimized miner, but it’s ballpark, enough for a hobbyist.  It shouldn’t take much to upgrade it to 0.9.3 or whatever recommendations come out from the audit.

---

**boris** (2019-05-23):

None of the EIPs are guaranteed for Istanbul yet.

From my POV it means that ProgPoW tried to get as ready as it can be and if it doesn’t make it then it goes into April 2020.

Also, it’s the only one that’s Accepted (pending audit) *and* has implementations for two major clients.

---

**salanki** (2019-05-23):

Has the non-ASIC design part of the audit been started at least?

---

**fubuloubu** (2019-05-23):

And by non-ASIC, we mean client implementation, which is arguable the most important part that everyone is worried about when they asked for the audit. It also happens to be the smallest and not require special hardware expertise to evaluate.

---

**shemnon** (2019-05-24):

There’s also the issue of validating that the cryptography was used properly.  And that is not a client implementation issue.  Going from keccak-1600 to keccak-800 is one example of a non-trivial crypto change that would require a second set of eyes to say “that was done correctly.”

---

**fubuloubu** (2019-05-24):

Yeah, but the auditors have the expertise to audit this. Also, they’re still inspecting the client implementation. If the miner is broken, someone will just fix the miner. They’re wayyyyy incentivized to do so, plus they can do it without having to hard fork unlike us.

The smart closed source miner teams are already ready for this. Miner software is heterogeneous enough in the wild not to be an existential risk, unlike the client software.

---

**esaulpaugh** (2019-05-25):

Seems like ProgPoW should get as much scrutiny as Ethash did, or less, considering that it’s a derivative. Are we going overboard?

---

**Anlan** (2019-05-25):

> They are no longer participating in the audit so we are looking for other auditors for the hardware portion

Would be interesting to explain why the auditors abandoned. I really don’t think professionals abandon a project without any reason.

---

**MadeofTin** (2019-05-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/anlan/48/1434_2.png) Anlan:

> Would be interesting to explain why the auditors abandoned. I really don’t think professionals abandon a project without any reason.

This is really speculative and bordering on conspiracy imo, there are many external factors that can explain this that have nothing to do with progPow. Of course they don’t abandon for no reason, it doesn’t imply the reason had to do something intrinsic to progPow. Internal things in the company are most likely to be the cause.

---

**MadeofTin** (2019-05-25):

I was kind of surprised that a hardware audit was also required. As long as the client implementation is secure won’t the network be secure? Miners are used to making miner software, they will iterate and are also invested in the security of their own software.

---

**Anlan** (2019-05-25):

So why simply not disclose ?

Any reason like :

- They don’t have time
- They don’t understand what to do
- They consider themselves not competent
- They asked for more money
- Whatever …

I’m not speculating but I’m fed up with governance’s lack of clarity

---

**fubuloubu** (2019-05-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/madeoftin/48/1969_2.png) MadeofTin:

> I was kind of surprised that a hardware audit was also required.

The intent of the “hardware audit” was more to assess the claims by the creators of the algorithm that ProgPoW makes more complete use of GPU hardware than Ethash does. There are a lot of technical claims made, which sound reasonable, but I think opponents wanted an independent assessment of them. We arguably don’t need to pay auditors to do this, anyone with the requisite experience can do this sort of assessment. The problem is finding someone with the requisite experience. Most people in our community don’t have the deep hardware design experience to do this, so we have to rely on the claims of overall chip usage by the designers.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/madeoftin/48/1969_2.png) MadeofTin:

> As long as the client implementation is secure won’t the network be secure? Miners are used to making miner software, they will iterate and are also invested in the security of their own software.

Absolutely, from a software perspective this audit will show that the implementation of the algorithm is secure enough for a public deployment. Mining software can be iterated on, and the overall mining software ecosystem will be heterogeneous enough to protect against catastrophic failure. However, assessing the claims made by the algorithm designers I think is more what people wanted to know about, and this audit will only partially provide that without hardware experts.

---

**MadeofTin** (2019-05-25):

Sorry for potentially over reading this. I feel you on lack of transparency. I don’t know where the information disconnect is so hard to know where the the lack of transparency lies.

---

**MadeofTin** (2019-05-25):

Thanks for clarifying. Kind of funny to me that progpow is possibly

1. the most scrutinized mining algorithm in the space. I certainly don’t know of another that will receive audits
2. The furthest EIP, as far as progress, on the list considered for Istanbul

And also the most likely to be kicked from Istanbul

I know there are commitments that have been made, and respect Hudson’s efforts in keeping them. It still makes me chuckle a little bit.

*edit: added a diagram*

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/d/d981c86575f62d7439c02387c29283a088ad8176_2_690x406.png)image941×554 57.3 KB](https://ethereum-magicians.org/uploads/default/d981c86575f62d7439c02387c29283a088ad8176)

---

**gcolvin** (2019-05-25):

I’ve stated (too) often that we accepted progPoW in early January and I have never understood how an audit became an obstacle.   A hardware audit seems particularly pointless, as if someone knew how to beat progPoW in hardware they’d do better to keep their mouth shut and make some money.  I wish we had called this progEthHash–it might have just sailed on through.


*(133 more replies not shown)*
