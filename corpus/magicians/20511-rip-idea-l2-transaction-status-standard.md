---
source: magicians
topic_id: 20511
title: "RIP Idea: L2 Transaction Status Standard"
author: highlander
date: "2024-07-09"
category: RIPs
tags: [transactions, status]
url: https://ethereum-magicians.org/t/rip-idea-l2-transaction-status-standard/20511
views: 1045
likes: 19
posts_count: 15
---

# RIP Idea: L2 Transaction Status Standard

A recent discussion (June 2024) in the RollCall Telegram Group has yet again shown that a lack of standards around the processing status of an L2 transaction is confusing not only for users and developers (block explorers, wallets, smart contracts, chain analytics) but also for client teams themselves trying to understand what different statuses mean and what trust assumptions have been made for each status. Besides confusion, there are real security risks, especially for L2 bridges based on the processing status of an L2 transaction (finalized on the L2 but not on the L1 vs finalized on the L2 and the L1).

This topic of discussion also arose in the [OASIS Ethereum Open Projects L2 Standards WG](https://github.com/ethereum-oasis-op/L2) when discussing the [L2 Transaction Fee API specification](https://github.com/ethereum-oasis-op/L2/pull/53). The WG decided to make L2 Transaction Statuses their next work item.

To start the discussion, the WG decided to propose a simple set of statuses both as a string and as a hex value, their definitions and trust assumptions. The minimal set of transaction statuses proposed is as follows:

- L2 Pending: An L2 transaction submitted to an L2, and waiting to be processed by a sequencer. Trust Assumption: No inclusion guarantee on the L2
- L2 Replaced: An L2 transaction that was “Pending” was replaced by another L2 transaction. Trust Assumption: Same as L2 Pending
- L2 Dropped: An L2 transaction that was removed from the L2 processing queue. Trust Assumption: NA
- L2 Confirmed: An L2 transaction processed by a sequencer and assigned an order in a proposed L2 block by the sequencer by applying an L2 client-specific L2 transaction ordering protocol. Trust Assumption: The L2 transaction order guarantee is based on the security guarantee of the ordering protocol. Inclusion in finalized L2 and L1 blocks is not guaranteed.
- L2 Included, L1 Pending: An L2 transaction included in an L2 block but not yet submitted to the L1. Trust Assumption: The L2 inclusion guarantee is dependent on the submission guarantee of the L2 block to the L1 and L1 Finalization.
- L2 Included, L1 Included: An L2 transaction included in an L2 block submitted to the L1. Trust Assumption: The L2 inclusion guarantee is dependent on L1 finalization.
- L2 Finalized, L1 Finalized: An L2 transaction included in a L2 block that has been included in a finalized L1 transaction. Trust Assumption: The L2 transaction finalization guarantee is equivalent to an L1 transaction finalization guarantee in a finalized L1 block.

## Replies

**ajsutton** (2024-07-09):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/highlander/48/2923_2.png) highlander:

> L2 Finalized, L1 Finalization pending: An L2 transaction included in an L2 block submitted to the L1. Trust Assumption: The L2 finalization guarantee is dependent on L1 finalization.

I don’t see how it makes sense for an L2 transaction to be “finalized” if it hasn’t yet been submitted to the L1. This is what OP Stack would call an `unsafe` block, available from the `latest` tag on JSON-RPC and it is the most likely category of block to be reorged. The term finalized should only be used for things that will not change within normal protocol operation (e.g like L1 finalized won’t change without at least 1/3rd of validators being slashed).

---

**highlander** (2024-07-10):

Well, it makes sense for those L2s that do not submit a new L2 block to the L1 every few seconds. That means you can have L2 blocks finalized on the L2, and, therefore, the new state can be used for subsequent L2 transactions, without the L2 block even submitted to the L1.

Would you not agree?

---

**timbeiko** (2024-07-10):

I agree with Adrian that overloading the “Finalized” term, which has a very specific meaning in Ethereum, would be misleading to users. Why not simply rename “L2 Confirmed” to “L2 Included”?

This way, you could also have:

- L2 Included, L1 Pending
- L2 Included, L1 Included
- L2 Finalized, L1 Finalized

---

**highlander** (2024-07-10):

[@timbeiko](/u/timbeiko) That is a good suggestion, will incorporate

---

**ranchalp** (2024-07-15):

IMO when a transaction is included and attested by some BFT protocol at the L2 consensus level (but not yet even submitted to L1) this should be called L2 finalized, and we should deal with the notion of L2 finality and L1 finality as two different layers of security.

The definition of finality in Ethereum is exactly that: the set of attesters voted on this block and thus this block will not suffer a reorg unless a third of the attesters equivocate. If the number of validators and economic security halved by some event in Ethereum, the definition of L1 finality in Ethereum would remain the same. I believe it is unrealistic to ask of an L2 consensus to choose a different term for the same notion (regardless of what is the economic security and number of validators in that L2).

