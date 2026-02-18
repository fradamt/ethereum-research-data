---
source: magicians
topic_id: 12072
title: "EIP-6110: Supply validator deposits on chain"
author: mkalinin
date: "2022-12-09"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-6110-supply-validator-deposits-on-chain/12072
views: 5012
likes: 12
posts_count: 33
---

# EIP-6110: Supply validator deposits on chain

Discussion thread for [EIP-6110: Supply validator deposits on chain](https://github.com/ethereum/EIPs/pull/6110).

## Replies

**poojaranjan** (2023-07-27):

[PEEPanEIP # 112: EIP-6110: Supply validator deposits on chain](https://youtu.be/tRTBgCN9VgY) with [@mkalinin](/u/mkalinin), Kevin Bogner & Navie Chan

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/e/e812e64f2c1124558bfa87f41e656174e6bf7abe.jpeg)](https://www.youtube.com/watch?v=tRTBgCN9VgY)

---

**mxs** (2023-11-07):

Hello,

Just a couple of notes on this specific point:

> Decrease of delay between submitting deposit transaction on
> Execution Layer and its processing on Consensus Layer. That is, ~13
> minutes with in-protocol deposit processing compared to ~12 hours with the existing mechanism.

This part of the proposal moves some complexity to operators in models where stakers ask operators to generate keys & operators deploy them:

- operators don’t know if a generated key is going to be deposited or not (transactions can be cancelled, misclicks, issues with wallets, etc), which means they either need pre-deploy keys the moment they are generated and end up managing dead keys in an infrastructure (with the risk of deleting them by mishap), or implement real-time watchers to deploy on-the-fly new deposits to their infra,
- restarting some components of an eth stack to add new keys can take time, more than 2 epochs: for example using scrypt or pbkdf2 for keystores, it can take minutes up to hours for web3signer or validators to load keys at start if you handle hundreds of them. Today you can schedule those restarts in time to add new keys in batch to reduce the overall impact, with this proposal you likely need to implement the key manager API to deploy without interrupt, which increases complexity.

I don’t think those points should impact the EIP as the user experience/model is better than the current one, just wanted to give a perspective on operational implications.

---

**mkalinin** (2023-11-08):

Hello [@mxs](/u/mxs),

Thanks a lot for bringing this to attention! If re-deploys takes so long the only way would be to pre-deploy keys and send a generated key to a staker only after it was deployed as you’re mentioning. Stale keys is probably a rare case, the other problem is that the response to a staker will be delayed by the time required to pre-deploy. Is it possible to add keys on the fly to a deployed instance of e.g. web3signer? If not I am curious how feasible it is to implement this feature considering security implications.

---

**mxs** (2023-11-08):

Thanks for the quick answer!

Yes, it is possible via the [key manager API](https://ethereum.github.io/keymanager-APIs/) to add keys without restarting in the case of validators, for Web3signer specifically I think the [hot-reload feature](https://consensys.github.io/web3signer/web3signer-eth2.html#tag/Reload-Signer-Keys/operation/RELOAD) is incremental (will confirm after testing), i.e: you could update the config automatically upon new deposits, call hot-reload which would only adds keys that aren’t yet loaded.

Async APIs approaches work as well, but this means you can’t be stateless regarding the deposit data: you need to store it somewhere secure, pre-deploy the key, then fetch it back to return it to the user. Being stateless on the deposit data is desirable as you can’t screw it up (i.e: no place for bugs to send the same deposit twice or the wrong one), you also don’t need to handle secure storage in the read-path of your API and implications around this.

IMHO the best approach here for operators is to generate keys and return them to stakers in a sync fast way, and handle the on-the-fly deployment on their side.

---

**mkalinin** (2023-11-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mxs/48/9802_2.png) mxs:

> IMHO the best approach here for operators is to generate keys and return them to stakers in a sync fast way, and handle the on-the-fly deployment on their side.

Yes, I entirely agree. I thought there is no way to do fast on-the-fly handling with existing key management, but if this option exists it will definitely be the path to take. It is worth raising node operator’s awareness when this feature will be considering for inclusion.

---

**mkalinin** (2023-11-13):

[@mxs](/u/mxs) I’ve made a straightforward calculation and the earliest time when a deposited validator is getting activated (with EIP-6110 in place) is `7` epochs after it was deposited which is about 45 mins. This is quite enough of a time to deploy new keys, isn’t it? Bits of the calculation from the [registry updates](https://github.com/ethereum/consensus-specs/blob/dev/specs/phase0/beacon-chain.md#registry-updates):

- 1 epoch of activation eligibility delay
- 2 epochs of finalizing the activation_eligibility_epoch to become eligible for activation according to is_eligible_for_activation
- 4 epochs minimal from compute_activation_exit_epoch

---

**mxs** (2023-11-21):

Thanks for doing the math, yes I think it makes such automation possible, it’s enough time to have multiple checks going on/time to deploy.

---

**TheDZhon** (2024-02-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mxs/48/9802_2.png) mxs:

> operators don’t know if a generated key is going to be deposited or not (transactions can be cancelled, misclicks, issues with wallets, etc), which means they either need pre-deploy keys the moment they are generated and end up managing dead keys in an infrastructure (with the risk of deleting them by mishap), or implement real-time watchers to deploy on-the-fly new deposits to their infra,

I am not sure that the operators are more vulnerable in this model rather than stakers themselves; they key issue is that the operator is able to front-run the deposit transaction with the same pubkey but different withdrawal credentials (e.g. doing 1ETH pre-deposit) and no matter what are the withdrawal credentials would be after that, only the pre-deposited ones would be assigned to the newly activated validator

The issue is relevant for the already existing staking pools, e.g. Lido: [lido-improvement-proposals/LIPS/lip-5.md at develop · lidofinance/lido-improvement-proposals · GitHub](https://github.com/lidofinance/lido-improvement-proposals/blob/develop/LIPS/lip-5.md) and mitigated via additional pre-confirmation steps and front-running prevention security committees for the keys.

---

**eawosika** (2024-03-13):

I published an in-depth explainer on EIP-7251 for those interested in learning more about EIP-6110’s proposal to introduce on-chain validator deposits and deprecate the Eth1-Eth2 bridge in favor of a simple, secure, and more efficient system for delivering deposits to the Beacon Chain: [EIP-6110: Fixing Beacon Chain Tech Debt](https://research.2077.xyz/eip-6110-fixing-beacon-chain-tech-debt).

The article provides historical context for the Eth1-Eth2 bridge and explores the impact of the Eth1-Eth2 bridge (and Eth1Data polling) on node operator UX and the Beacon Chain’s economic security (among others). It also explores EIP-6110’s approach to reforming the validator deposit process and analyzes the advantages and potential drawbacks of replacing the existing deposit processing workflow with an in-protocol deposit processing mechanism.

All comments/feedback are welcome.

---

**etan-status** (2024-04-29):

What’s the upside of introducing a new encoding, instead of simply reusing the existing [DepositData](https://github.com/ethereum/consensus-specs/blob/dev/specs/phase0/beacon-chain.md#depositdata)?

Why a generic mechanism for validator messages over simply adding a deposits list, or replacing the withdrawals tree with a container that supports both deposits and withdrawals?

---

**etan-status** (2024-04-29):

> With 1 ETH as a minimum deposit amount, the lowest cost of a byte of deposit data is 1 ETH/192 ~ 5,208,333 Gwei. This is several orders of magnitude higher than the cost of a byte of transaction’s calldata, thus adding deposit operations to a block does not increase DoS attack surface of the execution layer.

It’s not a cost. One can simply spam 1 ETH deposits onto a validator that is already exited and gets a full refund. The deposits per block are no longer limited, making it far quicker than the current 2-3 years to completely fill up the deposit contract (2^32 limit).

---

**etan-status** (2024-04-29):

Following up on this, it seems that:

> The encoded deposits will be included in the header and body as generic requests following the format defined by EIP-7685.

as is, is only used for the EL block header, but not for the CL ExecutionPayload.

In the EL block header, it’s arguably not needed, as the same information can be computed purely from the receipt. In the CL, it seems that the EIP-7685 framework to abstract across operations does not cleanly apply, based on the current spec.

Would prefer if EL block header / CL ExecutionPayload would conceptually match. The earlier design with a simple deposits tree (as is still proposed for the CL) seems much cleaner than the generic EIP-7685 framework. Even cleaner if the EL could reuse the same data structure from CL.

---

**etan-status** (2024-04-29):

> index field

For this rationale here, the mechanism worked so far without a per-`DepositData` index. The indices are completely sequential. An alternative design could be to keep `deposit_count` around. That would also eliminate the need for `deposit_receipts_start_index` (as in, this would be equivalent to whatever the `deposit_count` was at time of fork).

---

**matt** (2024-04-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/etan-status/48/7861_2.png) etan-status:

> What’s the upside of introducing a new encoding, instead of simply reusing the existing DepositData?

Mostly that we don’t have to introduce SSZ on the EL. It doesn’t seem like teams are interested in undertaking this right now.

---

**etan-status** (2024-04-29):

“It doesn’t seem” based on what?

- Geth / Erigon already contain SSZ light clients to follow CL chain.
- From L2 teams, @protolambda voiced support for EIP-6493 in ACDE 184

---

**etan-status** (2024-04-29):

For the transition, are we sure that the current logic processes deposits in order? It seems that there may be an extra few eth1_data voting periods before the old mechanism gets disabled.

Correct processing order is important e.g. for Rocketpool scrub check, because if deposits can get reordered the withdrawal address for a validator key may be reassigned to something else.

---

**matt** (2024-04-29):

I think you should raise this point on ACDE. AFAIK, we never considered SSZ encoding this data.

Several people on the geth team are not happy with fastssz. Yes, we use it in our light client, but that’s more of an experimental feature right now.

---

**etan-status** (2024-04-29):

https://github.com/ethereum/pm/issues/1029#issuecomment-2083588283

---

**etan-status** (2024-04-29):

For the [weak subjectivity analysis](https://eips.ethereum.org/assets/eip-6110/ws_period_analysis), would be nice to also extend this to average > 32 ETH, to see presence/absence of interactions with MaxEB proposal.

---

**mkalinin** (2024-05-03):

hey [@etan-status](/u/etan-status), attempting to address some of the concerns you have shared recently:

- In the attack scenario that you have described 1 ETH is not the cost, but there is an opportunity cost of the funds being locked on CL until they are withdrawn. With 1_000_000 validators it is about 9 days, with 512_000 validators (assuming after consolidation unlocked by MAXEB we have this number) it is 4.5 days. So to effectively burn deposit contract slots one will have to get a decent amount of spare ETH. IMO, it makes such attack non-viable.
- The order of deposit processing is not enforced, and during transition period more recent deposits will likely be processed before older ones (older than those that are supposed to be included by eth1 data poll). We should reach out to pools to get more feedback on it.
- MAXEB makes every top-up to an active validator to pass through the activation churn which does eliminate the impact of 6110 on the WS computation.
- index field is basically required for the transition period.
- Having deposits can be helpful in a situation when EL is serving block bodies to CL. Otherwise, it would require EL to parse them from receipts.

I have a follow-up questions:

- Do you suggest to pass deposit_count alongside to each deposit? or to a bunch of deposits?


*(12 more replies not shown)*
