---
source: ethresearch
topic_id: 20859
title: Several implementations only randomnize δ when using Groth16. Does this means sampling only 1 of γ or δ is enough to prevent forgeries?
author: ytrezq
date: "2024-10-29"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/several-implementations-only-randomnize-when-using-groth16-does-this-means-sampling-only-1-of-or-is-enough-to-prevent-forgeries/20859
views: 200
likes: 0
posts_count: 3
---

# Several implementations only randomnize δ when using Groth16. Does this means sampling only 1 of γ or δ is enough to prevent forgeries?

According to page 17 [from groth16](https://eprint.iacr.org/2016/260.pdf),  α ; β ; γ ; δ should be sampled by the trusted setup. [This article describe an attack](https://github.com/RareSkills/zk-book/blob/9289f45462a7fe73b7462cf6c45e5c76af97001d/content/groth16/en/groth16.md?plain=1#L276). But the attack described seems to only work when \gamma, \delta are equal. [Nerveless it also states both values should be sampled and not just 1](https://github.com/RareSkills/zk-book/blob/9289f45462a7fe73b7462cf6c45e5c76af97001d/content/groth16/en/groth16.md?plain=1#L303).

**But I’m seeing several implementation that randomize just δ thus leaving γ to the Generator point**. Does this means in reality that the 2 G_2 points representing public inputs should just have unknown discrete logarithms relation in order to thwart any possible attack ? I fail to see how this could be unsafe.

## Replies

**Mirror** (2024-11-03):

For optimal security in Groth16, both γ and δ should be independently sampled in the trusted setup to avoid any known relationships that could weaken the system. Leaving γ as a fixed generator, while only randomizing δ, can introduce vulnerabilities by creating predictable structures. Independent sampling ensures there’s no exploitable relationship, maintaining the integrity of the zero-knowledge proof.

---

**ytrezq** (2024-11-04):

My problem is having a concrete attack that work based on this. I m in a field where no proofs means secure so without example I can t convince anyone. Zcash itself seems to behave in the way described in this post.

Jens Groth himself told me he wrote about randomnizing both only because it makes proving the security simpler.

