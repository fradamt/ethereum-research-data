---
source: ethresearch
topic_id: 20396
title: "Introducing CCTP Express: a faster and cheaper way to use CCTP"
author: 0xwels
date: "2024-09-10"
category: Applications
tags: []
url: https://ethresear.ch/t/introducing-cctp-express-a-faster-and-cheaper-way-to-use-cctp/20396
views: 536
likes: 2
posts_count: 1
---

# Introducing CCTP Express: a faster and cheaper way to use CCTP

By [Wel](https://twitter.com/wels_eth) and [Alan](https://twitter.com/alau1218) on behalf of CCTP Express

*For most recent information about CCTP Express, please visit [our X](https://twitter.com/cctpexpress).*

# Motivation

We recognize the vital role stablecoins play in the Web3 ecosystem, especially within DeFi. Among them, USDC stands out for its high transparency and regulatory compliance. Circle, the issuer of USDC, introduced the Cross-Chain Transfer Protocol (CCTP) to securely transfer USDC across chains using a native burn-and-mint mechanism.

CCTP is a game-changing tool that drives USDC adoption in the multichain world, allowing developers to create applications that offer secure, 1:1 USDC transfers across blockchains. This eliminates the added risks of using bridges.

However, CCTP has a key limitation: wait time. Its off-chain attestation service requires block confirmations on the source chain to ensure finality before minting USDC on the destination chain. This process can take anywhere from 20 seconds to 13 minutes, which is not ideal for users needing instant transfers. To address this, CCTP Express was designed to provide instant USDC bridging while leveraging CCTP. We position CCTP Express as a booster tool of CCTP, enabling users to benefit from faster and cheaper transactions.

We believe CCTP Express is an essential tool to achieve chain abstraction by providing an instant USDC bridging experience.

# TL;DR

- CCTP Express is positioned as a booster tool to use CCTP, where users enjoys a faster and cheaper experience;
- It is an intent-base bridging system built upon CCTP, instant USDC bridging is enabled by the “Filler-Pay-First” mechanism;
- CCTP Express is a trustless design, allowing anyone to participate as a filler or datadaemon without permission;
- To mitigate the reorg risk exposed to the fillers, CCTP Express introduces an insurance fee that varies based on the user-defined initiateDeadline.;
- In order to lower the transaction costs, repayment and rebalancing transactions are bundled, cross-chain messages are transmitted as hashes to reduce data size.

# Primary principles

**1. CCTP Dependency**

CCTP Express is specifically designed to enhance CCTP. All fund rebalancing must be done exclusively through CCTP to avoid exposure to potential risks associated with other bridges.

**2. Decentralization**

The system must be trustless to ensure maximum protection for everyone’s assets. Players in the system, including Fillers and Datamaemon, are permissionless.

**3. Win-Win-Win**

The design should benefit all stakeholders — users, fillers, and CCTP. Users gain a faster and more cost-effective experience, fillers receive satisfactory rewards while their funds are safeguarded, and CCTP grows stronger through the support of CCTP Express.

# Key concepts

CCTP Express is an intent based cross-chain bridging system built upon CCTP. The key to speed up the transaction is the adoption of the “Filler-pay-first” mechanism.

When a user submits a bridging intent, fillers initiate an order on the origin chain, then immediately call a fillOrder on the destination chain and transfer funds to the user accordingly.

The system periodically validates the payments and repays to fillers in batches. Rebalancing across domains is done across CCTP if needed. This settlement process is out of the scene of the users, the repayments and rebalancing are bundled to save costs.

# Dive Deeper

CCTP Express adopts a Hub-and-Spoke architecture, it can be broken down into a 3-layered system: a request for quote mechanism to obtain users’ bridging intent, enabling a filler network to claim and fill those orders, and lastly a settlement layer periodically repay fillers through CCTP and utilizing attestation service from Iris (Circle’s off-chain attestation service).

Our design adheres to ERC-7683, emphasizing the importance of aligning with industry standards. This ensures that cross-chain intent systems can interoperate and share infrastructure like order dissemination services and filler networks. By fostering this interoperability, we enhance the end-user experience by increasing competition for fulfilling user intents. Below is a diagram of the architecture of CCTP Express:

[![Architecture of CCTP Express](https://ethresear.ch/uploads/default/optimized/3X/0/3/037c645827e04b44e5ed2f79fedaddff4f92eab3_2_690x451.jpeg)Architecture of CCTP Express1912×1250 96.4 KB](https://ethresear.ch/uploads/default/037c645827e04b44e5ed2f79fedaddff4f92eab3)

**Order initiation**

1. User signs an off-chain message defining the parameters of an order:

```auto
 function deposit(
        bytes32 recipient,
        bytes32 inputToken,
        bytes32 outputToken,
        uint256 inputAmount,
        uint256 outputAmount,
        uint32 destinationDomainId,
        bytes32 exclusiveFiller,
        uint32 exclusivityDeadline,
        uint32 initiateDeadline,
        uint32 fillDeadline,
        bytes calldata message
    ) external;
```

1. The order is disseminated to Fillers. The Filler calls initiate on the origin chain SpokePool. A CrossChainOrder will be created and the user’s funds are transferred to the SpokePool for escrow.
2. The SpokePool on origin chain submits a Deposit message to Circle’s off-chain attestation service, Iris, for attestation and subsequently a DepositAttestation will be generated.

**Filler Network Fills Order**

1. Fillers call fillOrder on the destination SpokePool with their own assets which are then transferred to the user from the SpokePool.
2. The SpokePool on destination chain submits a Fill message to Iris and a FillAttestation will be generated.

**Settlement**

1. A permissionless Datadaemon retrieves the DepositAttestation and FillAttestation and relays to the Hub Pool on the Settlement Chain.
2. Periodically, the Datadaemon calls repayFunds and rebalanceFunds at the Hub Pool, which would collect all the attestations and perform the following steps:

- Iterate through a list of attestations, a valid filled order is supported by both Deposit and Fill attestation.
- Determine the aggregate settlement sum from all valid fills for each filler.
- If there is sufficient funds on SpokePool to repay filler, a repayFunds message in the form of merkle root hash is sent to Iris.
- For the remaining outstanding payment, the Hub Pool will send a rebalanceFunds message in the form of merkle root hash to Iris, which indicates how much a SpokePool with surplus funds would send to another pool in deficit to fulfill the need for repayment.

1. Once the repayFunds and rebalanceFunds messages get attested by Iris, they are sent to respective SpokePools. Datamaemon will call repayFunds and rebalanceFunds on SpokePools with merkle root hash and their respective transaction details. Accordingly, funds would be repaid to fillers and sent to other SpokePools to ensure sufficient funds for handling repayments.
2. Repay funds to fillers from the SpokePool on destination chain, and rebalance funds across SpokePools on different chains via CCTP.

**Cctp Fill Settlement**

1. In case of an order initiated by Fillers not being filled, anyone can call cctpFill and mark the order status on destination chain SpokePool to RequestCctpFill and block any filler from filling it. At the same time, the SpokePool will emit a CctpFill message to Iris for attestation.
2. The CctpFillAttestation will be used to replace the FillAttestation mentioned in 5. and allow the user fund to be transferred via the CCTP route.

# Risk and solutions

**Reorg risk**

The reorg risk is uniquely borne by fillers. If the filler fills the intent too fast without waiting for the finality on the source chain, the source chain may reorg and cause a loss to the filler since the intent has been filled on the destination chain and the filler would end up in empty hand.

The reorg risk is effectively mitigated by the **Insurance Fee**, which varies based on the `initiateDeadline` specified by the user. If the `initiateDeadline` is sufficiently long, the filler can reinitiate the `CrossChainOrder` on the origin chain in the event of a reorg, ensuring the user’s funds are transferred again. The insurance fee is calculated using below formula:

[![Formula of Insurance Fee](https://ethresear.ch/uploads/default/original/3X/8/f/8f2626d45b13f0ec864c696fa581f0af9f7491b6.png)Formula of Insurance Fee488×192 2.96 KB](https://ethresear.ch/uploads/default/8f2626d45b13f0ec864c696fa581f0af9f7491b6)

Where:

*f(t)* is the insurance fee which is a function varies with *t*

*V* is the trading volume, representing the maximum insurance fee

*e* is the base of the natural logarithm

*k* is a constant that control the descending rate of the fee

*t* is the time between order creation time and the initiateDeadline

*T* is the time required for finality on the origin chain

The insurance fee varies with the `initiateDeadline`- it decreases with the increment of time between the order creation time and the `initiateDeadline`:

[![](https://ethresear.ch/uploads/default/optimized/3X/1/6/1626648dc74ed8b71e5d3e7f66c0b1d9731baba1_2_321x250.png)722×562 15.1 KB](https://ethresear.ch/uploads/default/1626648dc74ed8b71e5d3e7f66c0b1d9731baba1)

Since the insurance fee decreases significantly when the `initiateDeadline` is long (it drops to nearly zero if it is 2x of the time needed for finality on the origin chain), a normal user is likely to set a long initiateDeadline to avoid paying the fee, minimizing the reorg risk for the filler.

**High system costs**

The complexity of the design apparently implies higher costs compared to bridging directly using CCTP. To align with our goal of providing a faster and cheaper way to use CCTP, we mitigate costs through two key strategies: ***transaction bundling*** and ***data compression***.

Transactions bundling-

Datadaemon works periodically to call repayment and rebalancing on the hub pool. This interval is adjustable to make sure a sufficient number of transactions are processed in each batch.

In this architecture design, gas costs are primarily incurred in rebalancing via CCTP and fund transfers. By processing rebalancing in batches and handling repayments in aggregate sums to the fillers, these costs are distributed across multiple transactions, reducing the costs on any single transaction.

Data Compression-

Cross-chain messages are transmitted between spoke pools and the hub pool via Iris, Circle’s off-chain attestation service. To minimize data size and reduce gas costs, these messages are sent in the form of a hash.

For a detailed comparison of gas consumption between CCTP and CCTP Express, check out [this article](https://medium.com/@cctpexpress/cctp-express-is-cheaper-than-cctp-2c527e0afa62).

# FAQ

**1. What does it mean to the end user?**

When using CCTP Express’s front end or applications integrated with CCTP Express, users benefit from a significantly faster and cheaper way to bridge USDC across chains. By leveraging CCTP as the underlying asset bridge, the system enhances user experience while maintaining robust security.

**2. What are the possible use cases?**

We believe CCTP Express is essential to achieve chain abstraction by providing an instant USDC bridging experience. Possible use cases included-

*USDC-denominated dApps*

USDC is widely adopted in various dApps, e.g. dYdX and Polymarket. dApps can integrate CCTP Express SDK to offer their users instant transfer in and out from all CCTP supported chains without the usual waiting time.

*Payment Network*

CCTP Express can offer instant settled transaction experience for users across chains, enabling them to pay their USDC for a coffee from any CCTP supported chain.

*Money Lego*

Arbitragers and Solvers can utilize CCTP Express to be the backbone of their cross chain actions. It’s highly undesirable for arbitragers or solvers to wait for long in the high speed crypto world, CCTP Express can offer them superior speed without worrying about security as CCTP Express is using CCTP as the underlying bridge.

**3. With a similar idea of providing cross chain bridging powered by off chain agents, how is CCTP Express different from other intent-based bridges, say Across?**

The primary distinction between CCTP Express and Across are: positioning and settlement mechanism.

*Positioning -*

While both protocols are intent-based bridges powered by fillers/relayers, CCTP Express is positioned to be a booster tool to use CCTP.

Given this focus, CCTP Express is closely integrated with CCTP and evolves in tandem with it. For instance, if CCTP supports EURC, CCTP Express will promptly support it as well.

And this alignment also applies to the choice of picking which chain CCTP Express supports. CCTP Express aims to cover all EVM and non-EVM chains CCTP operates. And like[CCTP](https://developers.circle.com/stablecoins/docs/message-format#message-header), CCTP Express adopts the bytes32 address format, instead of the 20 byte address used in EVM, to handle 32 byte addresses in many non-EVM chains.

In contrast, Across is limited to EVM chains only, as it has a[hard requirement](https://docs.across.to/resources/new-chain-requests) to support EVM- chains only.

*Settlement mechanism -*

In CCTP Express, the Hub Pool smart contract utilizes the Iris attestation service used in CCTP to relay and verify messages. Deposit and Filled messages from various Spoke Pools are sent to Iris for attestation and then collected in the Hub Pool, which processes repayments on-chain.

In contrast, Across uses canonical bridges to relay messages and utilizes[UMA](https://docs.across.to/use-cases/settle-cross-chain-intents) to optimistically verify fill events off-chain. Since UMA works off-chain, an interval is needed as a dispute window.

# Discuss with Us

To shape a better product, we are keen to discuss with users, fillers and dApp teams who need instant USDC bridging. If anyone is interested in CCTP Express, we have a public telegram group here to discuss about it: [Join Group Chat](https://t.me/cctpexpress)
