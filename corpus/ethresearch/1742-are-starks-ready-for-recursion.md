---
source: ethresearch
topic_id: 1742
title: Are STARKs ready for recursion?
author: josephjohnston
date: "2018-04-16"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/are-starks-ready-for-recursion/1742
views: 3383
likes: 4
posts_count: 5
---

# Are STARKs ready for recursion?

STARK proofs, due to their succinctness, seem the only viable candidate for recursive proofs. Recursive proofs, where proofs can be made to verify other proofs, can provide a seemingly optimal scalability solution. Are community members currently developing a blockchain (or Ethereum extension) to implement such a solution? I don’t know of one, and I see no reason to wait, because STARKs are already fully developed. I’m confused why sharding, a tough concept to implement elegantly, is being pursued so vigorously when recursive proofs are already feasible. I don’t even see much discussion on recursive proofs. Are there legitimate concerns regarding recursive proofs, or is the lack of activity due to a lack of sufficient mathematical expertise in the community?

## Replies

**miles2045** (2018-04-21):

Vitalik commented on some of the reasons why recursive STARKs aren’t viable for blockchain scaling in this thread below:


      ![image](https://www.redditstatic.com/desktop2x/img/favicon/android-icon-192x192.png)
      [reddit](https://www.reddit.com/r/ethereum/comments/690y1u/scaling_tezos_in_which_we_do_not_pursue_sharding/)


    ![image](https://external-preview.redd.it/FZ1b87URl1Rp06EjNfWZJEon9fv0fTt0mEiO1SiD7Dw.jpg?auto=webp&s=3b2cfc7722c83f29abaf1c55106deb9f14e62781)

###

12 votes and 8 comments so far on Reddit








However, I am wondering if recursive STARKs can be used for *hashgraph* scaling

---

**josephjohnston** (2018-04-21):

Thanks for the link. Recursive proofs might not immediately solve data availability, but neither do they make the problem any harder to solve. Though it reintroduces need for trust, a partial solution would involve trusting a set of registered nodes with good reputation to correctly report on whether data is available. Any proof that changes the state would first require the signatures of a certain portion of these nodes.

---

**GuthL** (2018-09-21):

If the problem is data availability, could recursive STARK at least be useful to speedup the download of the latest state of the chain for light clients?

---

**vbuterin** (2018-09-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/miles2045/48/701_2.png) miles2045:

> However, I am wondering if recursive STARKs can be used for hashgraph scaling

Recursive STARKs don’t solve data availability in any system. I don’t think hashgraphs over any improvement over more structured forms of DAGs including chains in this regard.

