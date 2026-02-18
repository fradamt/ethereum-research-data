---
source: magicians
topic_id: 1556
title: "EIP-1482: Define a maximum block timestamp drift"
author: maurelian
date: "2018-10-09"
category: EIPs
tags: [yellow-paper, jello-paper, eip-1482]
url: https://ethereum-magicians.org/t/eip-1482-define-a-maximum-block-timestamp-drift/1556
views: 4738
likes: 4
posts_count: 7
---

# EIP-1482: Define a maximum block timestamp drift

[Read the full text here](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1482.md)

## Abstract

Include an explicit definition of the acceptable timestamp drift in the protocol specification.

## Motivation

There is a lack of clarity about how accurate timestamps in the block header must be. The yellow paper describes the timestamp as

> A scalar value equal to the reasonable output of Unix’s time() at this block’s inception

This causes [confusion](https://ethereum.stackexchange.com/questions/5924/how-do-ethereum-mining-nodes-maintain-a-time-consistent-with-the-network/5926#5926) about the safe use of the  `TIMESTAMP`  opcode (solidity’s  `block.timestamp`  or  `now` ) in smart contract development.

Differing interpretations of ‘reasonable’ may create a risk of consenus failures.

## Specification

The yellow paper should define a timestamp as:

> A scalar value equal to the output of Unix’s time() at this block’s inception. For the purpose of block validation, it must be greater than the previous block’s timestamp, and no more than 15 seconds greater than system time.

## Rationale

Both [Geth](https://github.com/ethereum/go-ethereum/blob/4e474c74dc2ac1d26b339c32064d0bac98775e77/consensus/ethash/consensus.go#L45) and [Parity](https://github.com/paritytech/parity-ethereum/blob/73db5dda8c0109bb6bc1392624875078f973be14/ethcore/src/verification/verification.rs#L296-L307) reject blocks with timestamp more than 15 seconds in the future. This establishes a defacto standard, which should be made explicit in the reference specification.

## Replies

**maurelian** (2018-10-12):

I’m going further down the stack with this simple EIP than usual. I’d appreciate any feedback on it.

Am I expected to provide [Test Cases](https://github.com/ethereum/EIPs/blob/6f05b979eb7c242b2b1e60a88f858764dbf8c7ec/EIPS/eip-max-timestamp-drift.md#test-cases) at this stage? To what detail do they need to be specified?

---

**ajsutton** (2018-11-13):

It should be noted that the “no more than 15 seconds in the future” rule does *not* apply to ommers. Need to be careful we don’t imply it does when adding this to the YP.

---

**boris** (2018-11-13):

Word on the street is that the [Jello Paper](https://jellopaper.org/) is going to be the canonical reference going forward. What does it say?

I’ve got a work-in-progress PR to codify in the EIPs README where canonical representations / specifications live, and how this interacts with EIP expectations.

I *think* this EIP is useful AND that it might be more of a matter of a PR against the Jello Paper? Not sure!

---

**pjeeer** (2020-04-01):

All those “15 seconds” should be “15 minutes”, right?

---

**maurelian** (2021-03-26):

No, per the source code it’s seconds:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/maurelian/48/43_2.png) maurelian:

> Both Geth  and Parity  reject blocks with timestamp more than 15 seconds in the future. This establishes a defacto standard, which should be made explicit in the reference specification.

---

**axic** (2022-02-10):

I think this may be a useful as a clarification, and could be applied similarly to some of the other “retroactive” ones, e.g. EIP-2681 and EIP-3607.

I wonder what how this will change after the merge, [@mkalinin](/u/mkalinin)?

