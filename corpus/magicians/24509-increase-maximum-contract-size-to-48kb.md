---
source: magicians
topic_id: 24509
title: Increase Maximum Contract Size to 48KB
author: Giulio2002
date: "2025-06-10"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/increase-maximum-contract-size-to-48kb/24509
views: 385
likes: 14
posts_count: 13
---

# Increase Maximum Contract Size to 48KB

The current 24KB contract size limit can be restrictive for complex contracts and applications. Increasing the limit to 48KB allows for more feature-rich contracts while maintaining reasonable constraints on block and state growth.

## Replies

**Ankita.eth** (2025-06-10):

Hi [@Giulio2002](/u/giulio2002),

I’m interested in the proposal to increase the maximum contract size from 24KB to 48KB, as it could enable more complex and feature-rich smart contracts. However, I’d like to better understand how this change balances the benefits for developers with potential impacts on network performance and security. Could you clarify the following points?

- Gas Metering Adjustments: The current 24KB limit (EIP-170) was set to prevent DoS attacks due to the O(n) costs of loading large contracts (e.g., disk reads, JUMPDEST analysis, Merkle proof sizes). Would the proposed 48KB limit rely solely on the existing gas metering from EIP-3860 (2 gas per 32-byte chunk), or are additional gas cost adjustments planned to account for the increased contract size?
- Impact on Node Performance: Doubling the contract size could increase the resource demands on nodes (e.g., disk I/O, memory usage). Has there been any benchmarking or analysis to ensure that a 48KB limit won’t strain full nodes or light clients, especially as block gas limits continue to evolve?
- Backward Compatibility: The proposal mentions enabling more complex contracts, but how will it ensure backward compatibility with existing contracts and tools (e.g., Etherscan, block explorers) that rely on the 24KB limit? Could this introduce new challenges for contract verification or debugging?
- EOF Contracts Consideration: With EIP-7830 proposing a 64KB limit for EOF contracts (due to simplified JUMPDEST analysis), how does the 48KB limit align with or complement EOF’s approach? Would a unified limit (e.g., 64KB for both legacy and EOF contracts) be more consistent for developers?

I think increasing the contract size limit is a promising idea to support richer dApps, but I’d love to hear more about how it mitigates the risks that originally justified the 24KB cap.

---

**aryaethn** (2025-06-11):

Hi [@Giulio2002](/u/giulio2002),

Isn’t [EIP-7907](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-7907.md) trying to do what you are proposing?

---

**wjmelements** (2025-06-11):

I think it should be a power of 2, like 64k

---

**Giulio2002** (2025-06-18):

Update: it will be `32KiB`

---

**cupOJoseph** (2026-01-16):

If EIP-7907 is too complex, then this is a great step. I strongly support including this in Glamsterdam.

A moderate increase now is better than spending years trying to perfect/optimize for an infinite or massive increase that grows with the gas limit, given the technical constraints.

---

**owen** (2026-01-16):

Agreed, I’ll take a moderate improvement over nothing.

In general increasing the size helps reduce gas for extcalls and helps reduce some of the more idiosyncratic ways of splitting up code just to get around it (which imo are often more bug-prone).

Obviously would prefer if we could get it to a clean 48kb–a 2x in size probably helps eliminate the majority of limits that people bump into today, but I’ll take whatever we can reasonably get.

---

**devops199fan** (2026-01-16):

+1 to [@cupOJoseph](/u/cupojoseph) and [@owen](/u/owen)‘s comments - this is definitely an improvement!

---

**cupOJoseph** (2026-01-16):

Here’s a short presentation with an overview of current contract size limit discussions and reasoning too:

[![Screenshot 2026-01-16 at 7.53.29 PM](https://ethereum-magicians.org/uploads/default/optimized/3X/e/2/e223f5fbd6c4222920af961acc07dd631a74c514_2_690x353.png)Screenshot 2026-01-16 at 7.53.29 PM1962×1004 93.4 KB](https://ethereum-magicians.org/uploads/default/e223f5fbd6c4222920af961acc07dd631a74c514)



      [docs.google.com](https://docs.google.com/presentation/d/1ixrOssk2QqB_jb1OzodnvUCxA0FDcN-vtF56GVYmb1k/edit?usp=sharing)



    https://docs.google.com/presentation/d/1ixrOssk2QqB_jb1OzodnvUCxA0FDcN-vtF56GVYmb1k/edit?usp=sharing

###

Increase the contract size limit With @cupojoseph










Long term we should aim for higher.

---

**Giulio2002** (2026-01-16):

Hey, do you plan on proposing it to ACDE? If so, I suggest putting it on the next ACDE agenda and joining. I can champion this again if there is interest

---

**Helkomine** (2026-01-17):

I think we should do the opposite: Reduce the maximum contract size for EVM Legacy on a schedule (or at least keep it at its current size) while increasing for EOF. This way, we will gradually phase out EVM Legacy more effectively at the protocol level, thereby paving the way for EOF.

---

**Giulio2002** (2026-01-17):

Update: without my own realization, this was CFIed for Glamsterdam.

---

**CPerezz** (2026-01-21):

Yes. I did the whole research for the viability of this and presented it in ACD. Not really arguing for your EIP (as 64kB is totally viable). But definitely arguing against any repricing that is unneeded for these sizes (EIP-7907).

More on the topic here: https://ethresear.ch/t/data-driven-analysis-on-eip-7907/23850

