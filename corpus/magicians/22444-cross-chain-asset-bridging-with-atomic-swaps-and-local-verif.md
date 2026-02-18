---
source: magicians
topic_id: 22444
title: Cross-chain Asset Bridging with Atomic Swaps and Local Verification
author: bot_insane
date: "2025-01-07"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/cross-chain-asset-bridging-with-atomic-swaps-and-local-verification/22444
views: 348
likes: 5
posts_count: 6
---

# Cross-chain Asset Bridging with Atomic Swaps and Local Verification

## Preface

For the past three years, as operators of a centralized bridge (Layerswap), we’ve been working hard to find a way to move assets between chains without requiring users to trust a third party. We’ve seen many solutions emerge, but they all rely on third parties to keep things secure, like Validators, DVNs, or Optimistic Oracles. Plus, none of them allow new chains to join freely without permission.

So, we set out to build a new way to bridge assets across chains that meets these key goals:

- Trustless: No need to rely on any new third party for security.
- Permissionless: Any new rollup or chain can join without needing approval.

> This post and the introduced protocol focus solely on transferring assets across chains. It is not related to cross-chain messaging and does not require such mechanisms to function.

## Intents, Solvers, and Atomic Swaps

Let’s set the stage. We have a user with an intent and a solver who is ready to fulfill that intent. To enable these two parties to exchange their assets across different chains, we need a trustless system. This concept has already been introduced with Atomic Swaps. I won’t go too deep into explaining Atomic Swaps, assuming a general knowledge of them, but I will introduce a slightly modified version called PreHTLC.

1. User Commit
 The user creates a PreHTLC (essentially the same as an HTLC, but without a hashlock) on the origin chain, committing funds for the selected solver.
2. Solver Lock
 The solver detects this transaction, generates a random secret (S), calculates HASH(S) hashlock and creates an HTLC, locking funds (minus the solver fee) for the user on the destination chain.
3. User AddLock
 The user observes the transaction on the destination chain, retrieves the hashlock, and converts their PreHTLC to an HTLC on the source chain. The PreHTLC can only be converted once with a single hashlock; no other information can be altered.
4. Unlocks
 Upon seeing this conversion, the solver reveals the secret (S) on the destination chain to release the user’s funds and then reveals the secret (S) on the source chain to claim their funds.

There are multiple reasons why we decided to go with this design. There’s a lot to discuss, but I would like to focus right now on the third step. The user is inside the dApp and detects the destination transaction via wallet RPC. This is essentially the exact point where verification happens. The user verifies this transaction, and it doesn’t introduce any trust assumptions. The user verifies it and takes responsibility. Is this enough?

## Local Verification (e.g. Light Client)

