---
source: ethresearch
topic_id: 19931
title: P2P ZK Light Client Bridge between Tron and Ethereum L2s
author: alexhook
date: "2024-06-28"
category: Applications
tags: []
url: https://ethresear.ch/t/p2p-zk-light-client-bridge-between-tron-and-ethereum-l2s/19931
views: 4490
likes: 6
posts_count: 1
---

# P2P ZK Light Client Bridge between Tron and Ethereum L2s

*By [Alex Hook](https://x.com/alexhooketh). Thanks to these people for inspiration, feedback and suggestions: [accountless.eth](https://x.com/alexanderchopan), [pseudotheos](https://x.com/pseudotheos), [Domothy](https://x.com/domothy), [Dogan Alpaslan](https://x.com/DoganEth), [ZKP2P team](https://zkp2p.xyz)*

---

**Abstract.** USDT on the Tron Network has emerged as a dominant crypto application in the Third World countries. However, the current cartelized control of the Tron Network results in elevated transaction fees, capital concentration, and an ecosystem isolated from other crypto networks. We propose a design for a cost-effective, peer-to-peer bridge from USDT TRC20 to Ethereum L2 networks, utilizing zero-knowledge light verification of the Tron blockchain.

# Introduction

According to [Token Terminal](https://tokenterminal.com/terminal/datasets/stablecoins), USDT on Tron has achieved preeminence by several metrics, including outstanding supply, 30d transfer volume, number of transfers, and number of holders. At the time of writing, the second place by volume, DAI on Ethereum, has only ~20% less volume than it, but two orders of magnitude fewer holders and number of transfers. The second place by number of transfers, USDC on Base, has 5x fewer transfers.

[![Screenshot 2024-06-27 at 8.00.11 PM](https://ethresear.ch/uploads/default/optimized/3X/6/4/6476c0c44ca7866bfea5a4f35205a47fa7c74204_2_690x459.png)Screenshot 2024-06-27 at 8.00.11 PM1096×730 77.1 KB](https://ethresear.ch/uploads/default/6476c0c44ca7866bfea5a4f35205a47fa7c74204)

This shows Tron USDT’s monstrous levels of payment usage among individuals. Unsurprising—Tron team has done an extensive advertisement campaign for its payment solution in Africa and Latin America. Shortly after, the network effect spread it to the developing countries in Asia and Post-Soviet area.

If we look at the areas of the largest prevalence of Tron USDT, a noteworthy pattern can be noticed. Tron USDT is largely used in the countries with weak economies and unsustainable local currencies: Türkiye, Lebanon, Zimbabwe, Venezuela, Argentina, and more. In these countries, traditional banking doesn’t provide people with options for reliable store of value and means of payment, as local currencies are unreliable, and foreign currencies are either banned for payment use or subject to strict control.

### Problems

It is fair to say that USDT on Tron is one of the largest crypto applications by usage today. Millions of people around the world are interacting with it every day. It’s massively used as a store of value, acts as a medium of exchange in isolated economies such as Northern Cyprus, Cuba, and Vietnam. [Local P2P platforms are building their infrastructure around USDT on Tron](https://mirror.xyz/0x8958D0c419BCDFB8A86b8c0089552bE015fbe364/ODhOuYjK80atc9_jGprXotSo3PNobT1PRLFtorXHBrA). However, its dominance presents certain challenges for the broader Web3 community:

- A primary concern is the high degree of centralization within the Tron Network. According to our research, over the past 250 days there were only 28 unique block producers. The same entities are constantly winning the DPoS election due to delegations from the largest TRX holders. Most of these Super Representatives (block producers in Tron) lack any public information beyond their status as block producers.
- Despite this centralization, transaction fees on Tron remain among the highest in crypto—420 sun (1 sun = 1e-6 TRX) per gas. At the TRX’s price of ~0.000035 ETH, this roughly corresponds to Ethereum L1’s gas price of 14.7 gwei. The usual fee for USDT transfers in Tron is $1-1.5 in TRX, rendering small transfers barely economical. However, the usage is still very high, as Tron’s ecosystem is isolated and there’s no convenient way to interact with other ecosystems from it.

In contrast, the Ethereum ecosystem continues to thrive. Following the Dencun upgrade, transaction fees on rollups have drastically decreased to [less than a cent](https://www.growthepie.xyz/fundamentals/transaction-costs) per ERC20 transfer. Combined with L2s, Ethereum DeFi [now comprises >80% of the entire DeFi TVL](https://defillama.com/chains). [Rollups alone consistently handle upwards of 100 TPS](https://l2beat.com/scaling/activity), [with theoretical limits of 400-800 TPS](https://mirror.xyz/alexhook.eth/y9PTlM6tVr0H8X68r1LV2UwAnT9D6u1MEEiUFvcpyG0) depending on the specific rollup. OP Mainnet has upgraded to Stage 1 trustlessness with all OP Chains and ZKsync catching up this summer. Arbitrum is working towards Stage 2.

People in developed countries are already integrated with Ethereum. By allowing ones from developing countries to seamlessly move into it from Tron, we can unite these disparate ecosystems and mitigate the risks associated with increasing centralization and monopolization of Sun’s machine.

# Rationale

The protocol for cross-chain transfers from Tron should ideally possess the following characteristics:

- Trust-minimized: The system should preclude the provision of incorrect information about the Tron blockchain or the theft of locked funds, except in the event of an attack on Tron’s consensus. In such a case, the security council authorized to stop the system can be established.
- Permissionless liquidity supply: The protocol should allow any entity to provide liquidity at their preferred rate. This fosters fair competition among providers, potentially resulting in more favorable and flexible exchange rates based on order size.
- Permissionless operation: While a centralized relay for light client updates and order fulfillment is acceptable, provided there exists a self-proposing mechanism in case of liveness failure, the relay must not serve as a source of trust. When feasible, on-chain operations should be implemented instead (e.g., a paymaster for gasless order claims).
- As simple as possible from the Tron side: Gas fees on Tron are extremely high, so it may be not affordable for users to execute more than necessary on-chain. Moreover, USDT Tron users are mostly using wallets such as Trust Wallet, Exodus, hardware wallets, and local exchange accounts, that do not support contract calls or token approvals. The only Tron wallet with these features, TronLink, is not common among USDT Tron users.
- Reasonably cheap on the destination side: Zero-knowledge proofs should be employed where possible to minimize costs. While the system can be more extensive than on the Tron side, it should still be optimized to keep user claim costs low.
- Single liquidity hub with enshrined bridging: The protocol should be deployed on a single L2 network to prevent liquidity fragmentation. To mitigate protocol isolation, cross-chain token bridges can be integrated at the UI level, similarly to ZKP2P.
- USDC-native: Given USDC’s prevalence in the Ethereum ecosystem, the protocol can be based on USDC, effectively providing USDT-USDC swaps. However, USDC is virtually unknown in areas of extensive USDT Tron usage, so this difference should be addressed on UX level to reduce user distrust.

# Tron’s consensus and protocol 101

[![image](https://ethresear.ch/uploads/default/optimized/3X/8/1/81e8ead1ee5585f245d51ac55f4f1db43f3785d2_2_540x500.png)image677×626 65.8 KB](https://ethresear.ch/uploads/default/81e8ead1ee5585f245d51ac55f4f1db43f3785d2)

Every 6 hours (7200 blocks), network participants delegate their TRX to validator candidates. The 27 candidates accumulating the most votes are elected as Super Representatives (SRs), who are then responsible for block production. Block producer selection follows a deterministic round-robin pattern. A block is considered finalized after receiving 18 confirmations, 2/3 of the SR set.

The block production is an ECDSA signature over the SHA256 hash of the protobuf-encoded block header. That is, one block = one signature. The top 128 representatives, beyond the 27 SRs, are designated as Super Representative Partners, voting on blocks produced by SRs. However, [as producers are predictable and the longest-chain rule is applied](https://developers.tron.network/docs/concensus#block-generation-mechanism), there is no necessity in validating votes.

Block header consists of the following elements:

```auto
message BlockHeader {
  message raw {
    int64 timestamp = 1;
    bytes txTrieRoot = 2;
    bytes parentHash = 3;
    int64 number = 7;
    bytes witness_address = 9;
    int32 version = 10;
  }
  raw raw_data = 1;
  bytes witness_signature = 2;
}
```

Even though state root is formally specified in the protocol, it’s not added to the header. We assume this is for backward-compatibility purposes, as the current version of Tron Network does not merkleize state.

The signature is made over a SHA256 hash of the serialized `raw_data` element. That is, by utilizing light verification, we can access only one transaction-specific element—the Merkle root of the transaction tree. However, in Tron, transactions carry their execution status, so we don’t need to access the state to validate the success of one-transaction operations, such as TRC20 transfer().

```auto
message Transaction {
  ...
  message Result {
    enum code {
      SUCESS = 0;
      FAILED = 1;
    }
    enum contractResult {
      DEFAULT = 0;
      SUCCESS = 1;
      REVERT = 2;
      BAD_JUMP_DESTINATION = 3;
      OUT_OF_MEMORY = 4;
      PRECOMPILED_CONTRACT = 5;
      STACK_TOO_SMALL = 6;
      STACK_TOO_LARGE = 7;
      ILLEGAL_OPERATION = 8;
      STACK_OVERFLOW = 9;
      OUT_OF_ENERGY = 10;
      OUT_OF_TIME = 11;
      JVM_STACK_OVER_FLOW = 12;
      UNKNOWN = 13;
      TRANSFER_FAILED = 14;
      INVALID_CODE = 15;
    }
    int64 fee = 1;
    code ret = 2;
    contractResult contractRet = 3;
    ...
}
```

Votes for witnesses (representatives) are of a specific transaction type. This means that in order to calculate the votes, the light client has to download all transactions and re-execute ones of this type.

```auto
message Transaction {
  message Contract {
    enum ContractType {
      ...
      VoteWitnessContract = 4;
      ...
}
```

However, considering the fact that the SR set is almost static, we believe that it would be computationally cheaper to delegate choosing the canonical set to DAO or enshrine the set into the circuit.

Normal contract calls, such as TRC20 transfer, have the `TriggerSmartContract` type and are nearly identical to ERC20 transactions. This means that we can prove the USDT transfer on Tron network using only the transaction root, which can be safely accessed on-chain using ZK light client relay.

# Design proposal

[![image](https://ethresear.ch/uploads/default/optimized/3X/4/b/4b4b8d0d74dfe0a7dd5991bce974eac97c8621fc_2_690x402.jpeg)image1519×887 226 KB](https://ethresear.ch/uploads/default/4b4b8d0d74dfe0a7dd5991bce974eac97c8621fc)

The proposed cross-chain swap mechanism involves three primary entities: the *User*, the *Buyer* (or liquidity provider), and the *Relayer*. The process unfolds as follows:

1. The Buyer locks USDC into the swap contract on the L2, specifying their exchange rate and Tron address for transfers.
2. The User selects a Buyer offering the most favorable rate with sufficient liquidity. The User then initiates a transaction on the L2 to temporarily lock a portion of the Buyer’s USDC. This step prevents liquidity depletion before order fulfillment. If supported by the L2, this transaction may be funded by a paymaster.
3. The User transfers the corresponding amount of Tron USDT to the Buyer’s specified address.
4. Following 18 block confirmations (~54 seconds, ensuring finality), the Relayer retrieves the latest Tron block headers and generates a ZK proof to them. The circuit for light verification must contain the transaction root from the header as the public input so that it’s known to the relay contract. This proof is needed to efficiently prove the new Tron blocks and their transaction roots to the relay contract.
5. The Relayer obtains the finalized transaction from the Tron blockchain and generates a zero-knowledge proof of transaction inclusion against the transaction root. This proof is needed to efficiently prove the order fulfillment to the swap contract. Just like light client proofs, transaction proofs can be aggregated to minimize the costs of on-chain proof verification.
6. The Relayer submits these proofs to the respective smart contracts on the L2. Upon verification, the swap contract releases the funds to the User and allocates a small portion to the Relayer as compensation. In case of liveness failure, the User can generate and relay proofs themselves, removing the need for relayer fees.
7. The Buyer can exchange their acquired Tron USDT for USDC on the L2 through various means, including direct 1:1 exchange with issuers, and reinvest in the swap contract.

This system streamlines the user experience to just two primary actions: committing to the order on the destination chain and transferring Tron USDT to a specified address. The User receives the equivalent USDC on the L2 within approximately one minute. This system can even be used to accept payments in USDT Tron, requiring only a web browser with a connected wallet for order creation.

For Buyers, liquidity provision is fully automated. They create a Tron wallet, and supply USDC with specified Tron address to the smart contract. When their liquidity is out, it is automatically removed. Received USDT can be spent and exchanged back to USDC at any time. This system is expected to provide higher exchange rates than the existing P2P platforms, as the rate is competitive and there’s no need to cover the costs of KYC and other web2-specific processes.

Relayers require only a server running relayer and ZK prover software. As relayers do not serve as the source of trust, this role can be either permissionless or delegated to the development team, provided self-proposing functionality is supported.

# ZK Light Client PoC

We’ve written a proof-of-concept of ZK light verification of Tron blocks in Noir language. It receives the previous and new block IDs with a transaction root as the public input, and the block header as the private input. It does not implement round-robin checks and election mechanism for efficiency purposes, and the SR set is hardcoded into the circuit. The proof is generated in about 35 seconds on an M1 machine.

For the production version of this system, it may be necessary to rewrite the circuits to STARK-based proof systems and/or implement GPU proving to improve proving speed.

The source code can be found here: [GitHub - ultrasoundlabs/zktron: ZK light client for Tron Network written in Noir](https://github.com/alexhooketh/zktron)

# Conclusion

The proposed P2P ZK Light Client Bridge between Tron and Ethereum L2s is a significant advancement in addressing the problems of Tron Network in a Web3 way. By leveraging zero-knowledge proofs and efficient light client verification, this system offers a trust-minimized, permissionless, and cost-effective solution for bridging the gap between these two prominent blockchain ecosystems.

This bridge design addresses several key challenges:

1. It mitigates the risks associated with the centralization of the Tron Network by providing users with seamless access to the more decentralized and robust Ethereum ecosystem.
2. It significantly reduces transaction costs for users, particularly benefiting those in developing economies who rely heavily on USDT for daily transactions and value storage.
3. It enhances liquidity and interoperability between Tron and Ethereum, expanding Ethereum ecosystem to the areas of extensive Tron usage.
4. It maintains a high level of security through the use of ZK proofs, ensuring the integrity of cross-chain transactions without compromising on efficiency.

By bridging these ecosystems, we can solve the problem of increasing influence of Tron, taking a significant step towards realizing the vision of a truly global, decentralized financial infrastructure that can benefit users across all economic backgrounds.

We welcome feedback and questions from the community. Feel free to leave your comments, suggestions, or inquiries in the comments section below. **Thank you for reading.**
