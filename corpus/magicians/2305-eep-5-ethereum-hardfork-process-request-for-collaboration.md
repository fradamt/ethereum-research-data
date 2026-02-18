---
source: magicians
topic_id: 2305
title: "EEP-5: Ethereum Hardfork Process - request for collaboration"
author: 5chdn
date: "2018-12-31"
category: Magicians > Primordial Soup
tags: [ethereum-roadmap, hardfork, roadmap, eep]
url: https://ethereum-magicians.org/t/eep-5-ethereum-hardfork-process-request-for-collaboration/2305
views: 2766
likes: 9
posts_count: 9
---

# EEP-5: Ethereum Hardfork Process - request for collaboration

This is a pre-announcement and request for collaboration. I’m planning to write an EEP to define the Ethereum Network Upgrade Process. EEP-5 here primarily covers Ethereum 1.0 upgrades.

```auto
---
EEP: 5
Title: Ethereum Hardfork Process
Authors: Afri Schoedon
Status:  Draft
Version: 2018-12-31
Discuss:
---
```

### General outline:

- whereas EEP-1 defines distinct consensus updates, this is suggesting a framework for upgrading the Ethereum network
- this suggests moving from ad-hoc hardforking to fixed-schedule
- this defines a process with all required stages of hardforking:

gathering EIPs, deadline to accept them
- proof-of-concept phase, deadline to implement them
- testing phase, fuzzing the new code, deadline to update test suites
- testnet rollout (ropsten, görli, or ad-hoc testnets)
- mainnet rollout

each stage should come with a best possible defined timeline and a set of conditions required to accept or postpone proposals

*WIP: open for comments*, Github: https://github.com/karalabe/eee/issues/5

The ultimate goal is to have a well defined process which all client developer teams can stick to and use as orientation for the short- and mid-term Ethereum roadmap in terms of development milestones.

## Replies

**poemm** (2018-12-31):

Looks great! Similar to the stages for proposed features in WebAssembly, https://github.com/WebAssembly/meetings/blob/master/process/phases.md . They maintain a table to track proposals at various stages, https://webassembly.org/docs/future-features/ .

---

**lrettig** (2018-12-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/5chdn/48/1242_2.png) 5chdn:

> this suggests moving from ad-hoc hardforking to fixed-schedule

Seconded. I think this is a fantastic idea. As Ethereum matures as a technology and as a product, it’s essential that our engineering, governance, and project management processes mature as well, and this is an important step in that direction.

---

**5chdn** (2019-01-02):

I posted a proposal for a fixed schedule on the PM tracker: [Ethereum Core Devs Meeting 52 Agenda · Issue #66 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/66#issuecomment-450840440)

> Now, that Constantinople is finalized, I would propose a rough schedule for a subsequent protocol upgrade (a.k.a. “Istanbul”?):
>
>
> 2019-01-16 (Wed) projected date for mainnet-hardfork (“Constantinople”)
> 2019-05-17 (Fri) hard deadline to accept proposals for “Istanbul”
> 2019-07-19 (Fri) soft deadline for major client implementations
> 2019-08-14 (Wed) projected date for testnet-hardfork (Ropsten, Görli, or ad-hoc testnet)
> 2019-10-16 (Wed) projected date for mainnet-hardfork (“Istanbul”)
>
>
> That breaks down to a fixed 9-months cycle to release protocol upgrades accepted prior to the hard deadline in May to mainnet. All proposals accepted after that date should go into a subsequent hardfork nine months later.

---

**boris** (2019-01-02):

I believe there had been discussion about moving to 6 months (and maybe even reducing to 3 months). What are your thoughts on 6 month hardforks?

---

**peter_bitfly** (2019-01-03):

Moving from an ad-hoc to a fixed hard fork schedule is a good change from my point of view. It will ensure that new client features are adopted much faster than it is the case now (e.g. Parity recently introduced improvements to their block propagation algorithm which should decrease the network uncle rate, but as long as not all miners update their Parity nodes, we won’t see any significant improvement).

A 9 month cycle seems a bit long and might cause lots of changes to be introduced in a single fork. Going for a 3 or 6 month cycle would allow to generally only roll out forks that focus on a few new features which are easier to test & adopt.

---

**jpitts** (2019-01-05):

*(definitely I am ready to be corrected [@5chdn](/u/5chdn) and [@karalabe](/u/karalabe) as I may be off the mark in my comments here!)*

How does this EEP-5 Harkfork Process fit in with the steps described in EEP-1 for Consensus-related forks? And will we leave lesser kinds of releases up to individual client devs, perhaps defining an EEP-10 which they can generally follow?

Probably the key thing that stands out is the coordination of testing and testnet-ing.

- smoke testing
- testnet rehearsal
- testnet rollout
- mainnet rehearsal
- mainnet rollout
- postmortems

Are perhaps the rehearsals not necessary in EEP-5, or is there another flow you would propose for the more general Hardfork Process?

Perhaps there is a sort of inheritance from EEP-5 into EEP-1, in which EEP-1 adds some steps because it involves changes to the consensus protocol?

Also, it might be good to list out the likely changes going into non-hardfork and hardfork releases, w/ tags we can all agree on across repos, then describing which EEE applies.

e.g.  data, p2p, les, json-rpc, rlp-encoding, evm … or evm-opcodes?, consensus

---

**boris** (2019-01-07):

Looks like Afri is heading into updates to co-author [EIP 233: Formal Process of Hard forks](https://eips.ethereum.org/EIPS/eip-233).

---

**axic** (2019-01-21):

EIP-233 discussion thread is here: [EIP-233: Formal process of hard forks](https://ethereum-magicians.org/t/eip-233-formal-process-of-hard-forks/1387)