---

**highlander** (2024-07-16):

[@ranchalp](/u/ranchalp) I agree with you, except that even if the L2 is finalized based on the finalization conditions of the L2 consensus algorithm an L1 reorg (before L1 finalization) will force an L2 reorg, or minimally a resubmission of the L2 blocks that were reorged on the L1.

Therefore, and only IMHO, for the word finalization to mean the same thing on an L2 and an L1, the L2 state can only be called finalized once the L1 state containing the L2 state is finalized.

The key is that we come up with a set of definitions we can all align with, albeit not necessarily agree with 100% – compromise rules ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12)

---

**dontpanic** (2024-07-17):

In 2018, [@expede](/u/expede) made efforts to standardize status codes for L1 contracts using erc-1066, akin to HTTP status codes. Hexadecimal codes were preferred there too for their neutrality and parsing simplicity compared to strings. The future evolution of L2 platforms may diverge from current practices. The primary objective was to enhance contract interface understanding of inter-contract message statuses. Is there an opportunity to unify L2 and L1 statuses under a single standard? [ERC-1066: Ethereum Status Codes (ESC)](https://ethereum-magicians.org/t/erc-1066-ethereum-status-codes-esc/283)

---

**highlander** (2024-07-17):

[@dontpanic](/u/dontpanic) I looked at 1066. Since it was referring to smart contract codes, I decided not to reference it in the initial write-up. Thank you for sharing.

I think status codes, in addition to a string, are also important and should be included. I think once we can align on the language and meaning of words, we can assign codes.

---

**sbacha** (2024-07-24):

Why not consider an rpc method getTransactionBySenderAndNonce

https://github.com/ethereum/execution-apis/issues/494

More details:


      ![](https://github.githubassets.com/favicons/favicon.svg)

      [github.com](https://github.com/manifoldfinance/rpc-eip-drafts/tree/master/eth_getTransactionBySenderAndNonce)





###



Custom RPC Methods for Ethereum/EVM chains. Contribute to manifoldfinance/rpc-eip-drafts development by creating an account on GitHub.

---

**Eikix** (2024-07-24):

What would happen if there are 5 transactions with same sender and nonce? (Someone trying to replace transactions)

---

**ranchalp** (2024-08-21):

[@highlander](/u/highlander)

> I agree with you, except that even if the L2 is finalized based on the finalization conditions of the L2 consensus algorithm an L1 reorg (before L1 finalization) will force an L2 reorg, or minimally a resubmission of the L2 blocks that were reorged on the L1.

Ethereum could tomorrow decide to protect against long-range attacks by checkpointing its state on to Bitcoin as an L0 (as is being discussed for some other PoS L1s, e.g. in Filecoin, or in academia, e.g. [1, 2]), which might also mean that a resubmission of checkpointed snapshots could be necessary in the event of a reorg. But this is IMO orthogonal with the notion of finality, which is internal and Ethereum-specific. I still think the same should be used for L2s.

> The key is that we come up with a set of definitions we can all align with, albeit not necessarily agree with 100% – compromise rules

Is there a manifested support for the terminology used in this RIP vs. some other?

[1] Azouvi, Sarah, and Marko Vukolić. “Pikachu: Securing PoS blockchains from long-range attacks by checkpointing into Bitcoin PoW using Taproot.” *Proceedings of the 2022 ACM Workshop on Developments in Consensus* . 2022.

[2] Tas, Ertem Nusret, et al. “Babylon: Reusing bitcoin mining to enhance proof-of-stake security.” *arXiv preprint arXiv:2201.07946* (2022).

---

**highlander** (2024-08-24):

[@ranchalp](/u/ranchalp) With the Pectra hardfork, Ethereum will have single slot finality (SSF) which makes this discussion mute. Note the “L2 Included, L1 Included” would only exist for ~12 seconds.

As to manifested support, see the comments here, plus the L2 Standards WG have created and already discussed a draft – See [PR](https://github.com/ethereum-oasis-op/L2/pull/55)

The WG has representatives from all major L2s, and people from RollCall stopped by to discuss the topic too.

Will also organize a RollCall break-out session.

---

**ranchalp** (2024-08-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/highlander/48/2923_2.png) highlander:

> @ranchalp With the Pectra hardfork, Ethereum will have single slot finality (SSF) which makes this discussion mute. Note the “L2 Included, L1 Included” would only exist for ~12 seconds.

SSL does not really solve the issue in the example I was suggesting with BTC as an L0 for long-range attack protection, if anything it makes speaking of L2 finality easier to argue for, as there would be no fork in Ethereum and no resubmission/reorg of L2 needed. Is this what you meant?

---

**highlander** (2024-09-04):

[@ranchalp](/u/ranchalp) Yes, SSF avoids reorgs, and therefore, L2 resubmissions. Therefore, the L2 included and L1 included status is only a very short-lived state ~ 12s, yet still required.

