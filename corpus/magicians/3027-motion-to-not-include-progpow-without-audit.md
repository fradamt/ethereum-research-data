---
source: magicians
topic_id: 3027
title: Motion to NOT include ProgPow without audit
author: ameensol
date: "2019-03-29"
category: EIPs
tags: [progpow]
url: https://ethereum-magicians.org/t/motion-to-not-include-progpow-without-audit/3027
views: 6984
likes: 101
posts_count: 45
---

# Motion to NOT include ProgPow without audit

I just joined my first core devs call #58 (late bloomer I know), and I was concerned to hear that the core devs seem willing to move forward and include ProgPow, even if the audit doesn’t take place due to a lack of funding.

At the risk of taking an extreme position, this strikes me as insane.

I understand that many people want to *just get this over with*, as [@gcolvin](/u/gcolvin) said on the call. But I don’t think it will *ever* make sense to switch to an **un-audited** hashing algorithm for a $10B+ network.

Also I understand that this is a hypothetical discussion about what we do *if the audit is not funded*, and that imminent funding for the audit would obsolete this conversation, but I believe that if the default is that we don’t implement ProgPow without a clean audit (imo the sane thing), it makes it far more likely that miners would expediently pay for the audit.

I want to add that I still don’t support ProgPow even if the audit comes back clean, but I would much more willing to accept it if it didn’t feel reckless.

Links:

- cat herders explaining why ProgPow audit is important
- gitcoin progpow audit grant fund

## Replies

**econoar** (2019-03-29):

I fully agree and was surprised to hear this was a possibility as well.

GPU miners are the ones set to gain financially from this change, I don’t think it’s unfair to ask them to come up with $50k to prove that it’s safe for the network to implement.

I’m a no right now, **strong** no without an audit and could lean yes if the audit results are clean.

---

**Anlan** (2019-03-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/econoar/48/1641_2.png) econoar:

> GPU miners are the ones set to gain financially from this change, I don’t think it’s unfair to ask them to come up with $50k to prove that it’s safe for the network to implement.

Quite honestly what surprises me is GPU miners should pay for everything. Are miners so annoying parasites ethereum needs to get rif of quickly ? They provide a service. Without them this chain wouldn’t exist.

---

**ameensol** (2019-03-29):

> GPU miners should pay for everything.

I don’t think they should pay for “everything”, but I think they should pay for this. They are getting $650M/y (at current prices), and the ProgPow change directly financially benefits them. Why should anyone else pay for it?

---

**Anlan** (2019-03-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ameensol/48/783_2.png) ameensol:

> They are getting $650M/y (at current prices)

While spending $649.99M/y in power costs. Margins are razor thin if any. Mining reward is not a “gift” or a benevolence. And once again: forking of ASICs won’t increment GPU miner’s revenues. It will redistribute existing ones to a new break-even point.

---

**tvanepps** (2019-03-29):

Here is the main contention [@ameensol](/u/ameensol) surfaces:

A completed audit is a prerequisite for hard fork inclusion. I think this is not only reasonable, but a bare minimum for due diligence! Changing a core component of the protocol should not be taken lightly and would only benefit from an external review.

Setting aside who pays for it, don’t you agree there should be an audit?

---

**timbeiko** (2019-03-29):

