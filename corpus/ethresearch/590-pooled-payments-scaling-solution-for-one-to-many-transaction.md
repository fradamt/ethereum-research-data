---
source: ethresearch
topic_id: 590
title: Pooled Payments (scaling solution for one-to-many transactions)
author: ptrwtts
date: "2018-01-11"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/pooled-payments-scaling-solution-for-one-to-many-transactions/590
views: 7310
likes: 10
posts_count: 11
---

# Pooled Payments (scaling solution for one-to-many transactions)

### Goal

Trustlessly pay tokens to a large set of users, while keeping fees / network congestion low

### Solution

Compress the payments into a single transaction, using merkle trees and off-chain data.

- Deposit the total token amount into a smart contract, along with a merkle tree root of the amounts allocated to each user
- Publish the full details of individual allowances off-chain
- Recipients can claim their allowance by submitting a merkle proof using off chain data

In essence, it acts like a one-to-many payment channel. Instead of opening a channel with every individual user, they can open a single channel (a “pool”), and pay many people at once.

### Recurring Transactions

Although useful for one-off mass payments (e.g. an airdrop), the more interesting use-case is recurring payments to a group of users (dividends, royalties, etc). In order to support micro payments, you want a single user to be able to receive many payments over time, and then withdraw all of their funds in a single transaction.

To do this, the payer can update a previously created pool by depositing more tokens and submitting a new merkle tree root with the cumulative allowances of all users. When a user wants to withdraw, the contract will allow them to withdraw up to the amount allocated in their merkle proof, minus any they have already withdrawn. The user can use any valid merkle tree root (the older ones will just entitle them to a smaller allowance).

### Features

- Payments are in ERC-20 tokens
- Each recipient can receive payments in unique amounts
- Cost is fixed, regardless of the number of recipients
- Payments cannot be taken back once settled
- Once a payment has settled, withdrawals are instant
- Recipients can withdraw multiple payments at once
- Recipients can withdraw any amount (does not need to be the full balance)
- When withdrawing, recipients can choose to send tokens to a different address. This way, the pool acts as a very basic on-chain wallet

### Rules

- Each recipient’s allowance can only ever increase
- A recipient cannot withdraw more than their allowance
- Always enough tokens in the contract for everyone to withdraw their full allowance. New deposits could be verified using a merkle sum tree, which was proposed a way to ensure that Bitcoin exchanges weren’t running fractional reserves.

### Attack Vectors

The ability to update a pool introduces some risk that needs to be mitigated. Normally, each user’s allowance should only ever increase. However, an attacker may try to submit a new merkle tree that increases their allowance, while reducing the allowances of others. To avoid this, pool updates could be subject to a challenge period (e.g. 1 day), to protect against the following scenarios:

**Invalid Data**

If an attacker tries to reduce an allowance, you can submit two merkle proofs (old and new) showing that an allowance went down.

**Data Withholding**

More likely, the attacker won’t even publish details of the pool update off-chain, making it impossible to prove that allowances were reduced. In this case, the recipients need a way to mass exit or prevent the update from being accepted. Two possible solutions:

*Exit Voting*

When data is withheld, recipients who are paying attention will want to withdraw their tokens before the update is accepted. When doing so, they could set a flag, indicating that they are exiting due to a problem. If X% of recipients or allowances raise the flag, the pool is frozen, giving everyone time to withdraw. This way, not everyone has to be online.

*Challenge*

Alternatively, a challenger could post a bond, attesting that data was withheld. The pool owner would be required to submit the full set of merkle proofs, or else the pool would be frozen. If they successfully did so, they would receive the bond, and the update would be considered valid. One potential issue is that a challenger never knows if valid or invalid data is being withheld, so they may be unwilling to take the risk of posting a bond.

### Outstanding Questions

- Any other attack vectors that are unaccounted for?
- Any better ways to prove that a balance has been reduced when data is being withheld?
- What should the protocol for off-chain data publishing be? JSON? REST API? Separate blockchain?
- Is there a simpler solution to achieve the same goal?

### Alternative Solutions

