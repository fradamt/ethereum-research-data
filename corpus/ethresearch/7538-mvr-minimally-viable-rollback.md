---
source: ethresearch
topic_id: 7538
title: MVR - Minimally Viable Rollback
author: avihu28
date: "2020-06-14"
category: zk-s[nt]arks
tags: [zk-roll-up]
url: https://ethresear.ch/t/mvr-minimally-viable-rollback/7538
views: 3795
likes: 11
posts_count: 9
---

# MVR - Minimally Viable Rollback

By [@bbrandtom](/u/bbrandtom) and myself.

**Introduction**

- ZK-based scaling solutions may opt for off-chain data (Validium is a recently proposed name for these systems)
- Vitalik described an attack on such systems by withholding the data, and a proposed solution. We later described why it is unsatisfactory.
- We describe below a solution for this attack.

**System Layout**

- An off-chain operator batches tx and generates proofs attesting to the integrity of the entire batch.
- The system transitions from state s to s’ iff it provides an on-chain verifier with a valid proof and a commitment to s’
- Data as mentioned above is stored off-chain
- Withdrawals are integral to the proof-based state transitions: the user sends a withdrawal request to the operator, who includes it in a future batch/proof
- The smart contract can freeze the system if it malfunctions:

A user whose withdrawal request isn’t serviced by the Operator raises a flag with the smart contract. The smart contract freezes the system if the Operator does not withdraw the requested funds (as manifest in a proof)
- Anyone who observes the unavailability of the off-chain data, can raise a flag with the smart-contract. This increases the likelihood of detecting such an attack in a timely fashion.

**Recovering from a system freeze**

- Naive approach

The system is reverted back to a recent state for which data is known, as recent as available. Any party can submit a request to become the new Operator. A request includes the id of the recovered state, and a bounty. An alternative Operator is nominated based on the list of proposals sorted by most recent state and sub-sorted by size of bounty.
- Problem: An attacker can withdraw funds, attack the system’s data availability, and once the system reverts to a recent state, their funds (already withdrawn!) in the system are reinstated. Essentially a double-spend attack

The MVR Solution

- The assumption is that we can recover to a state based on a history that took place not more than k batches ago.
- It is important to note that we recover not merely to a recent state of the system, state_recent, but rather to a state_new, which is a solvent state derived from state_recent
- In the normal course of affairs, each withdrawal is accompanied by the set of transactions that led to it in the last k state transitions. In the worst case, this would include all transactions in the last k batches. Assuming t tx/batch, that would mean k*t transactions would be included as public input to the proof that settles such a withdrawal request
- Computing state_new, to which the system recovers: state_new = state_recent + Σ (published transactions later than state_recent)
- This solves the double-spend attack as state_new reflects the withdrawal that took place sometime between state_recent and the present

**Observations**

- Worst case, when activating the MVR protocol, we get the performance of a ZK-Rollup, where all tx data is published on-chain.
- With Fast Withdrawals, the marginal cost of operating a system with MVR is in fact 0. The operator can allow users to withdraw through the Fast Withdrawal mechanism, and replenish its on-chain Cookie Jar only from “aged” accounts, i.e. accounts which haven’t had any activity in the last k batches. For that reason, withdrawals from those accounts, need not be accompanied by any transaction history.

**Open Matters**

- We did not describe how to handle deposits made in the last k batches. This is left as an exercise for the reader.

Tom Brand & Avihu Levy

## Replies

**hkalodner** (2020-06-14):

> Anyone who observes the unavailability of the off-chain data, can raise a flag with the smart-contract. This increases the likelihood of detecting such an attack in a timely fashion.

How do you handle griefing from users claiming that data is unavailable?. Traditionally this is a difficult problem to solve since either party could be lying.

> This solves the double-spend attack as state_new reflects the withdrawal that took place sometime between state_recent and the present

This appears to only solve double spends on withdrawals, but not double spends internal to the system. Unless you withdraw your funds, you don’t seem to have any protection against double spends

---

**bbrandtom** (2020-06-15):

> How do you handle griefing from users claiming that data is unavailable?. Traditionally this is a difficult problem to solve since either party could be lying.

Raising a flag means asking for a withdrawal directly from the contract. The contract will only accept a state transition if it includes the withdrawal of the user. If the operator handles the request, the state can advance. Only if the state does not advance then the system freezes and a rollback is possible.

> This appears to only solve double spends on withdrawals, but not double spends internal to the system. Unless you withdraw your funds, you don’t seem to have any protection against double spends.

You are right, this idea does introduce longer time for finality (k batches instead of 1 in validium/zkrollup without the ability to rollback). We will add it to the original post. Note there are ways to guarantee shorter finality for the users in exchange for greater risk to the operator.

---

**hkalodner** (2020-06-15):

So then there are really two different solutions. The naive solution that you described is a bit of a straw man since the attack would be fixed by just requiring a `k` block delay before transactions are processed.

Comparing those two approaches, with the MVR approach you gain the ability to withdraw in less than `k` blocks, at the cost of significantly increasing the complexity of the system as well as the costs of withdrawals.

---

**samueldashadrach** (2021-04-18):

What if user A tries to double-spend user B by attempting to not include the latest tx from A to B, when withdrawing?

Does B have to be online to respond to such challenges?

---

**avihu28** (2021-04-18):

This is enforced by the proof - ie part of the statement being proven when a withdrawal is presented is that it was presented with all the txs leading to it from the last k blocks.

---

**samueldashadrach** (2021-04-18):

yeah but someone can include a previous set right?

like if A sent to B and B sent to C in the last k blocks, B can show only the A to B tx and not the B to C and attempt withdrawal. C needs to be online to catch it.

---

**avihu28** (2021-04-18):

You only withdraw from the latest state. So if in the latest state B doesn’t have the funds (the B->C tx was already committed) he can’t withdraw it.

But there is a longer finality of k blocks because in the worst case there will be a rollback of txs that were not a part of a recent withdrawal in the last k blocks.

---

**samueldashadrach** (2021-04-18):

Am a bit confused. The idea is the person withdrawing doesnt know the latest state, right? (Or he can pretend not to know)

So you’re saying there is a way to check whether a withdrawal attempt (old state + k transactions) is valid purely from the published proof and no need to publish new state? (And that there were no newer txs that make the withdrawal invalid)

