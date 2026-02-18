---
source: magicians
topic_id: 27306
title: "ERC-8113: Series Accounting for Incentivized Vaults"
author: 0xpanicError
date: "2025-12-24"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-8113-series-accounting-for-incentivized-vaults/27306
views: 217
likes: 2
posts_count: 9
---

# ERC-8113: Series Accounting for Incentivized Vaults

The following standard formalizes the [Series Accounting](https://www.ssctech.com/blog/understanding-performance-fees-in-hedge-funds-series-vs-equalization) Method for ERC-7540 type vaults, enabling them to collect performance fees on yields without introducing a [free-ride](https://www.investopedia.com/terms/f/free_rider_problem.asp) problem.

Current ERC-7540 vault implementations typically implement a Highwater Mark based on the highest recorded price-per-share (the ratio of total assets to total shares of the vault) to ensure performance fees are not collected for recovering losses. But relying on a single vault-wide highwater mark introduces a free-ride problem.

A free-ride occurs when a user’s deposit is claimed at a price-per-share below the vault’s current highwater mark. When the vault later reaches a new highwater mark, the user doesn’t pay a performance fee on all yield accrued between their initial entry price and the new highwater mark, effectively diminishing returns for existing users.

This standard implements the series accounting method where all batches of deposit requests are claimed in a series which maintains a unique highwater mark for those deposits. This allows for the protocol to accurately account for performance fees across all user deposits fairly.

Check out the full proposal here: [ERC-8113: Series Accounting for Incentivized Vaults](https://eips.ethereum.org/EIPS/eip-8113)

## Replies

**Ankita.eth** (2025-12-25):

This proposal addresses a real accounting issue that shows up in ERC-7540 style vaults once deposits are settled asynchronously and performance fees are involved.

**What this standard gets right**

- Fixes the free-ride problem
A single vault-wide high-water mark assumes all users entered at similar prices, which breaks down when deposits are claimed at different exchange rates. Series-level accounting avoids newer deposits benefiting from recoveries they didn’t participate in.
- Series as deposit cohorts makes sense
Treating each claimed batch as its own accounting unit closely mirrors traditional fund accounting and maps well to how ERC-7540 request settlement already works.
- Reverting ERC-4626 conversion helpers is the honest choice
When shares are non-fungible across series, exposing a single totalAssets or conversion rate would be misleading. Forcing integrators to handle this explicitly is better than leaking incorrect abstractions.
- Asset-based redemption is the right abstraction
Once users can hold positions across multiple series, shares stop being a meaningful request unit. Redeeming by assets avoids pushing internal accounting complexity onto users.

**Points implementations should be careful about**

- Consolidation timing and fee finalisation
Merging series once a new high-water mark is reached is necessary for gas and reporting, but the exact trigger conditions matter. Edge cases around partial recoveries or fee timing need to be handled very carefully.

Overall, the added complexity feels justified for incentivised ERC-7540 vaults, especially those tracking RWAs or discretely priced strategies. This is not free complexity — it’s complexity that already exists, now made explicit and fair.

---

**0xpanicError** (2025-12-25):

Thanks for the reply!

Yes you’re right about the consolidation logic. In the proposal and reference implementation, I suggest consolidation logic can be to merge all outstanding series when the lead series reaches a new highwater mark. This was a design decision to try to keep complexities at a minimum.

But individual implementation can also for partial consolidations as well where outstanding series consolidate into each other instead of the lead if they are in sync with each other but not the lead yet. Although this must be done more carefully as it leads to more edge cases and has a greater surface for attack vectors.

For context, the reference implementation is also audited by Sherlock and thouroughly tested with integration and fuzz tests. You can find the report [here](https://github.com/AlephFi/smart-contracts/blob/bac9163538afb2d024bb91b25d4a14aa16d18e48/audits/15-10-2025_Sherlock_Aleph_v1.pdf).

---

**Ankita.eth** (2025-12-25):

Thanks for the clarification — that makes sense.

Consolidating outstanding series only when the lead series reaches a new high-water mark feels like a reasonable default to keep both state complexity and attack surface under control. I agree that partial or peer-to-peer consolidation between non-lead series can quickly introduce edge cases, especially around fee realisation and ordering.

It’s also good to know the reference implementation has gone through a Sherlock audit and extensive fuzzing — that adds confidence around the baseline design.

One follow-up from an implementer’s perspective:>

- Do you see value in standardising consolidation policies (not just mechanics) in a future extension?
For example, explicitly defining when partial consolidation is safe vs discouraged could help teams avoid diverging designs that reintroduce risk while still allowing flexibility.

Overall, the choice to keep the default consolidation path simple feels pragmatic, especially for early adopters of ERC-7540-style vaults.

---

**0xpanicError** (2025-12-26):

I think consolidation policies can be left an open design space for individual protocols. I was given an advice from other ERC authors to not over specify a standard as it makes it too opinionated and can make the standard restrictive for applications.

---

**SamWilsn** (2026-01-22):

> ERC-8113 vaults must override the ERC-4626 specification as follows:
> totalAssets MUST revert for all callers and inputs
> convertToShares MUST revert for all callers and inputs
> convertToAssets MUST revert for all callers and inputs

If you’re making this substantial of a change to an interface, you probably shouldn’t claim compatibility with it. To put it in computer science-y terms, these requirements violate the **Liskov substitution principle**. Software integrating with ERC-4626 vaults would very likely break if given an ERC-8113 vault.

---

**0xpanicError** (2026-01-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Liskov substitution principle

Thanks for pointing this out. While writing this ERC I was taking inspiration from ERC-7540, and was trying to maintain backwards compatibility with it. ERC-7540 itself maintain a backwards compatibility with ERC-4626 with the same method:

> All ERC-7540 asynchronous tokenized Vaults MUST implement ERC-4626 with overrides for certain behavior described below.
>
>
> Asynchronous deposit Vaults MUST override the ERC-4626 specification as follows:
>
>
> The deposit and mint methods do not transfer assets to the Vault, because this already happened on requestDeposit.
> previewDeposit and previewMint MUST revert for all callers and inputs.
>
>
> Asynchronous redeem Vaults MUST override the ERC-4626 specification as follows:
>
>
> The redeem and withdraw methods do not transfer shares to the Vault, because this already happened on requestRedeem.
> The owner field of redeem and withdraw SHOULD be renamed to controller, and the controller MUST be msg.sender unless the controller has approved the msg.sender as an operator.
> previewRedeem and previewWithdraw MUST revert for all callers and inputs.

Would you recommend I should follow the same pattern (I agree that overriding so many methods to maintain backwards compatibility doesn’t seem very helpful practically) or just remove the need for backwards compatibility with ERC-4626 and/or ERC-7540?

For more context, while ERC-4626 is very widely used, the concept of ERC-7540 is getting just as popular but I have seen zero implementations in production that exactly match that spec. Protocols implement async 4626 vaults in their own ways. Perhaps it could be because of the over specification of ERC-7540 and hence it’s better to not try to maintain backwards compatibility to a standard which not really used in production anywhere?

Relevant discussion: [EIP-7540: Asynchronous ERC-4626 Tokenized Vaults - #25 by nikollamalic](https://ethereum-magicians.org/t/eip-7540-asynchronous-erc-4626-tokenized-vaults/16153/25)

---

**SamWilsn** (2026-01-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/0xpanicerror/48/16212_2.png) 0xpanicError:

> overriding so many methods to maintain backwards compatibility

You’re breaking backwards compatibility either way.

What you need to do is choose between pretending you’re compatible or not.

Unfortunately I’m not the person you need to talk to help make the decision. I’m not really in the DeFi ecosystem, so I have no idea what the right approach is.

---

**0xpanicError** (2026-01-23):

Based on what I’m seeing, I don’t think there’s a need to extend 7540 spec or maintain backwards compatibility with 4626. Teams that will use this spec will work heavily with TradFi partners and they probably won’t care about maintaining some spec in some ERC, so I want 8113 to be specifically focused about Series Accounting. I’ll make the changes in PR to remove compatibility from 7540 and 4626.