This system is being explored as a solution for [PROPS](https://propsproject.com/static/PROPS%20Whitepaper.pdf), where a large set of users are rewarded in a token on a regular basis, for their contributions in digital media applications.

While a similar result could potentially be achieved with a plasma chain or [relay network](https://blog.gridplus.io/efficiently-bridging-evm-blockchains-8421504e9ced), the aim is to design something simpler (for this specific use-case) that does not require operating a separate blockchain.

*Any suggestions / feedback would be greatly appreciated. Thanks to [Santiago](https://twitter.com/smpalladino) for helping to refine.*

## Replies

**habdelra** (2018-01-30):

Your post inspired me to create a MerkleTree based payment pool. I blogged about it here: https://medium.com/cardstack/scalable-payment-pools-in-solidity-d97e45fc7c5c. Here’s the repo for it: https://github.com/cardstack/merkle-tree-payment-pool

---

**federicobond** (2018-01-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/ptrwtts/48/408_2.png) ptrwtts:

> Alternatively, a challenger could post a bond, attesting that data was withheld. The pool owner would be required to submit the full set of merkle proofs, or else the pool would be frozen. If they successfully did so, they would receive the bond, and the update would be considered valid.

If the merkle tree is sufficiently big, the pool owner may not even be able to do so. I don’t see the attack vector though, if you can always exit with an older merkle root.

---

**denett** (2018-01-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/federicobond/48/473_2.png) federicobond:

> I don’t see the attack vector though, if you can always exit with an older merkle root.

The owner can insert a merkle tree root that gives all allowances to him and immediately withdraw all funds from the contract.

---

**ptrwtts** (2018-01-30):

Yeah, that’s the issue.

If there’s a challenge period before a new merkle root is settled, then users can use an old merkle root to get their money out before it kicks in. However, I’m not a fan of solutions that require users to be paying attention and exit when things go wrong (e.g. Minimum Viable Plasma). It’s unrealistic, and limits the use-cases and types of participants.

That’s why I’m leaning towards adding a mechanism where a certain threshold of participants can “freeze” the pool when they suspect that a malicious merkle root was posted, and data is being withheld (exit voting).

I agree that forcing the owner to post the full tree is probably not viable, especially if it’s large, but wanted to list it as another potential solution to discuss.

---

**habdelra** (2018-01-31):

another idea is to require that submitters of the merkle root have a “stake” posted in the payment pool, such that you can only submit a merkle root if you have a high enough number of tokens staked in the payment pool (probably in a different ledger that doesn’t include the actual tokens being distributed as part of the pool). If malfeasance is discovered after the fact, the submitter’s stake could be lost, and perhaps distributed in the next cycle of the payment pool to the participants of the pool.

Then I guess you then have to think thru what is the process by which participants of the pool can claim that malfeasance has occurred (maybe some kind of voting process)…

---

**ptrwtts** (2018-01-31):

The biggest problem I see is that if an attacker is going to post an invalid merkle root, they’re unlikely to publish the proofs off-chain, making it impossible to discover and prove the malfeasance. The best you can do is make a claim that data is being withheld. But malicious users could also make false claims, which is why it’s risky to have a bond up for grabs, tempting them to try and win it. If instead you could only vote to freeze the pool, then the worst you could do is inconvenience the pool participants, (hopefully) making it less likely to be abused.

Data availability challenges are discussed in more depth here: https://github.com/ethereum/research/wiki/A-note-on-data-availability-and-erasure-coding

I feel like there’s better solution in there somewhere, but can’t quite put my finger on it.

---

**habdelra** (2018-01-31):

At cardstack we are actually working thru an approach to deal with “analytics mining”, where there are parties that contribute their GPU cycles to analyze log files to determine payment pool disbursements in return for a “mining reward”. The idea is that we are building a consensus protocol for “analytic miners” (the merkle root submitters in this instance) to arrive at an solution for the payout that has consensus amongst the pool. We’re still hashing out the details, but I think it actually gets to the heart of your concern. I’ll definitely keep this thread up to date with what we are working on.

---

**MaxC** (2018-02-15):

Here’s a post on another kind of availability proofs  [Proof of Visibility for Data Availability](https://ethresear.ch/t/proof-of-visibility-for-data-availability/1073/3)

---

**ptrwtts** (2018-02-15):

Thanks.

Part of the goal with this protocol is to inherit security entirely from the main Ethereum chain. As soon as you get into the territory of having validators and a consensus mechanism, you’re adding a lot complexity, and might as well have a fully functional bridged chain. The hope is that by limiting the scope (just one-to-many payments), it will be possible to avoid a secondary consensus mechanism completely. But perhaps that’s wishful thinking.

---

**bogdan** (2018-05-06):

Just [posted on efficient rewards distribution](https://ethresear.ch/t/efficient-onchain-reward-distribution-pooled-payments-dividends/1924) using an algorithm that works in O(1) time with O(N) storage, that’s also useful for recurring pooled payments.

