---
source: magicians
topic_id: 2494
title: State Rent proposal version 2 (rushed)
author: AlexeyAkhunov
date: "2019-01-21"
category: Working Groups > Ethereum 1.x Ring
tags: [storage-rent]
url: https://ethereum-magicians.org/t/state-rent-proposal-version-2-rushed/2494
views: 3958
likes: 10
posts_count: 6
---

# State Rent proposal version 2 (rushed)

Here is the current state of the second version of the State Rent proposal. It is rushed, and most probably contains some mistakes, and definitely lots of things left unspecified. It is here: https://github.com/ledgerwatch/eth_state/blob/master/State_Rent_2.pdf

Main differences from the version 1 (apart from the organisation of the document, which is now series of “change cards” with dependencies between them):

- Linear Cross-Contract Storage removed, since it is possible to emulate its functionality by contracts using CREATE2 opcode.
- Priority Queue for eviction removed, eviction would be based on “touching”, under the presumption that miners would not be able to censor evictions (if they had motivation to do so).
- Calculation of the correct contract storage size (accounting) introduced before the rent, to avoid some edge cases, where rent could become negative.
- Lock-ups with a fixed price introduced, to prevent or limit dust griefing attacks on pre-existing contracts, and to reduce the need to rewrite most of contracts.
- Possibility to exempt important contracts from storage rent by burning ETH prior or after the introduction of rent
- Temporal replay protection is preferred over the variant with non-zero nonces
- Rent price is assumed to be fixed, floating rent can be introduced in later versions of the proposal

## Replies

**veox** (2019-01-27):

It is the first presentation in [this YouTube video](https://www.youtube.com/watch?v=Nky1BPwap2M).

---

**AlexeyAkhunov** (2019-01-27):

Thank you! I have also committed a new version of the proposal (under the same link), with added illustrations for the lockups

---

**jochem-brouwer** (2019-03-04):

Hey [@AlexeyAkhunov](/u/alexeyakhunov) I have delayed sitting down and reading this proposal thoroughly. State rent excites me because this is the logical next step to make the network sustainable to make sure nodes don’t choke on the gigantic storage size! It’s a really interesting concept to think about.

The PDF file looks to me like some kind of presentation. Is there any other resource for information on your proposal? I am thinking more like some kind of paper or detailed documentation.

---

**Zerim** (2019-03-21):

Thanks for the work on putting this proposal together [@AlexeyAkhunov](/u/alexeyakhunov). I have a couple of related questions:

- The proposal specifies recovery for a contract from a hash stump but doesn’t give much detail on the recovery of an externally owned account. What state is restored?
- If the nonce of an externally owned account is restored (and if it isn’t, then why not?), why is temporal replay protection attached to this proposal (I understand that timestamp based temporal replay protection has other benefits, but specifically asking in the context of this proposal).

---

**AlexeyAkhunov** (2019-03-21):

thank you for the interest in the topic! By the way, there is a 3rd version of the proposal available here: [State Fees (formerly State rent) pre-EIP proposal version 3](https://ethereum-magicians.org/t/state-fees-formerly-state-rent-pre-eip-proposal-version-3/2654)

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/z/e95f7d/48.png) Zerim:

> The proposal specifies recovery for a contract from a hash stump but doesn’t give much detail on the recovery of an externally owned account. What state is restored?

externally owned accounts do not really have a lot of interesting data in their state: nonce and balance (which is 0 by definition at the time of eviction). Whenever someone sends some ETH to such evicted address, it comes back, with a different nonce (this is fixed in the 3rd version to prevent effects on CREATE opcode).

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/z/e95f7d/48.png) Zerim:

> If the nonce of an externally owned account is restored (and if it isn’t, then why not?), why is temporal replay protection attached to this proposal (I understand that timestamp based temporal replay protection has other benefits, but specifically asking in the context of this proposal).

Temporal replay protection is removed from the 3rd version of the proposal, because it opens the way for re-deploying contracts that have been self-destructed.

