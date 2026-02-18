---
source: magicians
topic_id: 4255
title: Using "network upgrade" over "hard fork" in the EIPs repo
author: timbeiko
date: "2020-05-04"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/using-network-upgrade-over-hard-fork-in-the-eips-repo/4255
views: 1178
likes: 5
posts_count: 7
---

# Using "network upgrade" over "hard fork" in the EIPs repo

Copied description from the [PR](https://github.com/ethereum/EIPs/pull/2624):

> As agreed to on the last AllCoreDevs call (see stream) and during the EIPIP meetings (notes), I’ve changed the term “hard fork” to “network upgrade” in EIP-1, the eips.ethereum.org index page, the repo README and for the upcoming upgrade, Berlin (cc: @axic).
>
>
> The reasons for this change, as described on the call, were the following:
>
>
> “Hard Fork”, while technically accurate, often is perceived by newcomers to Ethereum as to mean “chain split” (and possibly “free coins”).
> Most previous HFs/upgrades on Ethereum did  not  result in a chain split, and using “network upgrade” does not bring this connotation to new users, so it should be used as a default, with the possibility of chain splits being explicit
> The EF has used “network upgrade” over “hard fork” for the past couple upgrades, see Istanbul, Constantinople.
>
>
> On the last ACD call, it seem like there was agreement by core devs on moving this forward, modulo feedback on the specific wording. This is the place for that feedback
>
>
> Note: this does  not  remove previous instances of the term “hard fork” across the EIP repo/all EIPs. Only in the “guidelines” document and for the upcoming upgrade.

I would love to get broader community feedback here on both whether this is a good or bad idea, and the specific phrasing/implementation. Thanks!

## Replies

**tay** (2020-05-08):

I’m not too concerned about it but I do think there is a potential unintended consequence that we swing the pendulum too far back and less people take the change seriously enough, which could create confusion, certain providers not updating in time, people being surprised, technical people that are more deep in bitcoin thinking it is soft fork, etc etc etc.

The reason it doesnt concern me (too much) is because people are still going to call it a hard fork so whatever.

It’s worth noting that the downsides of “hardfork” are mostly around the connotations associated with that word. The benefit of this typically-negative connotation is every infra provider knows they need to update when theres a fork. And, based on the last fork that was during holidays and caught people off guard, this could exacerbate that,.

---

**edsonayllon** (2020-05-15):

I’m for the change. From my understanding, there has in the past been scams taking advantage of community misunderstanding of what a hard-fork means, where many in different communities associated it with a chain-split and getting new free coins.

---

**timbeiko** (2020-05-16):

Thanks [@tay](/u/tay) [@edsonayllon](/u/edsonayllon)!

This proposal got a fair bit of opposition on Twitter, which I want to document here as well:

- https://twitter.com/VladZamfir/status/1257424998471544833
- https://twitter.com/lex_node/status/1257321471237517312
- https://twitter.com/koeppelmann/status/1257436064345739264
- https://twitter.com/evan_van_ness/status/1257527185482678273
- https://twitter.com/phildaian/status/1257428389377585154
- (lol) https://twitter.com/MartinLundfall/status/1257608852737896452

Frankly, at this point, I’m not convinced it’s a hill worth dying on. Maybe we just keep our awkward status quo where the EIPs documentation uses “hard fork” and the EF uses “network upgrade” ¯_(ツ)_/¯

---

**edsonayllon** (2020-05-17):

I remember when Segwit 2 was almost going to happen, the person I knew who knew cryptocurrency the most at that time, late 2017, told me Bitcoin holders were going to get new Bitcoin from the upgrade. I believe the misunderstanding comes from new currencies from chain splits culturally being called “forks.”

I’m not sure if Twitter is the best place to discuss these kind of things. Different threads can be made up, unknown to other stakeholders. It’s a disorganized place to make decisions.

For the last few network updates, Muir Glacier and Istanbul, most news articles I read used the term network upgrade. So, the concern over misunderstanding in the future may not be so much an issue as long as the EF addresses them as such. So updating it in the EIP repo may not be necessary. We could optionally include both, one in parenthesis. Or just add a sentence in EIP clarifying hard-fork is a network upgrade, and keep hard fork everywhere else.

In terms of the phrase, I like it, but still prefer the term “network update.” There might be a time where a hard-fork may be needed not to bring new features, but to fix something. Fixing something isn’t upgrading it. Like the difficulty bomb hard fork. Nothing was improved, the difficulty bomb was just moved. I understand Zcash uses the term “upgrade,” but I think they were wrong in that for this reason.

Regardless, network upgrade is better for beginner understanding than hard-fork. Those that oppose this kind of change, from my read, are not beginners, and deep enough in understanding to not be confused by the term. Then again, a beginner probably won’t be going through the EIP repo.

---

**timbeiko** (2020-05-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/edsonayllon/48/2578_2.png) edsonayllon:

> Then again, a beginner probably won’t be going through the EIP repo.

Yeah I think this is the gist of it: we can use Network Upgrade in broad-reaching comms (i.e. announcement blog posts) and keep Hard Fork as the technical term.

---

**rumkin** (2020-05-29):

Sounds reasonable. But I would change “network” to “chain” to make it more specific. Network Upgrade is way more abstract than Chain Upgrade.

