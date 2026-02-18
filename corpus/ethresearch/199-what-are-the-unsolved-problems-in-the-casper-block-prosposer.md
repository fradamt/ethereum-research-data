---
source: ethresearch
topic_id: 199
title: What are the unsolved problems in the Casper block prosposer?
author: virgil
date: "2017-11-10"
category: Proof-of-Stake > Block proposer
tags: []
url: https://ethresear.ch/t/what-are-the-unsolved-problems-in-the-casper-block-prosposer/199
views: 1803
likes: 5
posts_count: 6
---

# What are the unsolved problems in the Casper block prosposer?

I am prepping for my MIT/Cornell trip and I’ve been going through these two papers again:

- https://people.csail.mit.edu/nickolai/papers/gilad-algorand-eprint.pdf
- https://arxiv.org/pdf/1406.5694.pdf

My current impression from these papers is that a Casper friendly block proposer (CFBP) doesn’t seem that hard of a problem.  Assuming Casper FFG is 100% working, all we really need is a controlled, rate-limited way to grow the block-tree that is resistant to various attacks and griefing vectors—that doesn’t seem so difficult!

But if this problem was really “not so difficult”, I suspect [@vbuterin](/u/vbuterin) would have already solved it.  And given that he hasn’t, I suspect I am missing something.

Ergo, I ask the team:

1. What are the functions CFBP must serve?
2. What are the engineering properties CFBP must satisfy?

And I will then investigate how well the current state of the art satisfies these.

## Replies

**vbuterin** (2017-11-10):

The one thing that we want and that we actually don’t currently have is that when you have two branches off the same most recent justified checkpoint, you want the one that contains the votes from the most unique depositors to be favored. This way, the proposal mechanism by itself cannot censor without the collusion of 51% of validators.

Otherwise, the CFBP basically just needs to grow a chain, and is it very true that there is a very very wide class of algorithms that could work.

---

**MicahZoltu** (2017-11-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> votes from the most unique depositors

Anytime I hear anyone say “unique ” my hackles raise as solving Sybil attacks is very far from a trivial problem.  I would say the problem is wholely *unsolved* if all you have is “once we solve the Sybil problem we are done”.

---

**vbuterin** (2017-11-10):

By “unique” I mean “unique accounts”. “The branch with the most unique depositors” means “the branch such that the largest portion of total deposited ether supported it”.

When doing economic analysis, it’s generally a bad idea to think of validators as discrete agents. Rather, you want to think of them as something more like an infinitely divisible liquid. This switch in framing removes a lot of misconceptions and bad ideas.

---

**MicahZoltu** (2017-11-10):

Ah, each validator has a fixed deposit size so 51% unique accounts is synonymous with 51% staked ether?

---

**NicLin** (2017-11-11):

what’s preventing us from having the branch supported by the largest portion of total deposited ether being favored? it seems pretty straightforward or am I missing something?![:open_mouth:](https://ethresear.ch/images/emoji/facebook_messenger/open_mouth.png?v=9)

