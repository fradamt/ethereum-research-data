---
source: magicians
topic_id: 2244
title: Guided On-boarding for Potential Contributors
author: jpitts
date: "2018-12-18"
category: Working Groups > Education Ring
tags: [core-devs, education, contributing]
url: https://ethereum-magicians.org/t/guided-on-boarding-for-potential-contributors/2244
views: 1079
likes: 13
posts_count: 6
---

# Guided On-boarding for Potential Contributors

I saw a [post on the AllCoreDevs gitter channel from Mudit Gupta](https://gitter.im/ethereum/AllCoreDevs?at=5c18f5099c82bd024032d6ac) which illustrates a problem in the community. This person was hoping to get up to speed enough to help with go-ethereum contributions, perhaps unrealistically, but earnestly. There is a need for advanced on-boarding, but the core devs don’t have time to do it and expect new contributors to do the work themselves.

Mudit Gupta:

> Some architecture diagrams of go ethereum or perhaps a video of someone going over the architecture will greatly help Imo. Otherwise, it will just take hours and hours for a new programmer to start contributing (which, as everyone can see, not many are willing to do).

Martin Swende:

> Docs about implementation internals have a tendency to rot fast. Docs about structures like patricia trees are great, but for a lot of things, the code will always be the best reference. It will take hours and hours to grasp it all, but we try to flag 'good-first-ticket’s to help on-board new devs. And the geth discord server is better suited for general geth-discussion

Mudit Gupta:

> I am not requesting detailed docs about the implementation. Just a 30 min video walkthrough maybe that says what is where.

And later on this person writes something about contributor motivations:

> I don’t want to just pick issues and solve them, I want to get the feel of the code first. I want to learn new things while doing that. I need to enjoy something if I am going to do it for free. I am just not ready enough to do chores that I don’t enjoy doing without any gains.

Are there any ideas about what can be done here?

## Replies

**jpitts** (2018-12-18):

Thanks [@AlexeyAkhunov](/u/alexeyakhunov) for engaging with Mudit. [@holiman](/u/holiman) too.

Advanced on-boarding is overall a problem in many open source projects; I’ve experienced it myself in civic projects involving much more common/traditional web-based systems.

“Onboarding in Open Source Projects”



      [juergenmuench.com](https://www.juergenmuench.com/publications/uploads/09162b2358b531ccfd186a98461314fd528f3ba1.pdf)



    https://www.juergenmuench.com/publications/uploads/09162b2358b531ccfd186a98461314fd528f3ba1.pdf

###



469.09 KB










> This case study on open source software projects shows that mentoring can have a significant impact on onboarding new members into virtual software development teams.

---

**boris** (2018-12-19):

A commitment to onboarding new contributors. Planning to have the documentation & person power to get them productive. Running the project with active PRs and issue grooming (“community management”) that welcomes outside contributions.

Major Eth Clients have not had a focus on this to date, and haven’t had big company backing either. I’d love to see more on the contributor onboarding side, but current maintainers also have to want this.

---

**holiman** (2018-12-19):

I promise you we want this. The problem is that onboarding new developers is a very time-consuming task. We do spend a lot of time trying to help people out and shepherd people through their PRs, but unless the person is ready to dig in and spend the time that is needed to there’s no way we can do that work for them.

What time is ‘needed’?

In my opinion, a contributor should spend enough time that he/she can ask relevant questions. A question may be ‘If I want to add a new RPC method, where do I define it?’. That’s an on-topic question with sufficient context that we can answer it immediately when it pops up. We have a discord-server for that purpose: https://discord.gg/nthXNEv

A question like ‘Can someone give me a 30 minute explanation about geth architecture?’ is unfortunately not as easy to accommodate.

---

**pet3rpan** (2018-12-20):

I also believe that the people who have the right aptitude and skills fit for such a role aren’t necessarily in the loop. It takes the investment of time to learn and get up to date before one can provide value. Most people who are up to date are mostly engineers and researchers - not necessarily folks skills in community management.

Usually in many companies, this progress happens after the right person with the potential underlying ability + attitude / right fit are hired. With most hiring, it is a bet that they are the one that can do the best job. The problem is that this initial contextual process of getting up to date on research, progress and everything else is expected.

I’d say to tackle issues such as talent and having the right people, we need to invest more in people and less in hard knowledge.

---

**RexShinka** (2018-12-30):

One suggestion is each project having standard documentation.  The SecurEth [guidelines](https://guidelines.secureth.org/) (which I contribute to , so yes a shill) have a top level System Description Doc, an architecture doc and requirements in code.  Yes it is extra work, but if developers used this, especially if everyone made the docs in a similar manner, then among the advantages is easier onboarding.  If you look at the examples we have, the actual amount of extra work is not significant.  We have tried hard to minimize the extra docs.

