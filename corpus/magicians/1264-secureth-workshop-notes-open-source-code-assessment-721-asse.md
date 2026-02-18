---
source: magicians
topic_id: 1264
title: "securETH workshop notes: open source code assessment & 721 Assessment Stamp"
author: ligi
date: "2018-09-06"
category: Working Groups > Security Ring
tags: []
url: https://ethereum-magicians.org/t/secureth-workshop-notes-open-source-code-assessment-721-assessment-stamp/1264
views: 1705
likes: 5
posts_count: 3
---

# securETH workshop notes: open source code assessment & 721 Assessment Stamp

I combine the notes I took for both workshops as there is overlap and I want to keep it DRY:

Workshop: Open-source code assessments

**Problems:**

- Age of audits (e.g. OpenZeppelin’s audit is 1.5 years old)
- Quality of audits (often projects do not actually want a deep audit - they just want to have the “audited” stamp to show to user and investors)
- Hard to differentiate between “good audit” and “bad audit” for users
- Audits are expensive

**Raised Questions:**

- how to raise funds?
- how to reduce costs?
- how to assess the quality of audits?
- what open source projects should be audited (get the spotlight)?

**Ideas/Comments:**

- often it is good to not see it as an audit at all - see it as getting a security engineer on board
- trail of bits: we never put a stamp and say we approved
- funding by letting companies/organisations use it advertisement (like gold/silver sponsors for conferences)
- tax tokens
- split audit targets / audit modules - this especially can address the update/“moving target” problems - modules might less updated than the whole project
- register
- security pot
- insurances as incentive for audits (Insurances can insist on audits and act as a feedback loop for assessing the quality of auditors. If insurances have to pay because a bug was used that was not found by the auditor -> then the auditor can be rated lower)

---

**additions at 721 Assessment Stamps**

- Stamps can be a way to communicate audit report to users.
- First we agreed that 721 is not really fitting for this use case.
- Stamps need some stake behind them. That can be either in the form of staking reputation or staking funds.
- Auditors can build reputation by finding bugs and doing audits.
- This reputation system can also be used to rank auditors
- We need different kind of stamps. There will not be one stamp to rule them all. Examples:

stamps that indicate that software is conform with a standard
- Stamps from automated audits (tools cannot replace auditors but they can supplement them)
- Formalized stamps (certain things where looked at / tested )
- Rejection stamps - if issues where not fixed
- Stamp that verified source code is publicly available (OSStamp)

we need to learn from the past and iterate (see e.g. how the FAA is doing it)
ideally a stamp is objective and independently verifiable
an important challenge is to educate the users
existing/emerging projects in this space (both in this workshop) panvala / solid stamp
alternative we could also build something like a crypto yelp

follow-up email addresses (we filled this out in  the slides that I do not have - can anyone provide this?)

**Action plan:**

- we need to build a on chain registry for audits (map project+commit-hash -> auditor+audit report)
- we need to build a reputation system for auditors
- in interfaces/wallets we need to indicate outcomes of audits and at least warn users about dangerous/buggy contracts (IMHO we should also warn users about contracts where the verified source code is not publicly available)
- we need to automate a lot of auditing (this can help to get the costs down and get more wide spread audits that then are even objective and independently verifiable by just running the tool again)
- we need to create pots where users can put funds towards audits of projects they use (as well as libraries that the projects use)
- we need to create formalized stamps/seals - including logos/organisations that users can easily recognize and build trust in

**On a personal note:**

Final thought for me is building approval stamps is really hard. I think negative stamps will be what I start with in [WallETH](https://walleth.org) - means showing users that bugs where found in a certain contract. Warning them that interacting with this contract is risky and offering them to send funds to the entity that found the bugs because this entity might have saved the user from damage. Also presenting users with negative stamps like “no verified source code available” and “no audit in registry” (the later one perhaps even with a link “do you want to put funds in a pot towards an audit?”)

Thanks to the facilitators of securETH and the participants in the workshops. I think it was a great event - although we could not solve all the problems yet - but I think at least some good seed was planted.

## Replies

**jpitts** (2018-09-07):

Thanks for posting this [@ligi](/u/ligi); I think that many who cannot attend this securETH workshop will find these notes valuable.

---

**Ethernian** (2018-09-08):

Thank you [@ligi](/u/ligi) for great work!

Here are some additions:

> We need different kind of stamps.

Two many stamps can be confusing. I would see only one stamp per independent audit.

Let see it from user’s perspective: the user will know if he can trust the code or not. He needs only the single high level message communicating if the code is OK or not.

Details are only interesting if the code is not OK.

So I would propose to organize all the stamps hierarchically with the single stamp at the top presented to User. If we have only one Stamp per Audit on the top level, we can combine many Stamps from independent auditors, which is usual praxis.

This top-level OK/FAIL should not only combine all partial “stamps” but also checks the completeness of implemented standards at the time of audit. It should also check the list of official claims made by author about the code (and used in his promotions).

This claims are free text Auditing Questions/Assurances, like that:

- [YES/NO] This token has fixed supply
- [YES/NO] This token has no super user
- [YES/NO] This contract has emergency stop mode, which can be deactivated later [YES/NO]

Please note that there is no standards for all possible Audited Claims because they are free text, so it will not be possible to put some stamp as the sign of compliance.

By buying an Audit, the Author presents the list of the Claims he would like to have audited. If an Auditor accept the Claim List, it means he believes it makes some sense and can be meaningful audited.

Everything above is about positive stamps. I need to think more about negative stamps.

