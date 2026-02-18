---
source: ethresearch
topic_id: 18326
title: Compliant Sanction for Tornado Cash
author: jstinhw
date: "2024-01-14"
category: Privacy
tags: []
url: https://ethresear.ch/t/compliant-sanction-for-tornado-cash/18326
views: 1338
likes: 1
posts_count: 3
---

# Compliant Sanction for Tornado Cash

## I. Problem

Platforms like [Tornado Cash](https://github.com/tornadocash/tornado-core)  on Ethereum have ensured transactional anonymity. However, their lack of sanctions screening mechanisms inadvertently leaves room for financial malpractices such as money laundering.

## II. Solution

Typhoon is a trustless and programmable solution founded on zkSNARK technology, offering:

1. Anonymity: It preserves the anonymity of transactions by obscuring the link between sender and recipient.
2. Sanctions Screening: It includes an integral sanctions screening mechanism to deter transactions from flagged or “suspicious” addresses.

### Protocol Description

[![Typhoon Protocol](https://ethresear.ch/uploads/default/optimized/2X/1/18cd9037d5afd5508d98472719af31a2a73b6cc5_2_690x331.png)Typhoon Protocol7470×3588 401 KB](https://ethresear.ch/uploads/default/18cd9037d5afd5508d98472719af31a2a73b6cc5)

**Deposit**: The user construct a commitment from the user’s address and a secret random number and deposit token into the smart contract with the commitment.

**Withdraw**: Within the secret random number, user can generate a proof to prove not in the blacklist and withdraw the token.

Any feedback is welcome! Here’s [more info](https://hackmd.io/ucwTLu9rQPqA37zRfzEqzg?both) and [repo](https://github.com/jstinhw/typhoon/tree/main?tab=readme-ov-file)

## Replies

**MicahZoltu** (2024-01-14):

I believe this is what https://www.privacypools.com/ is proposing.  As I have expressed to them, I think there are a few problems with it:

1. There is no evidence that governments would accept privacy preserving technological solutions to the problem they say they have (money laundering).  Tornado.cash had an extremely invasive compliance tool that completely doxxes the correlated deposit, but the US government doesn’t accept that.
2. Hackers can move into a privacy pool, then pull out immediately, then put back in and wait a bit, then pull out, then put back in and wait a bit longer, etc.  This means that hackers can effectively dodge any sort of list-adding with just a bit more work (and hackers can build automated tools to do all of this).  The end result is that you need to delay the time between deposit and withdraw by some amount of so the “good guys” can update the blacklist before the hacker can cycle their assets.  This creates a pretty big UX hurdle as your money always has to “bake” before it is usable.
3. A big part of the point of privacy is specifically to combat against unreasonable financial blacklist schemes that governments often impose.  Many people who get put on blacklists are not deserving of such.  The Tornado Cash developers themselves are arguably canonical examples of this, where they are on a financial blacklist just for building open source privacy tools.  Similarly, lockdown protestors in Canada had all of their assets frozen and were functionally “blacklisted”.  Governments have shown that they should not be given the tools to censor people’s money because they have repeatedly abused that power.  It is not clear to me that building tools for dictators is the best way forward.

---

**kiaraza** (2024-01-15):

What are the other application scenarios for this solution besides targeting deposits and withdrawals?

