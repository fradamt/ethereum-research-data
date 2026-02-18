---
source: ethresearch
topic_id: 151
title: Latest Casper Basics. Tear it apart
author: virgil
date: "2017-10-17"
category: Proof-of-Stake > Casper Basics
tags: []
url: https://ethresear.ch/t/latest-casper-basics-tear-it-apart/151
views: 18915
likes: 48
posts_count: 71
---

# Latest Casper Basics. Tear it apart

This is after Vitalik’s and mine’s edits.  We are largely happy with it.  This is us showing this to you all before we upload it to [arxiv.org](http://arxiv.org).  We don’t anticipate any notable errors, but **we request that you tear our release candidate to pieces before we upload it elsewhere.**

[casper basics_RC1.pdf](https://ethresear.ch/uploads/default/original/1X/fdbebd67c8a9671efabf4e53d6267789cd91d96c.pdf) (233.2 KB)

## Replies

**Lars** (2017-10-17):

The paper says there is a checkpoint every 100 blocks. Wasn’t this changed to every 50 blocks with the Vote mechanism?

That is, you still need 100 blocks to confirm a checkpoint, but this is now repeated every 50 blocks.

---

**vbuterin** (2017-10-17):

It likely will be 50, though it may well be changed; the purpose of the paper is to describe the general type of protocol and convince you that it works, not to be the authoritative holy source of fine-grained protocol details like numbers. Those may well change after the paper is “published”.

---

**djrtwo** (2017-10-17):

Seems like a typo on page 6:

> To support dynamic validator sets, we redefine a supermajority link as follows. An ordered pair of checkpoints (s, t), where t is in dynasty d, has a supermajority link if both:
> To support dynamic validator sets, we redefine a supermajority link and finalization as follows:

Looks like one is an older version of what you were trying to say and both got left in the paper.

---

**jannikluhn** (2017-10-17):

Something’s wrong with this sentence from section 4.2:

> PoS is because if the validators are split into two subsets, with subset V_A voting on chain A and subset V_B voting on chain B, then on chain A, V_B’s deposits will leak, and vice versa, leading to each set having a supermajority on its chain, allowing two conflicting checkpoints to be finalized without any validators being explicitly slashed (however, every validator will lose a large portion of their deposit on one of the two chains due to leaks.

---

**christianpeel** (2017-10-17):

Here are a few simple formatting and grammar notes that may be helpful.

- Why is the date red?
- It seems like an easy thing to add references to other PoS projects such as Dfinity (say to the slides https://goo.gl/jHscPb), and academic researchers such as Rafael Pass (https://eprint.iacr.org/2016/916.pdf). Such references will engender good will, even if you only refer to them in the  intro.
- In the introduction there was no space before reference brackets  (for example[1]), while later on there was a space after brackets  (for example [1]). This is minor of course, yet it makes it look  professional if you’re consistent.
- In Figure 1(a) I suggest replacing the text “The dashed line represents 100 blocks between the checkpoints.” with  “Each dashed  line represents 100 blocks between checkpoints, which are  represented by rounded rectangles.”
- Four lines up from bottom of page 7: I guess “submittedand” is  not intentional. Maybe “submitted and”?  See also   “communityvalidators” and “removingslashing” in the top paragaraph of  page 8.
- Two paragraphs up from bottom of Page 8 the sentence starting  “PoS is because if the validators…” sounds like it needs fixing.

---

**Taras** (2017-10-18):

Suppose we have a justified checkpoint A. Suppose that A has 2 child checkpoints, let’s call them B1, B2. Each of the child checkpoints received 50% of the votes. At this point, it is not possible for one of the B checkpoints to become justified, without someone losing their deposit, correct? This was a little confusing for me. Suppose that B1 has a child checkpoint C1. I then realized that a validator can vote on A -> C1 (skipping B1). So even though C1 is not a direct child of A, it’s still possible to vote that way (if my understanding is correct). So the B checkpoints can never become justified, but their children could (maybe you could state this explicitly).

I didn’t see this kind of example in any of the diagrams. (All votes seem to go from parent to direct child in all the examples, and never skip a generation).

---

**virgil** (2017-10-18):

100% correct [@Taras](/u/taras).   Not sure what to say about you not seeing any such example in the diagrams.  Figures 1c, 3, and 6 all having the jumping.

---

**virgil** (2017-10-18):

Thank you all with the help.  I’ve updated the paper based on your comments.  Keep them coming!

[CFFG_RC2.pdf](https://ethresear.ch/uploads/default/original/1X/1493a5e9434627fcf6d8ae62783b1f687c88c45c.pdf) (1.1 MB)

---

**chris-remus** (2017-10-18):

Here’s a running list of my comments, as I work through the paper.

Initial comments on Section 2 -

**Section 2 -**

**Comment A - Many Branches for a Tree**

Paragraph 2 ends and paragraph 3 opens with a discussion of a tree having many branches. The statement in paragraph 2 feels a bit open-ended. For example, is having many branches OK, not OK, a temporary or  permanent state?

The statement in paragraph 3 seems to clarify that many branches is undesirable. But the two statements left me a bit conflicted in the understanding. It may be helpful to add a clarifying statement to end paragraph 2.

**Comment B - Supermajority Link Definition**

The introduction of c’ -> c confused me a bit. For example, in Figure 1c are two examples of a c’ -> c supermajority link r -> b1 and r -> b2? It may be helpful to show examples of c’ -> c supermajority links in Figure 1c.

---

**josojo** (2017-10-18):

on page 7:

> Suppose that a large set of slashing violations results in results in two conflicting finalized checkpoints,

results in 2 times…

---

**virgil** (2017-10-18):

> For example, is having many branches OK, not OK, a temporary or permanent state?

Having many branches is unavoidable.  The branches will always be there, but they will eventually be ignored.

I think removing the line:

> Note that for an individual block, there will often be multiple blocks added as new children by this mechanism, so the block tree will have many branches.

at the of paragraph 2 is the way to reduce that confusion.  This leaves the text as:

> In this simple version of Casper, we assume there is a fixed set of validators and a proposal mechanism (e.g., the familiar proof of work proposal mechanism) which produces child blocks of existing blocks, forming an ever-growing \emph{block tree}.  From \cite{nakamoto} the root of the tree is typically called the “genesis block”.
>
>
> Under normal circumstances, we expect that the proposal mechanism will typically propose blocks one after the other in a linked list (i.e., each ``parent’’ block having exactly one “child” block).  But in the case of network latency or deliberate attacks, the proposal mechanism will invariably at least sometimes produce multiple children of the same parent. Casper’s job is to take the block tree and decide upon one canonical chain.

> Comment B - Supermajority Link Definition
> I clarified supermajority links a bit by mentioning Fig 1c, it is now:
> 341256×396 58.1 KB

Does any of that help?

---

**amar** (2017-10-19):

1. I have a question. If I am a validator, what is my incentive to send my vote earlier vs later in a given voting term (not sure how you’d define a voting term but I assume there is some set time period during which validators must submit a vote).
2. Also, have you decided on the exact values of NCP, NPP, etc. Specifically, in this version of Casper, the non-vote penalty. I think one of Vitalik’s blog post defined a protocol utility function in order to create some protocol-optimal solution for defining these constants (griefing factor analysis). Is similar work currently being done behind closed doors (and could we open those doors)?

---

**Lars** (2017-10-19):

The sentence

> the proposal mechanism will invariably at least sometimes produce multiple children of the same parent

Is kind of an oxymoron. Is it “invariably”, or is it “sometimes”? I think the “invariably at least” can be removed.

---

**chris-remus** (2017-10-19):

Yes, the revisions clarify those points to me!

Additional suggestions to the revisions -

**Comment A - Many Branches for a Tree**

“invariably, at least sometimes” comes across to me as conflicting. Is it one or the other?

Maybe change that part of the section to read something like, *“…deliberate attacks, it would not be uncommon or unexpected for the proposal mechanism to produce multiple children of the same parent. Casper’s job is to choose a single child from each parent. This selection decides upon and identifies a single canonical chain for the block tree.”*

**Comment B - Supermajority Link Definition**

Adding the distinct supermajority link references to 1c clarifies my original confusion. *I’d suggest adding r -> b3 as an example for completeness, if that can be a supermajority link.*

*You also may want to define “r” in the figures,* rather than relying on the reader to make the link between it and the earlier definition of root or genesis bock.

I understand the point about skipping checkpoints. I’d suggest changing that section to read something like -

*"Supermajority links can between adjacent checkpoints or skip checkpoints, i.e. it’s pefectly ok for h(b) > h(a) or h(b) > h(a) + 1.*

Now, on to the rest of the document ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**Lars** (2017-10-20):

When the deposit is slashed, I suppose some of it goes as a reward to those that reported the violation.

---

**djrtwo** (2017-10-20):

Yes. “small ‘finders fee’” referenced at bottom of page 3.

---

**virgil** (2017-10-20):

We’ve discussed several places for that slashed money to go.  The safest of these options is simply to burn it. The greater risk/reward option is for slashed funds to go into a DAO that pays out Ethereum dev grants.

---

**Lars** (2017-10-21):

I think burning it instead of putting it into a DAO is better. It is probably not going to happen, anyway.

The only thing that may happen is that a staking node goes offline, leading to slashing because of the censoring penalties. I think this will be very uncommon.

---

**virgil** (2017-10-21):

Well, we expect that more minor penalties will occur, i.e., the penalties in the Casper Economics paper:  I anticipate these weaker penalties will be semi-common.  It’s still unclear to me what to do with the money from these penalties.  I personally would love to have a penalty grants program from them.  I think of it as “using speeding/parking tickets to pay for new roads.”  But if the conflict of interest is too great, then we can just burn it.


      ![image](https://github.githubassets.com/favicons/favicon.svg)
      [GitHub](https://github.com/ethereum/research/tree/master/papers/casper-economics)


    ![image](https://avatars3.githubusercontent.com/u/6250754?s=400&v=4)

###

Contribute to ethereum/research development by creating an account on GitHub.

---

**hwwhww** (2017-10-22):

Amazing work! ![:grinning:](https://ethresear.ch/images/emoji/facebook_messenger/grinning.png?v=12)

Here’s some suggestions IMHO:

1. [1 Introduction, page 1, the 3rd paragraph]

> is based on a thirty year old body of research into BFT consensus algorithms such as PBFT

 →  is based on a thirty-year-old body of research into BFT consensus algorithms such as PBFT
2. [2. The Casper Protocol, page 4, Figure2]

> Violate either of these and you lose your deposit.

 → Validators’ deposit would be slashed if they violate either of these commandments.
3. [3. Enabling Dynamic Validator Sets, page 6, the 6th paragraph]

The description of A checkpoint c is called finalized… is duplicated.
4. [4.1. Long Range Revisions, page 7, the 3rd paragraph]

> Hence, as long as ω ≥ 4δ, it’s guaranteed that malfeasant validators will lose their deposits in all chains that any client accepts.

It would be more clear to define the notation ω first. Maybe it could be described in the above line: “so they reject blocks with timestamp ω > 4δ”? (or maybe I misunderstood…?)
5. Could you clarify the difference between ω ≥ 4δ and ω > 4δ?
6. [4.2. Castastrophic Crashes, page 8, the 5th paragraph]

> malfesant behavior

 → malfeasant behavior


*(50 more replies not shown)*
