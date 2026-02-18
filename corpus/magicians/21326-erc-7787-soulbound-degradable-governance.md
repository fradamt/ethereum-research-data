---
source: magicians
topic_id: 21326
title: "ERC-7787: Soulbound Degradable Governance"
author: ownerlessinc
date: "2024-10-10"
category: ERCs
tags: [erc, nft, governance, dao]
url: https://ethereum-magicians.org/t/erc-7787-soulbound-degradable-governance/21326
views: 110
likes: 0
posts_count: 1
---

# ERC-7787: Soulbound Degradable Governance

https://github.com/ethereum/ERCs/pull/674

I’d like to introduce **Valocracy**, a governance system for DAOs that seeks to fundamentally separate economic power from political power. Traditionally, DAOs have operated under the assumption that more tokens equals more power, leading to governance that can be driven by wealth rather than merit. Valocracy proposes a new approach: **tokens ≠ power**, with governance based on contributions and merit rather than pure token ownership.

### The Standard Proposal: Soulbound Degradable Governance (SDG)

Valocracy is the name of a system that uses the **Soulbound Degradable Governance (SDG)**, a system where political power is represented as a quantifiable amount, which degrades over time if no further political power is earned. This political power isn’t transferable and can’t be bought or sold—it’s earned through merit and participation.

Here’s how it works:

- When a member of a DAO successfully completes a task proposed by the DAO, they receive political power, represented as a non-transferable NFT.
- If they don’t receive additional power over a certain period (let’s say 90 days), the political power they’ve accumulated will gradually degrade.
- If too much time passes without further contributions, the NFT loses all its value, effectively removing the individual’s political power from the system.

This creates a dynamic system where political power must be continuously earned and reinforced through actions and contributions, preventing long-term dominance by any single party.

### Measuring Merit Through Community Engagement

Political power in Valocracy is earned by fulfilling pre-proposed tasks that the DAO votes on. Upon completion of these tasks, DAO members vote to determine if the task has been successfully completed. The decision is merit-based, and the voting power of the DAO’s members is used to decide whether additional political power should be granted.

This keeps the governance model aligned with the DAO’s values, ensuring that contributors are continuously evaluated by the community, and power is distributed based on merit rather than wealth.

### Transparency and Self-Regulation

One of the key principles of Valocracy is **transparency**. While the system provides tools for merit-based governance, it is ultimately up to each DAO to regulate itself. DAOs that maintain transparency and prioritize the well-being of the organization will naturally flourish, while those that become corrupt or allow bad actors to dominate will eventually self-destruct. The open, community-driven nature of the system provides a natural check and balance.

### A Game Master Approach for Early-Stage Governance

To ensure a smooth start, I’ve considered a **Game Master** approach where the protocol creator or DAO founder has slightly more political power initially, similar to token minting. This gives the founding members the ability to guide the early stages of the DAO while gradually decentralizing over time. Importantly, this power distribution isn’t imposed, but provided as a tool for the DAO to decide how to implement.

### Flexibility and Decentralization

One of the key aspects of Valocracy is that it provides **the tools, not the rules**. Each DAO can customize how SDG is implemented—deciding on the rate of degradation, voting mechanisms, and how power is distributed. This flexibility empowers DAOs to tailor governance to their specific needs, while still maintaining the core principle of merit-based power distribution.

---

You can read more about Valocracy [here](https://valocracy.xyz/en/read-the-manifesto).
