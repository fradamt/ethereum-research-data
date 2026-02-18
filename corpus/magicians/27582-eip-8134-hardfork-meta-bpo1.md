---
source: magicians
topic_id: 27582
title: "EIP-8134: Hardfork Meta - BPO1"
author: poojaranjan
date: "2026-01-25"
category: EIPs > EIPs Meta
tags: []
url: https://ethereum-magicians.org/t/eip-8134-hardfork-meta-bpo1/27582
views: 68
likes: 3
posts_count: 5
---

# EIP-8134: Hardfork Meta - BPO1

Discussion Topic for **Hardfork Meta - BPO1**  upgrade.

This EIP-xxxx captures its activation time, blob parameter changes, canonical configuration and historical references.

Blob-Parameter-Only (BPO) upgrades are *parameter-only network upgrades* (similar in nature to Ice Age forks) and have started deploying independently following the Fusaka upgrade.

While [EIP-7892](https://eips.ethereum.org/EIPS/eip-7892) defines the mechanism for scaling Ethereum’s blob capacity, there is currently no EIP that documents what changed in each BPO instance, when it was activated, and which parameter values were applied. Today, this information is fragmented across client repositories, HackMDs, coordination notes, and release artifacts.

This Meta EIP aims to provide a lightweight, durable reference for:

- Activation timing
- Blob target and blob maximum changes
- Base fee update parameters
- Historical context and data sources

PR: [Hardfork Meta to document BPO1 by poojaranjan · Pull Request #11164 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/11164)

Feedback is very welcome, particularly on:

- Whether this should evolve into a single living registry versus one Meta EIP per BPO
- Field completeness and structure
- Preferred identifier format (BPO1 vs BPO-1 vs BPO 1)

Appreciate any review, comments, or suggestions. ![:folded_hands:](https://ethereum-magicians.org/images/emoji/twitter/folded_hands.png?v=15)

## Replies

**abcoathup** (2026-01-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/poojaranjan/48/1514_2.png) poojaranjan:

> Whether this should evolve into a single living registry versus one Meta EIP per BPO

Each BPO should be represented as a Meta EIP, to easily document the timing and parameters a BPO uses.  We should avoid living registries that need to be maintained.

Creating a Meta EIP is fairly lightweight, and previous BPOs can be used as a template, with only the parameters changing.  I’d suggest creating BPO3.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/poojaranjan/48/1514_2.png) poojaranjan:

> Preferred identifier format (BPO1 vs BPO-1 vs BPO 1)

ethPandaOps The Lab uses with a space, i.e. BPO 1.  [The Lab by ethPandaOps](https://lab.ethpandaops.io/ethereum/forks/bpo1)

Whilst my preference is without a space, i.e. BPO1, which is what I use for Ethereal news (e.g. [Ethereal news weekly #2 | Ethereal news](https://ethereal.news/ethereal-news-weekly-2/) following the example of [Week in Ethereum News](https://weekinethereumnews.com) of using minimal additional characters), I would be led by ethPandaOps here.

---

**poojaranjan** (2026-01-27):

[@abcoathup](/u/abcoathup)

Thank you for the thoughtful review and for sharing your suggestion. I really appreciate you taking the time to look through this.

I also checked with the **ethPandaOps team**, and they indicated they do not have a strong preference either way. Given that, aligning with the existing specification feels like the most consistent path forward.

Thus, I’d keep the proposal as-is. As defined in [EIP-7892](https://eips.ethereum.org/EIPS/eip-7892)

> BPO forks SHOULD be named using the convention bpo, where  starts at 1.

Aligning with the naming standard specified in the “required” EIP helps ensure consistency and clarity across client implementations, documentation, and ecosystem tooling.

That said, thank you again; your feedback is very much appreciated.

---

**jochem-brouwer** (2026-01-29):

I don’t think we should add hardfork meta’s for these BPO forks. These are part of the spec: https://eips.ethereum.org/EIPS/eip-7892

Configuration-wise the only changes are the activation timestamp and the relevant parameters (max and target blobs, and the fee fraction constant). So although these are technically forks one could also think of these as updated configurations.

As an alternative which I would support more would be a living document with all BPO forks.

I fear if we add all these meta EIPs for BPOs, and if there are say 9 of these in the future, then the meta EIP section will look only like BPO forks (which are not super interesting from the changes necessary per client (a few constants) - of course, increasing blob capacity requires a lot of engineering ![:smiley:](https://ethereum-magicians.org/images/emoji/twitter/smiley.png?v=15) ) and I think most users will think that those are somewhat annoying and should not be there (or grouped under BPO forks, or thus in a separate EIP which documents all BPO forks)

---

**poojaranjan** (2026-01-29):

Thanks [@jochem-brouwer](/u/jochem-brouwer) for your review and thoughtful comments & suggestions.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> Configuration-wise the only changes are the activation timestamp and the relevant parameters (max and target blobs, and the fee fraction constant). So although these are technically forks one could also think of these as updated configurations.

My reasoning for having a separate Meta EIP per upgrade is more influenced by precedent, particularly the Ice Age–related forks such as **Muir Glacier, Arrow Glacier, and Gray Glacier**. These were parameter-only upgrades, yet each was documented with its own Meta EIP.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> I fear if we add all these meta EIPs for BPOs, and if there are say 9 of these in the future, then the meta EIP section will look only like BPO forks (which are not super interesting from the changes necessary per client (a few constants) - of course, increasing blob capacity requires a lot of engineering  ) and I think most users will think that those are somewhat annoying and should not be there (or grouped under BPO forks, or thus in a separate EIP which documents all BPO forks)

BPO has only recently been introduced, and developers are understandably being cautious, adjusting parameters according to a defined formula. While BPO-style upgrades provide flexibility to modify parameters as needed, I expect the system to stabilize over time, which may naturally lead to less frequent upgrades in the future (i.e., not necessarily having many BPO Meta EIPs each year).

Additionally, the parameter changes are not strictly unidirectional; the same flexibility allows values to be reduced if and when required. Given this, I see value in recording each change in a separate file, ideally with accompanying rationale, to preserve clarity, traceability, and historical context.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> As an alternative which I would support more would be a living document with all BPO forks.

I did consider the alternative of maintaining a single **Living Meta EIP** and appending a new row for each upgrade. However, historically, EIP editors have been cautious about using EIPs as living registries. That said, I would be open to this approach if there is broad agreement among the editors.

