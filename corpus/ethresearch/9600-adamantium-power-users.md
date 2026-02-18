---
source: ethresearch
topic_id: 9600
title: Adamantium - Power Users
author: avihu28
date: "2021-05-24"
category: Layer 2
tags: [zk-roll-up]
url: https://ethresear.ch/t/adamantium-power-users/9600
views: 11659
likes: 12
posts_count: 18
---

# Adamantium - Power Users

**TL;DR:** we propose Adamantium, a protocol for Autonomous Data Availability, which retains the scaling benefits of off-chain data availability, while removing all trust assumptions for any willing user. Willing to do what? To be online; and if they aren’t online, their funds cannot be stolen, nor frozen - rather, the funds are moved from L2 back to an Ethereum address under the user’s control.

**Background**

Validium relies on a DA Committee ([DAC](https://medium.com/starkware/tagged/starkex-self-custody)), made up of a set of reputable players in the blockchain space. DAC members store off-chain a copy of the account balances, and attest to the availability of its state S by signing the Merkle root of S after every batch processed by the StarkEx Operators.

Validium’s trust assumptions: Validium requires users to trust DAC members in one very particular scenario, which we call the Escape Hatch. In case the StarkEx Operators censor a user’s withdrawal request, users trust at least one DAC member to publish a current copy of the latest state S (read a complete description of the protocol [here](https://medium.com/starkware/data-availability-e5564c416424?source=collection_home---2------0-----------------------)). Can Validium be improved and made completely trustless? It can, and we call the improved protocol Adamantium.

[![Adamantium Description](https://ethresear.ch/uploads/default/optimized/2X/0/04df68a90f0b25c1ca14e3bdc97d9e525cd85e78_2_509x500.png)Adamantium Description1400×1375 118 KB](https://ethresear.ch/uploads/default/04df68a90f0b25c1ca14e3bdc97d9e525cd85e78)

**Description**

In Adamantium, users can operate in a fully trustless manner, by choosing to become a Power User (PU). The funds of a PU are always in her custody: typically a PU provides a signature that she has access to her own off-chain data, thus allowing her to activate her personal Escape Hatch with the Application Smart Contract on L1. Absent that timely signature, the PU’s funds are automatically withdrawn back on-chain (aka Protective Withdrawal).

What about users who do not wish to become a PU? With Adamantium, they have a wider set of choices. They will no longer be restricted to trusting a DAC member - they can opt to trust any Power User willing to serve as a watchtower on their behalf (and would have to authorize that PU to do so).

#### Participants:

- DAC: The DAC continues to operate, and offer its services to any interested users (i.e. app users)
- Users:

Regular Users: Users can continue to operate as they did previously, and rely on the DAC to fill its role, as described above.
- Power User (PU): A user who trusts no one - not the DAC nor anyone else.

##### System Design Implications & Economics:

- PU (Power User):

A PU has one or more Merkle tree vaults mapped to it - these are the vaults she signs for
- A PU is generally expected to be online:

Response time: a PU needs to provide her signature within a proof-generation time frame, so her response time is measured in minutes, not seconds.
- Cost: they have enough at stake, and care enough not to trust other parties, to warrant the hassle and expense.

When on-line: PU performs the same computational work as a DAC member: they need to hold the balance tree and verify the Merkle tree up to the root.
We estimate the PU’s monthly computational cost to be a few $100s/month.
- When going off-line: a Protective Withdrawal is executed.
Protective Withdrawal - the protocol-enforced withdrawal of funds back on-chain as call data - is the key innovation in Adamantium. Absent a timely cryptographic signature from the PU, the Operator is forced to make the funds available to the PU on mainnet.
In a given proof batch cycle, the Operator pays for call data only for those users who went off-line during that cycle. Importantly, this gas expense does not scale with the number of transactions in a given batch, nor with all users who are merely still off-line. Naturally, the Operator may charge the PU for this sequence.

Application Operator (e.g. the exchange):

- Adamantium Vaults: The Application Smart Contract tracks the vaults mapped to every PU.
- Protective Withdrawals Cost: Tx batching reduces the gas cost of a Protective Withdrawal so the amortized cost approaches the gas cost of placing the data on-chain.
- An Operator can ignore a PU’s signature, thus triggering an unwarranted Protective Withdrawal. Repeating this kind of ordeal too many times will simply cause PUs to switch to a competing application.

[![Screen Shot 2021-05-31 at 15.03.25](https://ethresear.ch/uploads/default/optimized/2X/f/f9621ee8f86ec2a2d793a5b568d872c806d296e6_2_690x286.png)Screen Shot 2021-05-31 at 15.03.251402×582 32.4 KB](https://ethresear.ch/uploads/default/f9621ee8f86ec2a2d793a5b568d872c806d296e6)

* Other than running an Ethereum node

** Till you withdraw

##### Protocol Extension: Followers of a PU

A Follower is a user who chooses to put their trust in one or more PUs that provide them with a watchtower service for a fee. A PU should sign not only for their own vaults, but also for the vaults of their Followers.

A Follower’s funds will be withdrawn back on-chain only if none of the PUs it follows have provided their timely cryptographic signature. By following multiple PUs, a Follower reduces the likelihood that a chance disruption of service by any single PU will result in a withdrawal of funds.

A PU could ignore a Follower’s signature, thus triggering an unnecessary Protective Withdrawal. We believe this kind of behavior will be very limited in scope, as Followers will simply switch to more reliable PUs.

## Replies

**StanislavBreadless** (2021-05-26):

Nice idea, but I still don’t get how is the operator *forced* to withdraw PU’s funds onchain. Could you please elaborate more?

Even if the withdrawal is enforced on the smart contract during each proof execution, why can’t the operator stop producing blocks?

Also, why can’t the operator ignore adding new PU’s, or the addition of a new power user should be done on-chain?

---

**avihu28** (2021-05-26):

For a state transition to happen, a proof attesting to the validity of this state transition has to verified on-chain.

Part of the statement being proven says that, for every PU, either they signed, or their funds *has to be* withdrawn. So if the operator wants to post a new state transition, they have to withdraw that PU funds.

The operator can stop producing blocks. In this case, every user can submit an on-chain request to withdraw their funds. If the request isn’t fulfilled by the operator after some time, users can freeze the system and withdraw funds from the merkle root by presenting the merkle path to their balances.

If the operator ignores adding a PU, this user can choose not to deposit funds to the system while their request is not approved.

---

**nktrong** (2021-06-01):

Interesting idea. How about assets that are defined only in Validium? Will the system redeem or exchange these assets into L1 assets so that users’ funds can be entirely withdrawn. For example, if power users have liquidity tokens of an AMM SC in Validium, the withdrawal of funds to L1 might require the burn of these tokens to redeem the initial L1-compatible token pair.

---

**avihu28** (2021-06-08):

A withdrawal process should be defined also for this type of token.

In StarkEx, for example, tokens that are minted on L2 can be withdrawn to L1 and will be minted there. So yes, in similar lines to what you described.

---

**avihu28** (2021-06-11):

I think there is a nice tradeoff that enables PU to only do log(n) work instead of O(n), in return for publishing log(n) data per withdrawal.

In the original proposal, PUs are holding the state so they can update their witnesses based on withdrawal data.

Well, what if withdrawal data will include not only the withdrawal but also the list of nodes changed because of it?

Then it’s enough for PU to only hold their witnesses and it would be possible to update them based on this data.

We are getting the worst case to be x log(n) data on-chain for PU to do log(n) work and not O(n).

---

**nktrong** (2021-06-16):

In fact, we have a similar idea but instead of having Validium as default, we have Zk-rollup as default setting.  If a Tx is included without any confirmation, its data must be published just like Zkrollup. Each time users confirm that they have data availability, the blocks that include their Txs can omit some on-chain data. The factor of gas economic maybe lower than Adamantium but it is more convenient for small users.

---

**bpfarmer** (2021-08-05):

I might be misunderstanding this scheme, but I don’t understand why the following attack is prevented.

A user deposits into the L2 as a PU (power user). The operator is malicious, and wishes to freeze/hold user funds for ransom. The operator submits a new (valid) state transition, withholds all updated witnesses that would allow users to exit, and then stops producing blocks.

There doesn’t appear to be any mechanism that would force the operator to submit a new state transition which in turn would force the operator to process protective withdrawals for all PU. Therefore, while it seems as though this is better than an ordinary ZKP-powered sidechain, because the operator can’t selectively freeze certain users while continuing to produce blocks, it doesn’t remove all trust assumptions because the operator can still hold all user funds hostage.

---

**avihu28** (2021-08-06):

> [The operator submits a new (valid) state transition…]

A valid state transition here enforces that, for every PU, either they signed on the root of the new state (before withdrawals) or that the operator withdraws their funds for them.

This is enforced by the proof, the same way all other “valid” transitions are enforced.

That’s why, in the situation you described, every PU either has the data to exit or will have their funds withdrawn after the state update.

---

**bpfarmer** (2021-08-06):

> that the operator withdraws their funds for them.

Ok, I think I see the misunderstanding - I assumed that protective withdrawals would affect the state, because they’re described as “withdrawn back on-chain” and in the graphic it says that outstanding settlements are executed.

To put it more clearly, suppose I’m a PU and sign a new root S’. A delinquent PU doesn’t sign and his account is protectively withdrawn back on-chain, but that action can’t affect S’ or it would invalidate the inclusion proof that I’ve received for my account.

Maybe by protective withdrawal you mean something other than a withdrawal or exit, just publishing the inclusion proof for an account on-chain, though this seems like it would be significantly more expensive in CALLDATA than a typical rollup (maybe not an issue if it’s assumed to occur rarely).

---

**fradamt** (2021-09-27):

What happens if too many PUs go offline at the same time and it is not possible to exit all of them at once because it would require more gas than an Ethereum block’s gas limit?

Then there can’t be any valid state update until enough of them come back online, which might be never.

One way to mitigate the issue could be to break up such a mass exit, by allowing state updates which perform only withdrawals, even if only a subset of the required ones, and having as many updates as needed until all required withdrawals have been performed. That way after any update it is still possible for all users to manually exit if needed.

While it can stop progress for a bit, it’s at least very expensive to do so, because it would require the PUs which are going offline to pay the gas for full Ethereum blocks, including the progressively increasing basefee and having to outbid all other Ethereum users.

Except, what if they can’t pay for it? Or generally, what happens if a user does not have enough money to pay for their own withdrawal? For example the Operator might want to make a state update during a time in which gas fees are very high, but some forced withdrawals might become prohibitively expensive even for users which have a non-negligible amount of money on L2.

It seems like you’d need some kind of deposit which tries to make sure that under all circumstances an exit will be affordable. Even ignoring extraordinary circumstances like the attack mentioned above, that might be already be a problematic requirement for users which are not PUs themselves but rather only delegating their custody to other PUs

---

**avihu28** (2021-10-10):

Thanks for the question!

![](https://ethresear.ch/user_avatar/ethresear.ch/fradamt/48/6474_2.png) fradamt:

> What happens if too many PUs go offline at the same time and it is not possible to exit all of them at once because it would require more gas than an Ethereum block’s gas limit?
> Then there can’t be any valid state update until enough of them come back online, which might be never.

I think there is no reason not to break the state transition into several transactions, and of course not all of them have to be in the same block. In fact, even today in StarkEx every state transition is made of several txs, with proof verification, on-chain data and storing state transition data all broken into several txs. So the block size is not the limiting factor.

In addition (if for some reason we want to keep state transition short), even the state transition can be broken into several transitions - where the first transitions are withdrawals only so no signatures are required (see comments below). This will follow with the rest of the state transition without the problematic PUs.

![](https://ethresear.ch/user_avatar/ethresear.ch/fradamt/48/6474_2.png) fradamt:

> One way to mitigate the issue could be to break up such a mass exit, by allowing state updates which perform only withdrawals, even if only a subset of the required ones, and having as many updates as needed until all required withdrawals have been performed. That way after any update it is still possible for all users to manually exit if needed.
> …

Some comments on withdrawals in the suggested model:

- Withdrawals always include on-chain data. That means that for withdrawals only transition no PU signature is required (they can always recompute the state based on the previous info and on-chain data).
- Every user can ask the operator to withdraw funds on their behalf. In the normal case its the operator performing the withdrawal for the user and pays for it. Only  if the operator is not responsive for a long time (“grace period”) to the user’s request the user can perform the withdrawal by themselves.
- If the operator is not responsive (for any reason) to users withdrawal requests the system will freeze and every user will have a very long time to withdraw their funds from the frozen state. So they are less exposed to the gas prices at a specific moment.
- If for some reason many or all PU are not responsive the operator can choose to serve only withdrawals for the while, of which no signature is required (as I mentioned in the first comment).

---

**bambroo** (2022-02-15):

Hey, 1. Is it like the full nodes of Starkware that store the data are forced to publish the data on chain as call-data if the PU went offline? 2. For users opting to be PU, do they have to run a node to store their own data offline? Any other node running requirement?

---

**NicLin** (2022-06-18):

Hi, the design seems very interesting. I have a question regarding how PU maintains the merkle proof(s) of his account balances.

In Validium, DAC has the transaction data so they all can derive the latest state and have the full view of every account’s balance and can thus generate the merkle proof for each account in the state tree. However, in Adamantium, who has the transaction data? If a PU doesn’t have access to the transaction data, how can he updates the merkle proof(s) of his account balances?

---

**randomishwalk** (2022-07-28):

Interesting design! Curious [@avihu28](/u/avihu28) how you think this type of design compares to Arbitrum’s AnyTrust design (setting aside the differences between optimistic and validity designs) whereby failures in the DAC cause a fallback to a rollup mechanism?

[Arbitrum AnyTrust docs](https://developer.offchainlabs.com/docs/anytrust)

---

**avihu28** (2022-08-29):

The goal is to enable PU and users to withdrawal out of the system whenever they wish. Therefore, only accounts balance (storage) information is needed, and not transaction data.

In any case, the PU should only sign have they received the data needed for them to perform a withdrawal. They should receive that data from the operator, or else refuse to sign.

---

**avihu28** (2022-08-29):

Good question!

I haven’t went thoroughly over all the details of anytrust, so might be wrong or inaccurate here.

But IIUC main differences come to mind:

1. DAC Is a previously chosen closeג permissioned quorum. The reason is that if you add unknown members and many go offline they turn the system into fully on-chain data one. Which defeats the purpose of anytrust. With PU one can be more permissive with who can become a PU. In the worst case they’d join and then be withdrawn if they don’t function. Asking for a deposit to cover that cost makes it an easier case.
2. In the case some DAC members don’t sign all batch data goes on chain. In the case where some PUs don’t sign their withdrawal data goes on-chain (so different data in those cases)
3. Trust level in anytrust is that DAC can steal all funds. This is worse than Validium (DAC can freeze the funds) and both are worse than Adamantium (where users can be fully trustless)
4. Anytrust is described for a general purpose rollup. Adamantium here is described for app specific use case. There can be a validity rollup with the same mechanism as anytrust, and Adamantium can be expended to a general logic, but this is not what is being described here. It requires more thought.

---

**randomishwalk** (2022-08-30):

Good points! I need to think about the compare & contrast a bit more…

In the meantime [@avihu28](/u/avihu28), has your thinking on this type of design evolved at all since the original post? Just curious, given there seem teams taking multiple approaches to DA (outside of the enshrined L1 solution obviously) ![:blush:](https://ethresear.ch/images/emoji/facebook_messenger/blush.png?v=12)

