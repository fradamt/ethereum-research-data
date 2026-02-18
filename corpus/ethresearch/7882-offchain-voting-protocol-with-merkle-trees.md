---
source: ethresearch
topic_id: 7882
title: Offchain voting protocol with merkle trees
author: adridadou
date: "2020-08-20"
category: Cryptography
tags: []
url: https://ethresear.ch/t/offchain-voting-protocol-with-merkle-trees/7882
views: 3163
likes: 4
posts_count: 13
---

# Offchain voting protocol with merkle trees

this is a copy of what I wrote here: [offchain voting](https://github.com/openlawteam/moloch/issues/2)

# Why

Onchain governance is always expensive because it involves so many transactions. The goal of this document is to discuss an approach to bring most of the voting mechanisms off chain but still have the same level of verifiability with a few assumptions. The goal here is to describe those assumptions, see if they are reasonable or not and maybe get feedback on how to improve this approach even further.

The properties we are looking for are:

near constant gas cost for a vote round

reasonable cost to create a vote

simple approach

on chain verification / audit possible if something doesn’t seem right

# Design

The goal here is to create two merkle tree:

The vote definition merkle tree. It represents every voting rights

The vote results merkle tree. It represents the result of the vote

The vote definition root is being submitted at the same time as we create the vote onchain.

The vote results are being submitted once the voting has ended.

## VoteRoundId

Each round needs to be uniquely identified. To do this, we use the function: **hash(Moloch address, proposalId)** which is always unique.

## Voting

A Voter should be able to vote as well. To do this, the user needs to signs with his key the following data:

for yes: hash(voteRoundId, 1)

for No: hash(voteRoundId, -1)

for abstain : hash(voteRoundId, 0)

### The vote definition merkle tree

Its structure is as follows:

leaf: voter address, voter weight. The hash representation of the leaf (used for parent nodes) is hash ( voter address, voter weight)

node: standard merkle tree node, i.e. hash of its children

Each leaf is sorted by the address

### The vote results merkle tree

Its structure is as follows:

#### leaf

it has the entries:

- voteSignature. // the actual vote
- balance (1, 0 , -1 )
The hash being used by the parent node is hash(voteSignature, balance)

#### node

It has the same structure but the function is a bit different

- hashOfChildren
- accumulation (sum of accumulation of its children)

#### root

then the hash of the root is being published with the accumulation result. The accumulation result is the result of the voting

## Happy path

If everyone is happy with the voting result (no fraud has been committed) then the DAO just take the result and acts accordingly.

## Fraud

This is the most important part. We describe here the fraud / attack vector, and how this system can respond to them.

### Wrong data

If someone tries to vote with the wrong data (not signed by the right key, not the right weight etc …) anyone can publish the proof that the leaf was wrong by publishing the incriminating leaf with its path to root, the proof in the vote definition and show that the data doesn’t match.

### unknown address

if someone shouldn’t be able to vote, anyone can publish a proof that the address doesn’t exist in the vote definition tree.

The way to prove that is as follows:

- get an address that should be before and after the missing address
- get all the parents to come with it and prove it’s part of the tree

if. the address is smaller or higher than any other address, just prove that the smaller / highest address in the tree definition is not this address and is higher / smaller than the one that has voted

## Failsafe

if anything goes wrong, we should make it possible to invalidate an offchain voting and switch back to onchain if a quorum of voters mark it as fraudulent. TBD: do we want to just cancel the vote or switch it to on chain ? maybe configurable ?

## Staking

It seems to me that using some form of staking to reward the participants and also having a way to punish bad behaviour makes sense but the details of this part is still TBD

## Assumptions

In order for this to work, we make a few assumptions:

- The vote definition tree is a sorted Merkle tree and we assume it is the case ( it is possible to add a way to prove fraud here (by showing two nodes that are not in order)
- The vote definition tree is available for anyone to check
- Once the vote happened, the vote result merkle tree is also available to anyone to check

## Smart Contract design

TBD: Let’s start with the high level design and then I can work on the smart contract itself

I know there are still a few things that need to be defined but I wanted to have a sense.

Does this approach make sense?

Am I missing something?

Is there an optimisation that is easy enough to do that I’m not seeing here ?

## Replies

**bonustrack** (2020-09-01):

Hi here! This sound awesome! I’m working on an offchain voting client here: https://snapshot.page I would love to bring onchain settlement. Maybe we can collaborate on this. Feel free to reach me [@adridadou](/u/adridadou)

---

**adridadou** (2020-09-01):

I saw it around! Looks very cool.

Is it correct that snapshot is a pure offchain solution with voting signature to prove the real owner did it.

I guess you (or the team) also have an aggregator tool to validate & count the votes

How does that work?

Would love to discuss it further and def collaboration is key here!

---

**bonustrack** (2020-09-02):

[@adridadou](/u/adridadou) Yes the users can create proposals and votes on Snapshot by signing a message with their wallet. The signed message is then sent to a Snapshot Hub where it get pinned to IPFS. The IPFS hash are also indexed in a redis db in the hub. The results for a proposal are calculated on the user browser by calling an archive node and asking balanceOf at a specific block number. We can you contact me in TG my username is [@bonustrack](/u/bonustrack) or come in Snapshot TG group here https://t.me/snapshotlabs .

---

**sirpy** (2020-11-18):

The problem is how do you trust the two merkle trees? they could appear to be correct, ie pass all the proof checks. but they simply do not reflect the real voting that happened. but some made up scenario that has valid merkle trees

so you need

a process to dispute the validity of those merkle trees

so you could have a bonded oracle that put those merkle trees on chain and anyone can open a dispute by matching the bond, then there’s an onchain vote in case of dispute. and the loser loses his bond.

---

**adridadou** (2020-11-19):

Totally, sorry I never updated this. I have an updated version of that here https://docs.google.com/document/d/1x2lBzsRPjhW_x5NjY16fjirEVBfTFl_tjeaGy-4PLcU/edit?usp=sharing

[@sirpy](/u/sirpy) could you have a look and let me know what you think?

---

**3esmit** (2020-11-30):

I am doing a research on this exact topic.

One of the main problems of inchain governance is the cost of vote, so using this will make voting free.

The way I found out to solve the problem with the conflicts on merkle trees is:

1. PoS for including votes
2. Anyone can include votes, accept duplicates, but ignore them

Anyone have other ideas?

See here my current PoC https://github.com/status-im/topic-democracy/

---

**adridadou** (2020-11-30):

Have you looked at my document above?

I haven’t looked at your code but I don’t see how you validate the merkle root.

You want to make sure that anyone publishing a merkle root is not pushing some bogus information. You also want to make sure that a verification is not O(n) where n is the number of participants.

---

**3esmit** (2020-11-30):

Yes, I seen what you written above.

My approach in this PoC is very simple, anyone can publish anything, even invalid information, but during the tabulation period it can only use valid signatures that are in a valid merkle root published during the voting period.

The influence power is not part of the vote leaf, only the vote itself, and the influence is gathered depending on the token balance or delegations.

---

**adridadou** (2020-12-01):

I will describe what I understand your system do, what issues I see and you can tell me what I got right, wrong and in general what you think.

From my understanding, the idea is to use a merkle tree to get all the votes but then someone needs to process each vote.

My understanding is that you will then have to proof of each leaf to prove that the vote is part of the merkle tree and once you’ve done them all, then you can finalize the vote.

The issue I see here is that you only move the issue, if the goal is to avoid ppl paying for the vote but someone else will, then I would suggest you don’t use a merkle tree but just some signature that ppl share and someone takes them all and push to the smart contract.

Furthermore, the gas cost will be higher because you will have to use the merkle proof to incorporate a vote.

The approach I’m having is to use an optimistic rollup. I.e. I publish the result and you will show other votes ONLY to challenge the result. That means that 99% of the votes will have a constant gas cost instead of a linear by the number of voters. You could argue that the cost will be O(log(n)) because of the merkle proof you need to provide but this is still much better.

Makes sense? Have I missed anything?

---

**3esmit** (2020-12-04):

Yes, it makes sense.

I also plan to solve the issue you described above, so we are not moving the problem to another actor.

The idea I had in mind is a PoS, where anyone could join to participate on the process of tabulation, however instead of using the EVM to process every vote, a cryptoeconomic would ensure the good behavior of nodes.

---

**sirpy** (2020-12-09):

looks goods

the **Result delay attacks** can be solved by considering a new merkle hash only if it changes the  voting    result. if the vote still passes or still does not pass there’s no need to reset the grace period

---

**adridadou** (2020-12-10):

I see that’s a good idea.

I’m trying to see how I can even remove the assumption of data availability but then I don’t see how you can avoid a result delay attack.