One thing I will add is that there has previously been [talk of having higher standards w.r.t. security in all EIPs](https://ethereum-magicians.org/t/eip-mandatory-security-considerations-for-eips/2839). Not auditing ProgPow would go in the opposite direction.

---

**Anlan** (2019-03-29):

Yes. Same thing should have been done with Constantinople. Two delays and a test-net completely messed up.

I agree on the need of an audit: strongly disagree with “miners should pay for it” as this attitude opens a very dangerous path.

---

**lookfirst** (2019-03-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/anlan/48/1434_2.png) Anlan:

> I agree on the need of an audit: strongly disagree with “miners should pay for it”

Agreed!

Why isn’t the EF funding at least some of it too?

---

**salanki** (2019-03-29):

I understand where this argument is coming from. The counter argument would be that a lot of people who have spent a lot of time understanding and implementing this algorithm (like Geth Martin) think that an audit is unnecessary since ProgPoW is an addition to ETHASH and not all that risky.

No one is arguing that proper security analysis shouldn’t be done, the argument is that we might not need an expensive third party to conduct something that the client devs and community can accomplish.

---

**gakonst** (2019-03-29):

You do not replace a so-far battle tested algo with one that has only been deployed in non-adversarial testnets AND has not been audited.

If no third party audit is performed, then it should be delayed until one is.

Note: The auditors must also be vetted for any relationship to manufacturers / developers of ProgPoW itself.

---

**kvanreppelen** (2019-03-29):

Only a few weeks ago, the hard fork was postponed because of a last-minute discovery. In the light of that event, I don’t really see how you can argue against caution (also, the cost of an audit would probable be smaller than the cost of introducing faulty updates to the current netwerk - correct me if I’m wrong). If I recall correctly, many devs were in favor of a delay to do some thorough checking.

Why should this be different?

---

**Anlan** (2019-03-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gakonst/48/50_2.png) gakonst:

> You do not replace a so-far battle tested algo with one that has only been deployed in non-adversarial testnets AND has not been audited.

Two points : first one seems noone cares to take a look technically and try to understand how this is not a “replacement” rather than an “addition” to ethash.

Second one : tests ! That’s what we’re begging since 7 months right now ! An official test-net, and an extensive analysis of crypto strength.

But apparently we need to hire a third party auditor (which exposes the fact the internal ethereum teams have no more crypto experts) which costs should be totally on the shoulders of miners.

And I can easily forsee that if an positive outcome gets out of the audit there will be still yellers asking to account the auditors.

---

**fubuloubu** (2019-03-29):

“We want an audit!”

What’s in the audit? What are the audit goals? What are the inputs to the audit? What work has been done already?

Answer those questions and we can get this party started!

A lot of people tend to think an “audit” is somehow a magical rubber stamp that makes all of their dreams come true. In reality, a badly defined audit does barely anything, and only ensures a worse outcome because people don’t consider the value the audit provided.

---

**lookfirst** (2019-03-29):

After the Cat Herders announcement about Least Authority (we’ve quickly moved on from White Block), I’m still waiting for answers to the questions I asked here back on March 25th:

https://medium.com/@lookfirst/what-is-the-total-amount-necessary-to-fund-the-audit-c2451efbcce5

---

**fubuloubu** (2019-03-29):

I’d also like to note that a part of what the Cat Herders are working on is in defining what the audit actually is, since most people have failed to articulate what they want out of the audit besides “security”

---

**Anlan** (2019-03-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fubuloubu/48/2484_2.png) fubuloubu:

> What’s in the audit? What are the audit goals? What are the inputs to the audit? What work has been done already?

[https://github.com/ethereum-cat-herders/progpow-audit/blob/master/Least%20Authority%20-%20ProgPow%20Algorithm%20Audit%20Proposal%20(v2).pdf](https://github.com/ethereum-cat-herders/progpow-audit/blob/master/Least%20Authority%20-%20ProgPow%20Algorithm%20Audit%20Proposal%20%28v2%29.pdf)

Work done already: NONE ! If funds not enough no one will move a finger.

---

**fubuloubu** (2019-03-29):

The audit goals are extremely broad, and probably led to a very high cost to obtain the audit. Nonetheless, there should be enough of the discussion captured in this forum and elsewhere to construct a majority of this report as it stands right now.

---

**fubuloubu** (2019-03-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/anlan/48/1434_2.png) Anlan:

> Work done already: NONE

Also, I meant in term of the test suite available. Ethereum has a very large and comprehensive test suite, so it shouldn’t be difficult to verify the updates with the client code. The work that would remain would be in verifying the miner code.

---

**Anlan** (2019-03-29):

There are several implementations of that.

MH Swende’s work into geth

Andreas Silva’s work into parity

Pawel Bylica’s work on ethash library (used both in ethminer and aleth)

There was also a fully functional miner supporting both ethash and progpow (with kernels for both CUDA and OpenCL/AMD) by me but I removed the work.

---

**cheeselord1** (2019-03-29):

Fully in support of needing a (well-defined and scoped) audit before moving forward with ProgPoW

And included in that audit we should look into the ASIC-resistance claims of ProgPoW and see if they actually stand up to scrutiny. See recent detailed write-up by Linzhi:

https://medium.com/@Linzhi/eip-1057-progpow-open-chip-design-for-only-1-cost-power-increase-eip-1057-progpow-d106d9baa6eb


*(24 more replies not shown)*
