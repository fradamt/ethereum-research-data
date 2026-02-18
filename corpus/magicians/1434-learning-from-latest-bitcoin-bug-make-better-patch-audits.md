---
source: magicians
topic_id: 1434
title: Learning from latest Bitcoin Bug. Make better patch audits
author: Ethernian
date: "2018-09-23"
category: Working Groups > Security Ring
tags: []
url: https://ethereum-magicians.org/t/learning-from-latest-bitcoin-bug-make-better-patch-audits/1434
views: 846
likes: 1
posts_count: 1
---

# Learning from latest Bitcoin Bug. Make better patch audits

## Houston, we have a problem

Look at this tweet from Emin Gün Sirer ( @el33th4xor ):

[The Latest Bitcoin Bug Was So Bad, Developers Kept Its Full Details a Secret](https://twitter.com/el33th4xor/status/1043592906857168897)

How concerning is the information on your scale?

I am VERY concerned. And not because of the bug, but because nobody in the world has ever noticed, that the patch did not fit to the bug description. Nobody has noticed, that the patch does MORE than promised. It is an evidence of very low security.

How many more patches do we have, that do not fit to patch description? Were there any backdoors or similar infiltrated with patches and nobody noticed? We just do not know.

What can we do? I would suggest to play a validation game.

## The Auditor Game

The rules are not ideal, but it can be improved.

1. The released patch should be published for public review for a while before build release.
2. The patch MAY have some intentional bugs. They are submitted in hidden bug list.
3. Anybody may file a public statement about irregularities in the patch under review among with hidden statement whether the public statement made is (intentionally) valid or fake.
4. Other people can support or refute the review.
5. Correct answers are rewarded, wrong answers are punished.
6. Hidden bugs (if any) get revealed.
7. If there were any bugs found/revealed, go to (1)

Rules are not optimal and should be improved.

Any thoughts?
