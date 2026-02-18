---
source: ethresearch
topic_id: 22218
title: Relay Inclusion Lists
author: kubimens
date: "2025-04-25"
category: Proof-of-Stake > Block proposer
tags: [mev, proposer-builder-separation, censorship-resistance]
url: https://ethresear.ch/t/relay-inclusion-lists/22218
views: 1084
likes: 22
posts_count: 9
---

# Relay Inclusion Lists

Co-authored by [Michael](https://x.com/mostlyblocks) and [Kubi](https://x.com/kubimensah) ([Gattaca](https://x.com/gattacahq)). Special thanks to [Thomas](https://x.com/soispoke), [Julian](https://x.com/_julianma), [Toni](https://x.com/nero_eth), [Ladi](https://x.com/ladislaus0x), [Justin](https://x.com/drakefjustin), [Auston](https://x.com/austonst) and [Max](https://x.com/0xKuDeTa) for their feedback and suggestions. Feedback is not necessarily an endorsement.

### Overview

This document introduces relay inclusion lists (rILs), a way to immediately improve Ethereum’s censorship resistance without introducing protocol changes, new trust assumptions, or significant technical complexity. The design is intended as a new default feature for non-censoring relays, with an opt-out option provided to accommodate validator preference.

We proceed by detailing how relay inclusion lists increase Ethereum’s censorship resistance while preserving validator’s risk-reward balance. We then propose a rule for constructing relay inclusion lists that is efficient and resilient to outlier values, alongside enforcement procedures that integrate seamlessly with existing block validation. The document concludes with an outlook on promising future directions.

Overall, the document details the exact procedures for generating, validating, and enforcing inclusion lists in the relay. It reflects the [EIP-7805 (FOCIL) specifications](https://eips.ethereum.org/EIPS/eip-7805) to ensure protocol compatibility and operational integrity, preparing the block production system for a future in-protocol implementation of inclusion lists in a risk-off manner.

**[![](https://ethresear.ch/uploads/default/optimized/3X/e/0/e048a3c8ab4d33140a0e4bc016754381b135c70c_2_624x500.png)874×701 38.8 KB](https://ethresear.ch/uploads/default/e048a3c8ab4d33140a0e4bc016754381b135c70c)**

### Distribution and roll-out

Relays supporting relay inclusion lists will by default generate and enforce an inclusion list from transactions pending in the mempool for all blocks they deliver. Validators that wish to opt-out may do so by explicitly indicating this preference through the relay registration API, as an additional preference field.

Relay inclusion lists empower validators to immediately improve Ethereum’s censorship resistance without incurring any additional risk or trust assumptions, as the compilation and enforcement of the inclusion list is delegated to the relay, with the validator remaining blind to its contents upon signing the block header. An alternative out-of-protocol approach is [IL-Boost](https://github.com/eserilev/il-boost/blob/main/README.md), which delegates block building but retains inclusion list construction at the proposer level.

We note that the system is consistent with validator’s economic incentives. In practice, it will reflect as fuller blocks, which come with a minor latency trade-off due to their larger data footprint. In the case where all relays adopt the design, this trade-off will be minimized on a relative basis, as the bid curve will shift to accommodate this marginal and predictable latency overhead; put another way, the best bid is submitted earlier. In the case where some relays do not adopt the design, validators are insured through the standard block auction, which will continue to yield the highest-paying block.

Overall, the design does not impose additional requirements on validators, and allows them to improve Ethereum’s censorship resistance without shifting on the risk/reward curve. For this reason, the system is accessible and attractive to all participants, from solo stakers to large node operators.

### Inclusion List Generation and Communication

Relays independently generate inclusion lists from mempool transactions by applying a deterministic inclusion rule. The core purpose of the rule is to maximize the predictability of inclusion by observing the mempool only; specifically, the arrival times and priority fees of pending transactions.

We propose an initial, simple two-step rule:

1. Normalize waiting time and priority fee:
 For each transaction t in the mempool, compute:
  S_w(t) = \frac{w(t)}{\tilde{w}}, \quad S_f(t) = \frac{f(t)}{\tilde{f}}
 where:

w(t) is waiting time of transaction t in the mempool.
2. f(t) is the priority fee of transaction t.
3. \tilde{w} and \tilde{f} are the medians of the waiting times and priority fees respectively, for all transactions pending in the mempool.
4. Compute total score and adjust for transaction size:
 Each transaction is initially assigned a total score:
  S(t) = S_w(t) + S_f(t)
 The score S(t) is then size-adjusted to provide higher marginal pricing for large transactions:
  D(t) = \frac{S(t)}{size(t)}
 where size(t) is the transaction’s size measured in bytes. Transactions are then ranked in descending order of D(t).

The relay then builds an inclusion list with a maximum size of 8 kilobytes, in adherence to the EIP-7805 (FOCIL) specifications, by including the top-ranked transactions until there is insufficient marginal space for a further inclusion.

Normalizing via the median avoids skew from transactions that have not seen inclusion for economical reasons, i.e. due to underpayment. The rule is computationally efficient, as median calculation and transaction sorting can be performed quickly for typical mempool sizes using standard algorithms. An adversary attempting to grief the median by spamming low fee transactions would simply increase the prioritization score of other transactions; a simpler and cheaper way of reaching inclusion would just be to pay more.

Ranking the transactions by the density score imposes a higher marginal price per unit of blockspace consumption. This market-based approach incentivizes the inclusion of many smaller transactions, thereby maximizing participation from as many originators as possible. Large transactions, which consume more blockspace, can still be included quickly by increasing their priority fee accordingly.

Uniform application of the inclusion rule across all relays is desirable; in practice, it is most important that each relay fills the inclusion list to its maximum size (given sufficient transactions in the mempool), to preclude skewed IL implementations optimizing for latency (i.e. lean blocks). Relay behaviour is enforced via proposers, which may elect to opt out of relays that optimize for factors other than censorship resistance. The inclusion rule is economically rational and incentive-aligned by taking into account priority fees.

The inclusion list is computed before the beginning of each slot, and the relay exposes an HTTP API endpoint that builders use to fetch the completed inclusion list. There are no sorting constraints imposed on builders; transactions on the inclusion list can be sorted into the block in the most efficient way.

### Block Validation and Enforcement

Block validity is enforced against the FOCIL criteria; specifically, a block proposed to the relay is valid if and only if the following conditions are fulfilled:

1. Transaction Inclusion Check

- Every transaction listed in the IL provided by the relay is either:

Included explicitly in the block delivered by the builder.
- Verifiably invalid after executing against the block’s resulting post-state.

1. Simulated Transaction Validation

- The Relay simulates execution of each IL transaction not included in the block against the block’s post-state.

A block is invalid if it omits any inclusion‑list transaction that would, when validated against its resulting post‑state, pass all pre‑execution validity checks—correct signature, chain ID, nonce, sufficient balance, and intrinsic gas.
- Transactions failing simulation due to inherent invalidity (e.g., nonce mismatch, insufficient balance) do not invalidate the block.

Simulation and verification of the IL is done in the simulation part of block verification.

This approach fits the FOCIL criteria to the current off-chain PBS pipeline without introducing additional stages; the block simulation is simply marginally extended by one transaction for each IL transaction not included in the block. In the case of optimistic relaying that skips the simulation stage for trusted builders, no overhead is incurred.

### Enforcement and Penalties

As per the FOCIL criteria, compliance with the inclusion list is treated as a validity condition. Non-compliance results in non-acceptance at a minimum, and in the case of optimistic builders, a penalty may be enforced.

We propose that the penalty enforced against non-compliant optimistic builders should reflect the IL as an integral validity condition, and lead to forfeiture of the block value against the builder’s collateral. Relays may elect to demote non-compliant builders temporarily, until the error has been traced, to avoid excess collateral burn.

### Future Directions

**Inclusion Lists for Blob-Type Transactions**

In the future, the design may be extended to encompass blobs. This would widen the censorship resistance of the current design while improving timely data availability for L2s.

**Larger Inclusion Lists**

Relay inclusion lists can be larger than proposer-centric inclusion lists, as they are not directly bottlenecked by validator bandwidth constraints. The present design mirrors FOCIL sizing to ensure blocks with relay ILs are competitively priced in the PBS auction, and can in the future be expanded to accommodate a larger total size.

**Multi-Relay Inclusion Lists**

Under the present design, each relay maintains its own inclusion list. Builders seeking to retain maximal optionality for their blocks may choose to send a different block to each relay, reflecting the IL provided by the relay.

In the future, even stronger censorship guarantees may be achieved by forming an inclusion list from the intersection of multiple inclusion lists. This ensures fair competition between relays by enforcing uniform application of the inclusion rule, and can be easily computed over the transaction ranking used to compile the inclusion list. This would also reduce redundancy for builders, by removing the need to compute tailored blocks per relay, or to include a union of inclusion lists.

In such a case, each relay could gossip an extended list, which is then deterministically reduced to a uniform standard-sized list by taking the intersection. In practice, this may be achieved by upgrading relays with a simple gossip protocol.

**Links**

- Fork-Choice enforced Inclusion Lists (FOCIL): A simple committee-based inclusion list proposal
- EIP-7805: Fork-choice enforced Inclusion Lists (FOCIL)
- Uncrowdable Inclusion Lists: The Tension between Chain Neutrality, Preconfirmations and Proposer Commitments
- il-boost/README.md at main · eserilev/il-boost · GitHub

## Replies

**famouswizard** (2025-04-26):

Given that Relay Inclusion Lists aim to enhance Ethereum’s censorship resistance without introducing new trust assumptions, how do you foresee the adoption of rILs impacting competition and differentiation among relays in the proposer-builder ecosystem?

---

**remosm** (2025-04-28):

From the validator POV, relays have so far competed on two axes -

(1) Latency, or block value.

(2) Trust guarantees, or the likelihood of payment.

rILs introduce a third differentiator: verifiable and immediate censorship resistance.

With the initial specs, the latency hit is marginal and predictable, or put another way, rewards should remain effectively unchanged. We also do not introduce new risks for validators, as they are blind to the content of the rIL.

In the short term, relays adopting the design differentiate themselves by providing a strong additional net value add to validators in the form of censorship resistance.

In the medium term, we expect rILs to become a baseline design / table stakes.

---

**aelowsson** (2025-04-29):

Interesting idea. It should be noted that to empower the protocol—through its validators—to enforce censorship resistance, something like FOCIL would still be needed, and that the referenced IL-boost mechanism gives validators a more direct influence. Yet this can be a straightforward way to promote light censorship resistance at the current stage, which of course is welcome. A contradiction to note is that censorship resistance will be imposed by a single party. There may also be risks with the resulting reliance on the mempool specified by the relay. To increase openness, the mempool producing the IL would ideally be made available at the same time that the IL is. This will not prove that the relay operates honestly, but makes it much more difficult not to.

I will in my review seek some clarifications on technical details and outline potential improvements.

![](https://ethresear.ch/user_avatar/ethresear.ch/kubimens/48/18593_2.png) kubimens:

> For each transaction t in the mempool, compute:
>  S_w(t) = \frac{w(t)}{\tilde{w}}, \quad S_f(t) = \frac{f(t)}{\tilde{f}}
> …
> \tilde{w} and \tilde{f} are the medians of the waiting times and priority fees respectively, for all transactions pending in the mempool.
> …
> Normalizing via the median avoids skew from transactions that have not seen inclusion for economical reasons, i.e. due to underpayment. The rule is computationally efficient, as median calculation and transaction sorting can be performed quickly for typical mempool sizes using standard algorithms. An adversary attempting to grief the median by spamming low fee transactions would simply increase the prioritization score of other transactions; a simpler and cheaper way of reaching inclusion would just be to pay more.

I will try to analyze the options to see if I understand your intentions correctly, and to also explain the rationale behind alternative designs.

A benefit of the normalization step is that it produces an “unopinionated” balance between priority fees and delay. It also adjusts according to the state of the mempool. Two examples: if the delay to inclusion increases in the mempool, the importance of the delay is weighted down; if there is a spike in priority fees, the importance of the priority fee is reduced relative to the delay. Normalization can thus be favored if this type of balancing is desirable. However, it would then seem optimal to apply the normalization only to a subset of txs that have some sufficient `max_fee_per_gas`, for example ensuring `max_fee_per_gas * 2 > base_fee_per_gas`. You might even consider `max_fee_per_gas > base_fee_per_gas`. This option has a clear interpretation: if there is space, all txs are with a sufficient `max_fee_per_gas` are included, and otherwise, the selection is still based only on the distribution of such txs.

The thresholding is to make it more difficult for adversaries to alter the balance between delay and priority fee with spam txs. As an example, you can otherwise make the mechanism prioritize priority fee over delay by filling up the mempool with txs with a low `max_fee_per_gas` and a low `max_priority_fee_per_gas`, and let them sit in the mempool accruing delay.

It can be noted that directly computing a score to rank txs by, and including the subset with the highest score, would already be sufficient. It is only really necessary to incorporate a normalization step if you wish to specifically balance the influence of priority fees and delay *according to the present state of the mempool*, when the two variables after normalization are summed. Another way to explain this is to say that normalization is not necessarily required to handle for example a spike in priority fees, given that all txs will be compared with each other (thus a relative operation) anyway in order to select the most relevant for inclusion.

It would therefore as an alternative be perfectly theoretically sound to not normalize, just computing a score from, e.g.,

S(t) = a\,w(t)+f(t)

or

S(t) = (w(t)+a)\times(f(t)+b),

where a and b are weights that can be used to specify a sought balance between delay and priority fee. Setting both a and b to 0 in the second equation then yields

S(t) = w(t) \times f(t).

A doubling of one variable then has exactly the same impact on ranking as a doubling of the other. If a tx provides a 0 priority fee, it cannot be included. This is perfectly reasonable, and, actually, probably desirable. A tx also cannot be included the exact moment it arrives. This may be undesirable, and some weight a can be added to enable direct inclusion, albeit a delay will of course also quickly accrue otherwise. Such an equation would look like this:

S(t) = (w(t)+a)\times(f(t)).

Foregoing normalization has the benefit of making it more difficult for the relay to influence the outcome. This can actually be very important, given the inherently centralized nature of the design.

![](https://ethresear.ch/user_avatar/ethresear.ch/kubimens/48/18593_2.png) kubimens:

> The score S(t) is then size-adjusted to provide higher marginal pricing for large transactions:
>
>
>  D(t) = \frac{S(t)}{size(t)}
>
>
> where size(t) is the transaction’s size measured in bytes. Transactions are then ranked in descending order of D(t).
>
>
> …
>
>
> Ranking the transactions by the density score imposes a higher marginal price per unit of blockspace consumption. This market-based approach incentivizes the inclusion of many smaller transactions, thereby maximizing participation from as many originators as possible. Large transactions, which consume more blockspace, can still be included quickly by increasing their priority fee accordingly.

Here I would also like to understand your argument and the intention behind the step. What are  “small” and “large” transactions? Is it those that consume a lot of gas, or those that have a large raw byte size? Or is the correlation between the two somehow a part of the rationale? For example, it seems to me that ranking by the density score does not actually guarantee

![](https://ethresear.ch/user_avatar/ethresear.ch/kubimens/48/18593_2.png) kubimens:

> …a higher marginal price per unit of blockspace consumption

given that blockspace is measured in gas, not byte size. To achieve a higher marginal price per unit of blockspace consumption, the requirement would be to account for gas g(t) used by the tx, computing the density score as

D(t) = \frac{S(t)}{g(t)}.

It can be clarifying to outline various alternatives, focusing on how the priority fee relates or not relates to byte size:

1. Priority fee per gas – This is a neutral approach w.r.t. the space that the tx occupies in the block—where space is defined by the gas limit. It is simply a ranking by priority fee, since “per gas” is implied. This is used in for example FOCIL with ranked transactions (FOCILR), where a ranking by priority fee (potentially combined with other measures) serves to keep txs in or out.
2. Priority fee per byte – This is a neutral approach w.r.t. the space that the tx occupies in the actual IL—where space is defined by the size limit of the IL. The total priority fee accrued from a tx is then divided by its byte size. This is, e.g., similar to the function that validators would likely prioritize txs by under FOCILR, given that they wish to squeeze out as high rewards as possible from their IL.
3. Priority fee per gas/byte size – This is the approach in this post (accounting also for delay). It will favor txs with small byte sizes (as also indicated). It will also tend to favor txs with low gas consumption, given that gas consumption correlates with byte size.
4. Priority fee per gas/gas used – This is an approach that guarantees a higher marginal price per unit of blockspace consumption. It will favor txs with low gas consumption. It will also tend to favor txs with low byte size, given that gas consumption correlates with byte size.

Is there some specific reason why transactions with small byte sizes are prioritized for censorship resistance? I see the argument of favoring as many originators as possible, but this would in a more targeted way be accomplished by (4) not (3). It can also be argued that the most neutral approach to censorship resistance is to not take an opinionated stance on which txs that should be prioritized for inclusion. Is it perhaps the limit of 8 kb that ultimately motivates (3) over (1) or (4)? This limit is arguably self-imposed and not really a requirement for the relay, given that IL propagation is not design-critical, as opposed to in FOCIL.

![](https://ethresear.ch/user_avatar/ethresear.ch/kubimens/48/18593_2.png) kubimens:

> Block validity is enforced against the FOCIL criteria; specifically, a block proposed to the relay is valid if and only if the following conditions are fulfilled:
>
>
> Transaction Inclusion Check
>
>
> Every transaction listed in the IL provided by the relay is either:
>
> Included explicitly in the block delivered by the builder.
> Verifiably invalid after executing against the block’s resulting post-state.

How will the mechanism handle full blocks? Can the builder ignore the IL if the block is full? It appears from the text as if all highly ranked txs must be included in the block, regardless of if the block is full or not—that is to say, the design imposes the same stronger censorship resistance conditions as imposed by FOCILR. If you are pursuing these stronger censorship resistance properties, it might however be reasonable to apply a [gas threshold](https://ethresear.ch/t/rainbow-roles-incentives-abps-focilr-as/21826#p-53062-h-323-gas-threshold-17) to the IL (and by extension the block). This would encourage more usage of the relay, which could otherwise forego too much value.

![](https://ethresear.ch/user_avatar/ethresear.ch/kubimens/48/18593_2.png) kubimens:

> The present design mirrors FOCIL sizing to ensure blocks with relay ILs are competitively priced in the PBS auction, and can in the future be expanded to accommodate a larger total size.

This makes it even more important to clarify and analyze how the mechanism intends to deal with full blocks, and might make a design favoring (3) above less compelling.

![](https://ethresear.ch/user_avatar/ethresear.ch/kubimens/48/18593_2.png) kubimens:

> In the future, even stronger censorship guarantees may be achieved by forming an inclusion list from the intersection of multiple inclusion lists. This ensures fair competition between relays by enforcing uniform application of the inclusion rule, and can be easily computed over the transaction ranking used to compile the inclusion list. This would also reduce redundancy for builders, by removing the need to compute tailored blocks per relay, or to include a union of inclusion lists.

Relays integrating with builders will then seek to influence the aggregate list to maximize the value that their builder can extract; something to ponder on a bit. It is furthermore not perfectly clear to me that censorship resistance would improve, due to increased collusion concerns.

---

**remosm** (2025-05-02):

Thanks for your thoughtful comment Anders. Will step through the points sequentially:

**Median Normalization**

We have considered a `max_fee_per_gas > base_fee_per_gas` filter and a (post-normalization) multiplicative derivation of S(t).

We have refrained from proposing such a model at this initial point as under EIP‑1559 any transaction whose `max_fee_per_gas` at least meets the `base_fee_per_gas` should, in principle, qualify for inclusion.

Note that this proposal is a first step, and that in the future, such an adjustment could be made, for example, if the priority fee ends up consistently underweight versus the weight time factor, e.g. in a high volatility environment.

Agree that with such thresholding, the normalization would not be strictly required.

**Density adjustment**

We are referring to the raw byte size with regards to the networking constraint, which is a current inclusion list size of <= 8kB.

In practical terms, a scenario to avoid is a single “large” transaction saturating the capacity of the inclusion list.

The lingo here should indeed reflect that the size adjustment specifically refers to the networking constraint rather than a blockspace constraint.

**Handling of full blocks**

The builder should account for the inclusion list when packing the block. A gas threshold is worth exploring!

**Shared inclusion lists**

This reduces to how we can ensure objective application of the inclusion rule. Validators should opt out of relays that consistently diverge from peers. One option here could be a public dashboard tracking the overlap between these.

---

**aelowsson** (2025-05-04):

Thanks, just a few clarifications:

The purpose of applying a threshold like `max_fee_per_gas * n > base_fee_per_gas` with, e.g., `n=2` is to make manipulation of the normalization step more difficult. Without such a threshold, one could submit transactions with a low `max_fee_per_gas` to skew the normalization process, even if those transactions are not intended to be included. The thresholding of the mempool is thus specifically for making the normalization step less arbitrary, and is only necessary under normalization. If txs are directly ranked from an equation such as

![](https://ethresear.ch/user_avatar/ethresear.ch/aelowsson/48/7611_2.png) aelowsson:

> S(t)=(w(t)+a)×(f(t)).

then txs that are not included will not have any influence on which txs that are included. This reduces the opportunities for the relay to manipulate the outcome (albeit, it can still nudge the registration time). The transacting user that did not have its tx included can simply review included txs to confirm that those score higher (at least the score will not depend on non-included txs, while registration time is still not objective).

![](https://ethresear.ch/user_avatar/ethresear.ch/remosm/48/19723_2.png) remosm:

> We are referring to the raw byte size with regards to the networking constraint,

And to be clear, my assumption is that the networking constraint imposed for p2p propagation in FOCIL does not really apply for the relay.

![](https://ethresear.ch/user_avatar/ethresear.ch/remosm/48/19723_2.png) remosm:

> The builder should account for the inclusion list when packing the block. A gas threshold is worth exploring!

Ok, so the inclusion list should be adhered to under full blocks, potentially with a gas threshold. This follows the definition in FOCILR, which differs from FOCIL. In FOCILR, these stronger censorship resistance guarantees are imposed at the protocol level, as opposed to by a single relay. Builders can extract more value when the IL does not constrain which txs it must include. When the harder stance is taken at the protocol level, the proposer cannot avoid them. When the relay takes this harder stance, the proposer has the opportunity to opt out—the option to let the builder control the content of the full block still exists. This will probably have a larger effect on proposer rewards than the latency trade-off discussed in the introduction of the post.

![](https://ethresear.ch/user_avatar/ethresear.ch/remosm/48/19723_2.png) remosm:

> This reduces to how we can ensure objective application of the inclusion rule. Validators should opt out of relays that consistently diverge from peers. One option here could be a public dashboard tracking the overlap between these.

I think the issue is pretty complex given that diverging ILs generally are desirable, and that the dashboard could not reveal collusion between relays. Simply put, IL aggregation in this context seems generally difficult to get right.

---

**mikeneuder** (2025-05-21):

related discussion: [Resistance is ~not~ futile; CR in mev-boost](https://ethresear.ch/t/resistance-is-not-futile-cr-in-mev-boost/16762#relay-constructed-ils-5)

---

**remosm** (2025-05-22):

Thanks for dropping the link, and props for suggesting rILs this early. We were not aware of this previous discussion, it’s great to see.

We think now is a good time to proceed with an implementation.

Specifically, by using the 8 kilobytes constraints from the FOCIL specs as a lean starting point and gas- or bytesize-adjusting the transaction inclusion scores, the impact on proposer earnings should be limited.

Then once several relays run rILs, there is an opportunity to increase the maximum size of the rIL. Multi-relay ILs are also a promising direction to increase censorship resistance and efficiency by enforcing uniform inclusion rule enforcement, and by allowing builders to consider a single rIL only.

Also dropping the recording and slides from the related discussion on the FOCIL Breakout #11:

- Slides
- Recording

---

**mikeneuder** (2025-05-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/remosm/48/19723_2.png) remosm:

> Then once several relays run rILs, there is an opportunity to increase the maximum size of the rIL. Multi-relay ILs are also a promising direction to increase censorship resistance and efficiency by enforcing uniform inclusion rule enforcement, and by allowing builders to consider a single rIL only.

sounds great! super cool that we arrived at the same conclusion ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) hope this is a fruitful implementation and helps pave the way for an in-protocol FOCIL!

