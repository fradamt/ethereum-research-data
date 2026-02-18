---
source: ethresearch
topic_id: 21638
title: "Canonical cross-chain swap: fast and decentralized settlement for cross-chain swap using canonical/native L1->L2 messaging"
author: suahnkim
date: "2025-01-30"
category: Layer 2
tags: []
url: https://ethresear.ch/t/canonical-cross-chain-swap-fast-and-decentralized-settlement-for-cross-chain-swap-using-canonical-native-l1-l2-messaging/21638
views: 475
likes: 8
posts_count: 4
---

# Canonical cross-chain swap: fast and decentralized settlement for cross-chain swap using canonical/native L1->L2 messaging

# Canonical cross-chain swap: fast and decentralized settlement for cross-chain swap using canonical/native L1->L2 messaging

Written by [Suah Kim](https://github.com/suahnkim) & [George](https://github.com/NegruGeorge) ([Tokamak Network](https://www.tokamak.network/))

# TLDR:

Canonical cross-chain swaps uses canonical/native L1→L2 messaging to improve decentralization and speed up settlements for liquidity providers. This improves capital efficiency and increases available liquidity to help address L2 fragmentation.

# Introduction

Popular cross-chain swap platforms like [Across](https://across.to/), [1inch](https://1inch.io/), [UniswapX](https://app.uniswap.org/), and [0x](https://0x.org/) have improved user experience with faster, cheaper, and more accessible swaps, helping reduce L2 liquidity fragmentation.

However, these improvements come with increased centralization, as these platforms rely on **permissioned or/and third-party consensus algorithms** for cross-chain messaging. This creates heightened risks for liquidity providers such as loss of fund and longer settlement times, reducing the capital efficiency.

Using the canonical L1→L2 messaging (ex: Optimism’s Portal, Arbitrum’s Inbox) for cross-chain communication provides a simpler and more decentralized cross-chain swap. This approach enables liquidity providers to conduct their own due diligence without relying on third parties. While liquidity providers still need to trust the L1 and L2 networks, this method improves capital efficiency and increases available liquidity by lowering barriers to entry for liquidity providers.

# Existing risks for liquidity providers

*For clarity, we define the following terms:*

- Requester: A user who requests a cross-chain swap
- Provider: A liquidity provider who facillitates the cross-chain swap request

While existing cross-chain swap services provide a seamless experience for Requesters, both Providers and Requesters face risks from systemic dependencies:

- Dependency on centralized cross-chain messaging: Relying on centralized cross-chain messaging (such as permissioned or third party consensus protocol) introduces risks like loss of funds and settlement delays due to service outage, errors and failures. If the service Provider decides to stop the service, it could also affect the user experience for Requesters.
- Reliance on L2: Providers must trust L2 networks to operate in good faith and prevent issues like service outages, censorship, or excessive gas prices.

# Proposed protocol

Our protocol, canonical cross-chain swap, leverages “canonical L1→L2 messaging” to enable seamless cross-chain communication, eliminating reliance on permissioned or third-party protocols. It is important to note that the current version is specifically designed to support L2-to-L1 cross-chain swaps and does not yet accommodate efficient L2-to-L2 cross-chain swaps (will be updated later).

“Canonical L1→L2  messaging” refers to native messaging system used by L2s, for example, OP stack uses Portal contracts to send message from L1 to L2. This enhances both security and user experience for Providers by reducing the number of trusted parties.

### Key Features

- Reduces dependency on permissioned or third-party cross-chain messaging
- Faster settlement times for Providers
- Minimizes Provider risks during request changes or cancellations
- Safeguards against timelock vulnerabilities in cases of service outages or L2 censorship
- Minimize transaction fees by reducing the number of transactions and storage updates while maintaining security. (Please check our MVP )
- Current version supports L2 → L1 only as a proof of concept, but it can be extended to L2 → L2.

In proposed protocol, Requesters will still receive their funds first, maintaining the excellent user experience of existing protocols, while Providers operate with less risk. This creates a fair and secure system for all participants, simplifying operations and greatly improving the Provider experience.

[![Fig. 1 L2→L1 canonical cross-chain swap flow.](https://ethresear.ch/uploads/default/optimized/3X/a/b/abd49a1358ae96fef7ecb3cd80cb6c42418820f1_2_690x454.jpeg)Fig. 1 L2→L1 canonical cross-chain swap flow.1478×974 150 KB](https://ethresear.ch/uploads/default/abd49a1358ae96fef7ecb3cd80cb6c42418820f1)

Here’s how our proposed protocol works, step-by-step:

**1. Requester makes a cross-chain swap request on L2**

Requester initiates a cross-chain swap on the origin chain by specifying details like the desired L1 token information and locking the tokens to escrow contract.

---

**2. Provider fulfills the request on L1**

Anyone can observe the requests on L2 and fulfill the request. A network of Providers observes the requests registered in the escrow contract:

(a) Provider calls the cross-chain messenger contract to provide the requested amount of tokens

(b) (in the same transaction) the Requester will receive the funds from cross-chain messenger (transferred on behalf of Provider)

(c) (in the same transaction) L1→L2 settlement request message is sent to the escrow contract, instructing it to release the locked tokens to the Provider.

---

**3. Cross-chain Messaging to L2**

Upon receiving L1→L2 settlement request message, L2 sequencer relays the message to the escrow contract. This ensures the process remains trustless and fully reliant on the security of the L1→L2 canonical messaging.

---

**4. Funds Released to the Provider on L2**

Upon receiving the message, the escrow contract verifies the transaction. It releases the locked tokens to the Provider, completing the settlement transaction (the Provider now has their funds on L2)

To summarize, in a canonical cross-chain swap:

- Requester executes a single transaction to escrow the tokens for swapping, which can be made gasless using the “permit” mechanism.
- Provider performs a single transaction on L1 to transfer the tokens to the Requester and send the settlement message. This transaction includes the L1→L2 canonical messaging, seamlessly relayed by the L2 sequencer without requiring any additional action from the Provider.

# Editing and Canceling Requests: using L1 as the Trust Anchor

To ensure the integrity of the protocol, critical operations like “editing” and “canceling” requests have to originate from L1 (cross-chain messenger contract), even if the request itself was initiated on L2 (escrow contract). This ensures that the trust and security of the system remain intact and that funds are safeguarded for both Requesters and Providers.

**Editing a request**

The “Edit” function allows the Requester to modify the token amount that the Provider should provide to Requester based on dynamic market conditions like token and gas prices.

Unlike other services that rely on off-chain oracles or time-based Dutch auction models, this feature handles edits directly through the L1 (cross-chain messenger contract). Since these changes immediately effect the Provider’s economic incentives, the edits take effect instantly when a Provider fulfills a request.

[![Fig. 2 Editing request flow. Useful to change the incentive based on the market condition.](https://ethresear.ch/uploads/default/optimized/3X/2/f/2f7aca19a7eedbe6023227c94246c63af44b2d10_2_690x313.jpeg)Fig. 2 Editing request flow. Useful to change the incentive based on the market condition.1478×672 94.5 KB](https://ethresear.ch/uploads/default/2f7aca19a7eedbe6023227c94246c63af44b2d10)

Here’s how “edit” works:

- Requester sends an edit transaction to the cross-chain messenger to update the requested amount.

For example: Requester initially wanted to exchange 10 USDC on Optimism for 8 USDT on Ethereum. When Ethereum gas prices drop, the Requester can edit their request to receive 9 USDT on Ethereum instead.

“Edit” is only applied if no Provider has fulfilled the request yet.

- Ensures that the Provider always has the most up to date information about the request and the request cannot be edited or cancelled after the liquidity has been provided.

By enforcing edits and cancellations on L1, the proposed protocol strikes a balance between flexibility and system integrity, ensuring that both Requesters and Providers benefit from L1 security throughout the entire transaction lifecycle.

**Canceling a Request**

The “Cancel” function allows the Requester to cancel their request, reclaiming their tokens from the escrow contract.

This process has to originate from the cross-chain messenger contract and only takes effect if the request has not been fulfilled. This ensures that scenarios where the Provider has already fulfilled the request are avoided, preventing the Requester from maliciously canceling the request and stealing the Provider’s funds without releasing the locked tokens on the escrow contract.

[![Fig. 3 Cancelling request flow.](https://ethresear.ch/uploads/default/optimized/3X/8/1/81b44110da1699ee3796599c402870145c63b14b_2_690x452.jpeg)Fig. 3 Cancelling request flow.1486×974 143 KB](https://ethresear.ch/uploads/default/81b44110da1699ee3796599c402870145c63b14b)

Here’s how “cancel” works:

- Requester executes the “Cancel” function on the cross-chain messenger contract (L1).

For example, Requester decides to not swap because there are better opportunity on L2.

If the request is not fulfilled, the cross-chain messenger sends a cross-chain message to the canonical L1→L2 messenger, instructing it to release the escrowed tokens back to the Requester.
After the request is sequenced on L2, the escrowed tokens are returned to the Requester.

# Disadvantages of the proposed protocol

- Increased transaction costs for the protocol: Cross-chain messenger uses canonical L1→L2 messaging, so this generally cost more than other existing services that uses off-chain or third party protocol to communicate from L1→L2. This is a trade-off for enhanced security and decentralization.
- Editing or canceling requests has to be done on L1: All edit and cancel operations must occur on L1 to maintain the protocol’s decentralized and trustless nature. While this ensures security, it requires users to interact with L1, increasing transaction costs and latency.
- Timelock is not supported for requests: The protocol cannot guarantee strict deadlines for requests due to the possibility of L2 sequencer outage or censorship, which can lead to loss of fund for Providers; instead of offering an incomplete product, the proposed protocol does not provide timelock function.
- L2 sequencer outage or censorship risks: If an L2 operator censors cross chain messages, the settlement may face delays, but the Provider will never lose any fund.
- Low capital efficiencies for L2 → L2 cross-chain swap: While the current version is designed specifically for L2 → L1 transactions, we plan to extend support to L2 → L2 swaps in the future. A straightforward extension is possible, but it would reduce capital efficiency for L2 → L2 swaps, as liquidity would need to be sourced from L1 and L2 liquidity cannot be used.

Some of these trade-offs are intentional, prioritizing decentralization, security, and trustless transactions over optimizing for minimal gas costs.

Although they may introduce certain inconveniences, these decisions align with the protocol’s objective of building a cross-chain swap system that relies solely on the security trust assumptions of L1 and L2.

# ERC 7683 Compatibility

Our protocol can integrate [ERC 7683](https://www.erc7683.org/), offering support for intent-based systems while enhancing decentralization (the “[fillDeadline](https://eips.ethereum.org/EIPS/eip-7683#:~:text=A%20compliant%20cross%2Dchain%20order%20type%20MUST%20be%20ABI%20decodable%20into%20either%20GaslessCrossChainOrder%20or%20OnchainCrossChainOrder%20type)” parameter has to set at the maximum value to avoid timelock vulnerability). This ensures Providers and users with the flexibility of interoperable standards while ensuring a more secure and efficient transaction process.

While the introduction of standards like ERC and RIP has made these systems possible, they also come with additional security assumptions. It’s encouraging to see these efforts advancing cross-chain functionality, but there remains a need for a protocol that rely solely on the inherent security of L1 and L2 networks.

# Conclusion

The canonical cross-chain swap protocol enhances decentralization and efficiency in cross-chain liquidity by leveraging native L1→L2 messaging, reducing reliance on centralized intermediaries. This approach mitigates risks, improves capital efficiency, and addresses L2 fragmentation.

# MVP

- GitHub:

link

Description:

- Provided by Tokamak Network’s George and Harvey
- Written in solidity and supports cross-chain swap from Optimism or Arbitrum L2 to Ethereum.
- Has not been formally audited and is not production ready yet.

What key contract design considerations were applied?

- Security assumption: contracts in L1 does not know what is happening on L2 and cannot verify any activites on L2. The liquidity provider must verify that the cross-chain swap request actually exists on L2.
- Transaction fee minimization: Instead of relaying unreliable request information from L2 to L1, provider must provide all the relevant information about the request and the request is verified during the settlement step.

## Replies

**The-CTra1n** (2025-01-30):

Interesting work. Looks like you are re-using many of the techniques described in these 2 posts: [here](https://ethresear.ch/t/fast-and-slow-l2-l1-withdrawals/21161) and [here](https://ethresear.ch/t/same-slot-l1-l2-message-passing/21186), albeit using two L1 → L2 messages instead of one to release the funds on L2 instead of L1.

---

**alau1218** (2025-01-31):

So the major difference between this proposal and Across v2 is that when provider fulfills the request, this proposal would also send a message to L2 sequencer to instruct the release of esrowed fund, while Across would be handled by dataworkers.

Is there other differences I omitted? Thanks.

---

**NegruGeorge** (2025-02-25):

Hey. Sorry for the late reply - we were working hard on releasing an L2 to L2 version of this proposal for the upcoming launch of Tokamak Rollup Hub ( Tokamak Rollup Hub: A Tailor-Made L2 Rollup Solution for Developers and Users )

To answer your question, yes, the key difference is we only rely on the canonical messaging system to release the funds while Across uses dataworkers and off-chain infrastructure.

The main philosophical difference is prioritizing decentralization while relying on L1 as the source of truth for every action.

We will post soon an updated version of the L2 to L2 (with a demo to see it in action).

