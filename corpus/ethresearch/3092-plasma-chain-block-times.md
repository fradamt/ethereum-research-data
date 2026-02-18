---
source: ethresearch
topic_id: 3092
title: Plasma chain block times
author: elie222
date: "2018-08-26"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/plasma-chain-block-times/3092
views: 1454
likes: 1
posts_count: 10
---

# Plasma chain block times

How often are sidechains expected to update the mainchain?

The two factors involved seem to be:

Shorter wait - more txs for the operator to put through on mainnet (more costly).

Longer wait - the longer the recipient has to wait to be certain he has received the funds.

I realise there’s no correct answer to this and likely depends on how many txs are being made on the sidechain per second, as well as fees the operator is charging, but still interested to hear what the plans are for initial plasma operators.

## Replies

**boolafish** (2018-08-26):

I believe shorter wait has more benefit. As all the plasma or sharding work should be enabling blockchain to be used in daily life. As a result, better user experience should be important. And if better UX can bring more users, operators should be able to get more fee to cover the mainnet tx fee (and the tx fee for submit block should not be too high anyway since it’s just submitting the block hash).

---

**MihailoBjelic** (2018-08-26):

That should solely depend on the needs of the business/organization running the specific Plasma chain, and the needs of their users.

One Plasma chain might host a high-frequency trading platform with $100M/hour volume. The platform is probably a very profitable business and they probably want to submit checkpoints very often, e.g. every 30 seconds. The other chain might be a voting chain of some local community. They vote once per month on average, so they would probably want to checkpoint only once per month.

That flexibility is one of the beautiful things about Plasma. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**gakonst** (2018-08-26):

Shorter wait means more block commitments, and larger operating costs on the operator side. For Plasma Cash also this means more costs on the user side for non inclusion proofs

---

**sg** (2018-08-27):

AFAIK for now Tesuji Plasma itself costs 121ETH/day via pessimistic assumption.

update) per week [source](https://github.com/omisego/elixir-omg/blob/73a20499b251bd6587e91fdcc09c6f4d66bf80f7/README.md#L356)

[![08](https://ethresear.ch/uploads/default/optimized/2X/c/c98d965f606bb1a08beb3bb6e5b073f19ebd7a94_2_500x500.png)08761×760 73.7 KB](https://ethresear.ch/uploads/default/c98d965f606bb1a08beb3bb6e5b073f19ebd7a94)

---

**cmccabe** (2018-08-27):

If a platform is submitting checkpoints that often, would they actually benefit from using Plasma?

---

**elie222** (2018-08-27):

If you submit every block of the day I don’t think it gets that pricey.

4 blocks per minute. 240 blocks per hour. 5760 blocks per day. Assuming 2 gwei and 50k gas per block submission that’s, ~$0.03 per tx and costs $200 eth per day, or less than 1 eth per day. Obviously depends on what you pay for gas, but would have to be 200+ gwei for every block submitted to cost 121 eth per day.

---

**elie222** (2018-08-27):

Yes, because each block could contain 1000 txs

---

**elie222** (2018-08-27):

How often will Loom commit blocks initially?

---

**MihailoBjelic** (2018-08-27):

I would say yes, definitely. They give up on a fraction of their profit, but their chain gets the security level of the main chain in return. Users should value that, and the increase in profit should be higher then the cost of checkpointing.

