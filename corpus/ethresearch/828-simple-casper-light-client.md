---
source: ethresearch
topic_id: 828
title: Simple Casper light client
author: vbuterin
date: "2018-01-20"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/simple-casper-light-client/828
views: 4596
likes: 3
posts_count: 3
---

# Simple Casper light client

Here is a scheme that allows light clients for Casper with very fast syncing properties without having to even bother implementing the Casper FFG consensus logic; it uses cryptoeconomics.

Validators have the ability to sign messages, of the form `[epoch, checkpoint_hash, validator_index, sig]`. An additional slashing condition is added where a message of this form that does not have the correct checkpoint hash for the epoch it specifies means that the validator that signed it can be slashed.

A client that was online at some previous point, less than the withdrawal period in the past, and which has C as its latest known authenticated finalized checkpoint, can use Merkle proofs to download the validator set active at C, then send the network a message asking for checkpoint messages from those validators for the most recent checkpoint they are willing to attest to. If some checkpoint gets more than some threshold (eg. 10% of validators) attesting to it, then the validator accepts that as its new authenticated checkpoint. The client rebroadcasts these messages to make sure that if they are incorrect, the validator that creates these messages gets slashed.

This allows light client resyncing that’s not only not slower, but actually much *faster*, than proof of work.

## Replies

**nate** (2018-01-22):

Super cool! Seems to use both flavors of economic finality at once to get the best of both worlds ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

It seems as though adding this wouldn’t change the incentive design much, if at all. If validators are only making commitments on epochs that they have already helped finalized (and would be slashed for trying to revert), it seems like we don’t really have to incentivize them that much to make these commitments.

Is it as easy as periodically requiring validators, when they vote, to include this commitment to the most recent finalized epoch that they would get slashed for trying to revert?

---

**vbuterin** (2018-01-22):

We don’t need to incentivize or require validators to do anything necessarily; we could first see if this could be done entirely with channel payments. Though we can certainly weave it into votes.

