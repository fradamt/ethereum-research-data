---
source: magicians
topic_id: 2252
title: How should we distribute reputation?
author: kronosapiens
date: "2018-12-19"
category: Working Groups
tags: [reputation-systems, reputation-types]
url: https://ethereum-magicians.org/t/how-should-we-distribute-reputation/2252
views: 1049
likes: 6
posts_count: 4
---

# How should we distribute reputation?

Let’s assume a context with a single reputation score, used for decision-making. Some questions to consider:

- How should reputation be given? In absolute amounts (100 rep), or relative (1% of rep)?
- How should reputation be managed over time? Should it decay? Should it inflate? If so, how?
- How do we determine the amount of reputation awarded at any given time?

## Replies

**auryn** (2018-12-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kronosapiens/48/699_2.png) kronosapiens:

> How should reputation be given? In absolute amounts (100 rep), or relative (1% of rep)?

This is only a meaningful question if you are abitrarily assigning a reputation value to an action, which feels sub-optimal.

If that is the case, then absolute values seems like the better of the two options, as a relative percentage would effectively introduce an inflation rate on reputation that is determined by the rate at which the associated action takes place.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kronosapiens/48/699_2.png) kronosapiens:

> How should reputation be managed over time? Should it decay, and if so how? Should it inflate, and if so how?

I tend to think that including both is the optimal state, as they provide different contexts.

Decay over time helps ensure that one’s reputation is relevant to the current context in time. To steal your own example form the DGOV channel, it probably wouldn’t feel right if someone who earned a ton of reputation 10 years ago, and subsiquently hase been univolved, showed and threw the weight of that old reputation around.

Inflation gives context to the raltive size of one’s past contributions given the current state of the organisation, regardless of when those contribution happened.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kronosapiens/48/699_2.png) kronosapiens:

> How do we determine the amount of reputation awarded at any given time?

I personally like the idea of deriving reputation from a stable coin or stable value to ensure the relative magnitutde of reputation awards remains somewhat consistent over time.

---

**cemfd** (2018-12-19):

Under the provided assumptions regarding the governance module:

> How should reputation be given? In absolute amounts (100 rep), or relative (1% of rep)?

- I’m not sure as to how relevant if the rep accreditation is absolute or relative since as long as the rep is non-transferable it should act as a relative asset with respect to rep voting.

> How should reputation be managed over time? Should it decay, and if so how? Should it inflate, and if so how?

- In almost all DAO use cases, engagement is prioritized. We consider “rep decay” or “rep inflation” in order to reflect that in the form of incentives. In order to have an optimal decision we must consider these factors imo: the rate of onboarding: [since this will determine the decay rate if we use inflation], the avenues of rep generation: [in order to keep a sustainable rep topography there must be sufficient and preferably unbiased channels of rep generation] and the objective/usecase of the DAO: [ how agile must the DAO conduct its decision making processes should dictate the intensity of the use of the drug]. Essentially both are tools which could be employed.

> How should reputation be managed over time? Should it decay, and if so how? Should it inflate, and if so how?

- In the current state of the DAOs, the proposer can request or the manager can appoint a value. But i think as we evolve a DAO Ontology this can evolve into context specific reputation attribution by semantic analysis.

---

**dtedesco1** (2022-04-13):

Where any of these ideas implementated? How do folks feel about the current state of reputation management in the ecosystem?

