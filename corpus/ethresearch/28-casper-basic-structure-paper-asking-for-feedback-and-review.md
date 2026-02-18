---
source: ethresearch
topic_id: 28
title: Casper Basic Structure paper, asking for feedback and review
author: vbuterin_old
date: "2017-08-19"
category: Proof-of-Stake > Casper Basics
tags: []
url: https://ethresear.ch/t/casper-basic-structure-paper-asking-for-feedback-and-review/28
views: 2432
likes: 4
posts_count: 16
---

# Casper Basic Structure paper, asking for feedback and review

https://github.com/ethereum/research/blob/master/papers/casper/casper_basic_structure.pdf

## Replies

**MicahZoltu** (2017-08-19):

I recommend Google Docs (or similar) for authoring/feedback as it allows people to comment in-line rather than having to do what I’m about to do.  ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

Section 2, paragraph 2 has “An epoch is a period of 100 epcochs”.  I’m assuming this is a typo, but if not please come up with better variable names rather than using the same name to represent two things (1 epoch and 100 epochs).

---

**vbuterin_old** (2017-08-20):

Unfortunately google docs doesn’t do PDFs well: https://docs.google.com/document/d/152epW9cQ2sZ1ZBjCS1L8mwADXiZkMnm-75Xzb-tKDAg/edit?usp=sharing

Would definitely welcome other suggestions. And yes, you are correct about the typo, will fix.

---

**phil** (2017-08-20):

I’d read it as “epoch is a period of 100 blocks”.

---

**BenMahalaD** (2017-08-21):

What are you using to create the pdf? Are you writing it in Latex? If so you can just put the source code into a repo or a doc.

---

**vbuterin_old** (2017-08-21):

Latex: https://github.com/ethereum/research/blob/master/papers/casper/casper_basic_structure.tex

---

**malefizer** (2017-09-15):

Page 5 “During epoch n, validators are expected to send prepare and commit

messages with e = n and h equal to a checkpoint of epoch n”

But checkpoints are defined in the paper as the last block of an epoch, so it seems impossible to prepare and commit the checkpoint hash in advance, or did I miss something?

---

**vbuterin_old** (2017-09-15):

Yes, that was a mistake and should be changed. Should be:

“During epoch n+1, validators are expected to send prepare and commit

messages with e = n and h equal to a checkpoint of epoch n”

---

**malefizer** (2017-09-15):

Next question: Is this argument correct:

When there are holes in the justified checkpoint list because not enough votes for the same hash came together, the specific Epoch is not secured by Casper and it is just secured by PoW?

---

**jgm** (2017-09-15):

Question on figure 1 in section 3: the right-hand side of the diagram shows two conflicting checkpoints, but they are at different block heights.  Given that checkpoints are at a pre-determined block height how would this situation occur?

In section 2 you state:

> During epoch n, validators are expected to send prepare and commit
> messages with e = n and h equal to a checkpoint of epoch n. Prepare
> messages may specify as h* a checkpoint for any previous epoch (preferably
> the preceding checkpoint) of h , and which is justified (see below), and the
> e* is expected to be the epoch of that checkpoint.

This clashes with your definition of h* above in the same section, which specifies h* as

> h* the most recent justified hash

Something that is unclear from the paper is what happens if a checkpoint is not finalised during the following epoch.  I would assume that prepare/commit carries on in to the next epoch, but then that could cause h* to change during an epoch and result in there not being enough prepares to finalise a checkpoint so perhaps I’m wrong with that assumption.

---

**vbuterin_old** (2017-09-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/malefizer/48/38_2.png) malefizer:

> When there are holes in the justified checkpoint list because not enough votes for the same hash came together, the specific Epoch is not secured by Casper and it is just secured by PoW?

Yes, there can be holes in the justified checkpoint list as currently written. However, that specific epoch becomes also secured by Casper later on once a descendant is finalized, as finalizing anything in a hash chain necessarily implies finalizing everything before it.

---

**vbuterin_old** (2017-09-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/jgm/48/25_2.png) jgm:

> I would assume that prepare/commit carries on in to the next epoch

No. If a checkpoint is not finalized during an epoch, the process is abandoned for that checkpoint, and starts again for its child.

---

**malefizer** (2017-09-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> No. If a checkpoint is not finalized during an epoch, the process is abandoned for that checkpoint, and starts again for its child.

So (prepare, commit) are always in the same epoch. 2/3 prepare, 2/3 commit and then it’s fine. Otherwise it restarts for the next epoch. I don’t understand what problem commit does solve then, Can’t we just “justify” with prepare?

---

**vbuterin_old** (2017-09-20):

Read the safety proof in the paper. The safety proof breaks down if commits are removed. There may well be ways to make a prepare for epoch N+1 do double-duty as a commit for epoch N, but this would just shuffle the complexity into a different place.

---

**zlawrence** (2017-09-25):

In section 5.1 (Long Range Attacks) :

1. You assert: If clients hear about two conflicting finalized checkpoints C_1 & C_2 where, from the point of view of all clients, T_2 > T_1, they all choose C_2 over C_1. Why is this true?

---

**virgil** (2017-10-05):

In my old neuroscience research group the way we would do edits of the .tex in Google Docs.  This is what I suggest here.

