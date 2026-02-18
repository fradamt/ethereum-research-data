---
source: magicians
topic_id: 2901
title: Patent Covenant for EIP submissions?
author: boris
date: "2019-03-11"
category: Magicians > Process Improvement
tags: [eip, legal, patent]
url: https://ethereum-magicians.org/t/patent-covenant-for-eip-submissions/2901
views: 1928
likes: 5
posts_count: 10
---

# Patent Covenant for EIP submissions?

In several discussions about the EIP process, a concern has been raised about patent coverage.

Specifically, while the text of the EIP is contributed by the authors under CC0, this does not speak to whether or not they hold patents against it.

Do we need to add patent covenant language to the EIP process? Can we pay for a review and assistance from lawyers to help with this?

---

I have filed this in Github as [#1840](https://github.com/ethereum/EIPs/issues/1840) to track it. Let’s use this thread for long form discussion and research.

## Replies

**boris** (2019-03-11):

This originally came up in [Prague around EIPs & Standards](https://ethereum-magicians.org/t/breakout-session-3-eips-interoperability/1751) and discussions with the EEA team.

I’m bringing this into a separate thread to help those interested take action on it. Who is interested in leading this process / discussion / research?

---

**ligi** (2019-03-11):

IANAL - but I think this is a good idea. Would be sad if we drag something patented into Ethereum.

---

**Ethernian** (2019-03-12):

There was a great guy, [Florian Glatz](http://blockchain.lawyer) from Berlin in the ethereum community one year ago. May be it will make sense to ask him.

---

**ligi** (2019-03-12):

[@Ethernian](/u/ethernian) great idea - I know him and will reach out. Also dropped the person responsible for legal stuff in the EF a note.

---

**boris** (2019-03-14):

[@ligi](/u/ligi) can you say who this is at the EF? Would be good to know who that point of contact is / how to contact them.

---

**jpitts** (2019-03-14):

X-Linked on /r/ethlaw…

https://www.reddit.com/r/ethlaw/comments/b175wp/do_we_need_to_add_patent_covenant_language_to_the/?

---

**shemnon** (2019-03-15):

Would it be simpler to switch from CC0 for EIPS to another permissive OSS license that has a patent covenant?

---

**boris** (2019-03-15):

All of those are designed for code, not specifications, so that won’t work. That’s why it’s CC0 for the written prose.

Basically we need “like CC0, but includes that the author isn’t knowingly submitting something over which they or their employer have a patent over”.

The IETF likely has a process here. I haven’t looked.

Would be great if someone stepped up to lead this process.

---

**boris** (2019-11-02):

I updated the linked Github Issue to point to [@bobsummerwill](/u/bobsummerwill)’s PR for the ETC improvement process:



      [github.com/ethereumclassic/ECIPs](https://github.com/ethereumclassic/ECIPs/pull/162/files#)














####


      `master` ← `bobsummerwill:ip_protection`




          opened 12:42AM - 02 Nov 19 UTC



          [![](https://avatars.githubusercontent.com/u/3788156?v=4)
            bobsummerwill](https://github.com/bobsummerwill)



          [+109
            -36](https://github.com/ethereumclassic/ECIPs/pull/162/files)







Defined a new IP protection process for ECIPs.
Mandatory use of Apache 2.0 for […](https://github.com/ethereumclassic/ECIPs/pull/162)ECIPs, plus optional use of various copyleft license for the source code.
Mandatory DCOs for contributions with real name requirement.
Option for ECIP editors to override the real name requirement if they feel a contribution is exceptional.












See Brian Behlendorf’s (Linux Foundation, Hyperledger) commentary on this for good commentary:

https://twitter.com/brianbehlendorf/status/1190589921335136256

Note: ETH2 and any other ETH1 sub components – e.g. devp2p, who have no license on the spec repo at all, [see issue](https://github.com/ethereum/devp2p/issues/76) – all need to be aligned around this.