Not really. To safeguard the user, an ideal solution would be to run a light client of the destination chain inside the dApp, like [Helios](https://github.com/a16z/helios). The dApp would run a light client of the destination chain and verify that the `hashlock` retrieved from the destination chain is actually on the chain, after which the user can proceed to the next steps. If there is no Light Client implemented for the destination network (there should be), you can get the `hashlock` from multiple RPC endpoints, dramatically reducing the risk of compromised data from RPCs.

## Any Chain or Rollup Can Join

Now, the `PreHTLC` contracts are immutable, chain-agnostic, and around [200-300 lines of Solidity code](https://github.com/TrainProtocol/contracts/blob/main/chains/evm/solidity/contracts/Train.sol). They can be implemented in [any VM](https://github.com/TrainProtocol/contracts/tree/main/chains) and do not need any modification when new chains are added. They are end-to-end immutable. Therefore, what is necessary for any new chain to be added to this protocol? It’s as simple as deploying a `PreHTLC` contract to a new chain and running a solver. No committees, no approvals, no voting—just these two things, and anyone can have their intent solved.

## Underwater Stones & Conclusion

There are many hidden challenges, most of which we have explored and found solutions for—though not perfect yet. We believe this foundation is the right way to go. It ensures trustless exchanges for users and solvers and guarantees permissionless onboarding for new rollups or chains. We have [detailed documentation](https://docs.train.tech) available that covers how to ensure solver liveness, discovery, and the auction system.

We believe this solution will finally solve asset bridging for all chains and rollups. I am happy to discuss any ideas, questions, or concerns. Which parts need more clarification? Are we missing something?

## Replies

**leonafrica** (2025-02-24):

Hey [@bot_insane](/u/bot_insane)

I have a few questions and points of clarification I’d love for you to expand on:

1. How does PreHTLC compare to Axelar in terms of efficiency, speed, and transaction security?
Axelar leverages a validator network to facilitate cross-chain transfers, ensuring transactions are executed securely and efficiently without requiring user intervention. PreHTLC, on the other hand, relies on user-side verification and light clients.
2. Wouldn’t Axelar provide faster execution since it doesn’t require users to monitor transactions manually?
3. How does PreHTLC handle transaction protection and finality compared to Axelar’s security model?
Specifically, how does it mitigate risks like rollback attacks or malicious activity in cases where users must verify transactions themselves?
4. Are there scenarios where PreHTLC is actually more secure or efficient than Axelar’s validator-based approach?

Thanks for sharing this idea—looking forward to your response!

---

**bot_insane** (2025-03-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/leonafrica/48/14472_2.png) leonafrica:

> How does PreHTLC compare to Axelar in terms of efficiency, speed, and transaction security?
> Axelar leverages a validator network to facilitate cross-chain transfers, ensuring transactions are executed securely and efficiently without requiring user intervention. PreHTLC, on the other hand, relies on user-side verification and light clients.
> Wouldn’t Axelar provide faster execution since it doesn’t require users to monitor transactions manually?
> How does PreHTLC handle transaction protection and finality compared to Axelar’s security model?
> Specifically, how does it mitigate risks like rollback attacks or malicious activity in cases where users must verify transactions themselves?
> Are there scenarios where PreHTLC is actually more secure or efficient than Axelar’s validator-based approach?

- PreHTLCs with local verification completely eliminate the need to rely on third-party security. The entire verification process is conducted within the dApp, ensuring a trustless exchange. In contrast, other approaches require trust in “validators,” “oracles,” and similar intermediaries. The swap takes under <30 seconds.
- Transactions are not monitored manually; they are automatically monitored within the dApp.

---

**hellohanchen** (2025-03-17):

Could you please provide more details about what happen if the process if broken (e.g. user or solver do something wrong).

And how do we handle the finality latency of different chains?

---

**bot_insane** (2025-03-17):

There are basically four types of failure/misbehavior:

### Solver Fails to Act on the User’s Commitment/Intent

In a rare scenario where the winning Solver fails to act on the User’s commitment, other auction participants have a chance to lock instead of the winner. If all participants fail to act, the User only needs to wait for the timelock period (usually ~15 minutes) to receive their funds back.

### User Fails to Act on the Solver’s Lock

If the User does not act on the lock created by the Solver, both parties can refund their funds after the timelock period expires.

### Solver Fails to Release the User’s Funds

In scenarios where the Solver releases their funds but fails to release the User’s funds, the User can capture the secret used to release the Solver’s funds. The User can then use this secret to manually release their own funds on the destination chain.

### Solver Fails to Release Any Funds

If the Solver fails to release any funds, the User can wait for the timelock period to expire and then refund their funds.

A detailed explanation and diagram for each type are [documented here](https://docs.train.tech/protocol-spec/edge-cases#solver-fails-to-release-any-funds).

Finality is handled by both the user and the solver. The solver locks/releases funds when it considers the transaction final. A risky solver can do this quickly, providing faster transaction times, while a conservative solver can wait as long as needed. The same applies to the user.

---

**bot_insane** (2025-04-09):

A quick update on this idea: we were able to implement the core functionality, pass the security audits, and deploy it to mainnets.

You can now try it live at https://app.train.tech.

Additionally, all the code—including the dApp, contracts, and most importantly, the Solver—is open source and available [here](https://github.com/TrainProtocol/solver).

If you have any questions or feedback, we’d be happy to discuss!

