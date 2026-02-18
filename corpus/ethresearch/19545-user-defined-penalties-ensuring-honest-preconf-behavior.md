---
source: ethresearch
topic_id: 19545
title: "User-Defined Penalties: Ensuring Honest Preconf Behavior"
author: jonahb27
date: "2024-05-13"
category: Economics
tags: [mev, preconfirmations, based-sequencing, sequencing]
url: https://ethresear.ch/t/user-defined-penalties-ensuring-honest-preconf-behavior/19545
views: 4376
likes: 7
posts_count: 7
---

# User-Defined Penalties: Ensuring Honest Preconf Behavior

*Thank you [Justin Drake](https://twitter.com/drakefjustin) and [Ryan Sproule](https://twitter.com/sproule_) for the help.*

**tl;dr:** *Allow users to specify their preferred penalty when requesting a preconf, enabling the market to naturally establish preconf cryptoeconomic security parameters, rather than setting parameters upfront.*

As the community settles on a design for preconfs, a critical choice arises: how can we ensure crypto-economic security for preconfs? Specifically, what incentives exist to prevent safety or liveness faults? I’ll present a high-level overview of the current solutions before proposing an alternative.

Here are the current mechanisms (they can be used in combination):

1. Basic Slashing: If a proposer is responsible for a safety or liveness fault, they are slashed.

Open Question: How much should be slashed, and what amount of stake should the proposer put up?
2. Freezing: The proposer’s stake is frozen, causing them to lose the time value of their money.

Justin Drake suggested during the Ethereum sequencing call #7 that this approach could help ease the adoption of the preconf protocol since preconfs introduce new behaviors the market needs to adjust to.
3. Open Question: How much stake should be frozen, and for how long?
4. Dynamic Reputation Slashing: Each fault by a validator results in a progressively stricter penalty; for instance, they might be slashed more or locked up longer.

Open Question: What should the penalty curve look like? Should it be time-based and reset after a period of honest behavior?
5. Insurance: Proposers must compensate users whose preconfs fail due to faults. Effectively, users’ preconfs are insured.

Open Question: How much insurance should be offered?

All these mechanisms require us to know ex ante what preconf users want. Inevitably, this will be opinionated and lead to deadweight loss, as some users who might want a preconf could feel uncomfortable with the setup. Moreover, some proposers might feel uncomfortable with the parameterization and choose not to offer preconfs. The best solution is to allow users to work with proposers to agree on the appropriate level of crypto-economic security.

My Solution: **User-Defined Penalties**

Users should be able to specify their desired level of crypto-economic security by attaching a penalty structure to their preconf. This structure will detail the consequences of a fault.

For instance:

```rust
// Here, users can define a penalty associated with any specific fault,
// and the system is generic enough to allow for arbitrarily complex rules.
struct PreconfAgreement {
    faults: Vec>,
}

struct Fault {
    condition: C,
    penalties: Vec,
}

trait Condition {
    fn should_penalize(...) -> bool;
}

trait Penalize {
    fn penalize(...);
}
```

*Note: There is a DoS vector associated with unbounded compute when evaluating conditions. Some gas metering should be used, or conditions should be constructed as succinct statements (e.g., a SNARK).*

This solution is unbiased and allows the market to determine the appropriate parameters naturally. Users can decide the level of security they want rather than leaving it up to the protocol to estimate, while proposers can choose their risk-reward profile. Heavier penalties will likely result in higher costs for users.

**Complexity Concerns:**

- Proposers’ Perspective: With preconfs, we already assume that proposers (or their gateways) are sophisticated, and giving them the ability to manage their own risk profiles should benefit them. Inexperienced proposers can set a simple threshold for the maximum penalty they are willing to incur and, as they gain experience, adjust it more systematically.
- Users’ Perspective: This approach shouldn’t add complexity, as wallets can easily abstract the penalty decision, much like they abstract gas fee choices. Fine-grained choices can be offered as an opt-in feature for more advanced users.

## Replies

**SK0M0R0H** (2024-05-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/jonahb27/48/14890_2.png) jonahb27:

> allow for arbitrarily complex rules

Does it create potential “attacks” on proposers? Here, by “attacks,” I mean risks that the proposer is not ready to accept. For arbitrarily complex rules, you need a complex decision-making process.

Or am I missing something?

---

**jonahb27** (2024-05-14):

You’re definitely right. Allowing arbitrarily complex rules introduces potential attack vectors for unsophisticated proposers (and can add latency).

The advantage of complex logic is the ability to express more nuanced penalties. For example, a user might specify a fault condition if a swap preconf results in slippage exceeding a threshold. That said, mixing faults and fulfillment preferences at the penalty layer can add unnecessary complexity and vulnerabilities. For simplicity and security, a more constrained approach could be more practical.

Arguably, we should constrain the PreconfAgreement space to only safety and liveness faults, avoiding arbitrary fault types. For penalties, we can offer a few predefined, tunable options: slashing a specified amount of ETH, freezing ETH for a certain period, providing insurance, or a combination of these penalties. This approach balances flexibility, simplicity, and safety, making the system easier to manage while still allowing users to specify meaningful penalties.

---

**imkharn** (2024-05-21):

Each user has a different value for their preconf and it seems clear that there is no other way to get that valuation info from the market other than to ask. So, logically isn’t this the *only* solution to this problem? At least the only solution that has market determined expenses.

---

**0xTariz** (2024-05-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/jonahb27/48/14890_2.png) jonahb27:

> proposers can choose their risk-reward profile.

Can you explain what is meant?

My understanding: a proposer can choose which slashing mechanisms(preconf penalty structure) to attach to themselves and make this public in their profile. Users then request a preconf from a proposer who has the preconf penalty structure they want in their profile.

Is this correct?

---

**jonahb27** (2024-05-28):

I agree that this will allow for the most optimal market to form, but to play devil’s advocate against my proposal, it introduces a lot of complexity. The opposite extreme would be to mirror the existing ETH protocol and establish a minimum stake amount with fixed penalty and slashing rules. This tradeoff would reduce complexity at the expense of expressivity. A middle ground would be to create a few categories of preconfs (e.g. strict, not strict, and loose) with each type having a different preset penalties.

---

**jonahb27** (2024-05-28):

Thank you for your question.

The idea is that users, not proposers, specify the penalties associated with a preconf. Essentially, users create a kind of “contract” where they outline their requirements for including a transaction in a block, the amount they are willing to pay, and the penalties the proposer will face if they fail to meet these requirements.

When I mentioned that “proposers can choose their risk-reward profile,” I meant that proposers are not obligated to accept every preconf request. Instead, they review the terms set by the users and decide if the rewards outweigh the risks. This involves evaluating the opportunity cost of accepting the preconf and the risk of incurring the specified penalties if they fail to meet the preconf conditions, and judging this against the user’s payment for the preconf.

Note that the heavier the penalties, the larger the accepting risks, meaning that a higher payment for accepting is necessary. In this market structure, some proposers might choose to communicate their preferred penalty structures and prices.

Does this answer your question?

