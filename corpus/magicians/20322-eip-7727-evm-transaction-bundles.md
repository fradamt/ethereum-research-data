---
source: magicians
topic_id: 20322
title: "EIP-7727: EVM Transaction Bundles"
author: Lilyjjo
date: "2024-06-17"
category: EIPs
tags: [mev]
url: https://ethereum-magicians.org/t/eip-7727-evm-transaction-bundles/20322
views: 1687
likes: 4
posts_count: 3
---

# EIP-7727: EVM Transaction Bundles

Discussion thread for [EIP-7727](https://eips.ethereum.org/EIPS/eip-7727)

Today, all sequencing logic for a mainnet block is controlled by the single winner of the JIT PBS block auction. This is problematic as sequencing, the choice of who gets to alter what piece of state in what order, influences value flow. The goal of this EIP is to give transactions and smart contracts more control over how they are sequenced through explicit delegation of local sequencing rights.

### Technical Summary

This EIP aims to enable more fine-grained and multi-party block building by introducing two new EIP-2718 transaction types and one new opcode. These new additions would provide:

- The ability for transactions to delegate their local sequencing to a specified external party.
- The ability for an external party to build ‘bundles’ of transactions that are run in order in a block.
- The ability for smart contracts to see who put the transaction in a bundle if the transaction was in a bundle.

One of the EIP-2718 transactions would extend normal transactions to include two new fields: `bundle_signer` and an optional `block_number`. The `bundle_signer` would be the entity who is delegated local sequencing rights for the transaction, and the `block_number` would be the block number that the transaction is valid in if not zero.

The other EIP-2718 transaction would be a meta-transaction whose only function is to order transactions that delegated sequencing rights to the signer of the transaction. This meta-transaction could only sequence transactions that delegated to it and could also delegate itself to another external party and specify a block number. This transaction would not start an execution context for itself.

The opcode, potentially named `BUNDLE_SIGNER`, would expose the most immediate external party who put the transaction into a bundle if present.

Other relevant pieces of technical information:

- Unlike searcher PBS bundles, there is no revert protection provided to the sequenced transactions. This is to enable this EVM change to work with all types of EVM block builders, including ones that do not do simulations.
- If a transaction in the meta-transaction’s bundle is invalid, the bundle signer is charged for the invalid transaction as if it were just CALLDATA bytes. This is for DOS protection and due to the inability for a bundle creator to control all state that it is building on.
- If a transaction specifies a bundle_signer, it must be included in a bundle signed by the signer to be valid. This is to prevent competition between the total block builder and the delegated bundle creators.

[![Screenshot 2024-06-17 at 5.38.55 PM](https://ethereum-magicians.org/uploads/default/optimized/2X/b/bc8b64e6c82ff08f6070465f69a686dc00f4c090_2_690x484.png)Screenshot 2024-06-17 at 5.38.55 PM2576×1808 232 KB](https://ethereum-magicians.org/uploads/default/bc8b64e6c82ff08f6070465f69a686dc00f4c090)

### Example Use Cases

Together, these new forms of expression would enable:

- Smart contracts to auction off the right to be the first entity to operate on a piece of state, such as:

AMMs auctioning off the first swap to lessen LVR. (Example using PBS searcher bundles).
- Oracles auctioning off the rights to be the first transaction post update to cover posting costs.
- Lending protocols auctioning off the right of liquidation of hard-to-price collateral.

Smart contracts to order transaction operations for user benefit, such as:

- Lending protocols placing user liquidity adds before liquidations to reduce bad debt creation.
- AMMs preventing sandwiching.

Front-ends and wallets to explicitly sell their order flow to mini-builders who do not have to win the entire block.

### Unanswered Questions:

- Difficulty of verifying the new opcode for zk-evms.
- How this composes with account abstraction efforts.

### Feedback Wanted!

- Is this plan technically infeasible for any reason?
- Are you interested in this?
- Is there a different design which could enable a similar result?

This EIP idea is an attempted technically more coherent plan of an idea expressed in this [Eth Research](https://ethresear.ch/t/evm-native-sequencing-rules/19606) post.

## Replies

**thogard** (2024-06-17):

It’s not clear to me why an EIP is needed for this when the same goals can already be accomplished without an EIP using execution abstraction (E.G. [atlas_whitepaper/Atlas_Whitepaper.pdf at main · FastLane-Labs/atlas_whitepaper · GitHub](https://github.com/FastLane-Labs/atlas_whitepaper/blob/main/Atlas_Whitepaper.pdf) ).

To be clear, what you’re proposing is functionally different, I’m just not seeing its advantages over op-level (EOA or SCW) sequencing that can more readily pass data between operations. Can you elaborate on the advantages of bundle-specific sequencing at the transaction level over the operation level?

Support for repeatable 7702 txs?

---

**Lilyjjo** (2024-06-18):

Is this a fair summary to you?

Execution Abstraction:

- Uses account abstraction transactions instead of traditional transactions as a base.
- Builds bundles of the account abstraction transactions off-chain.
- Uses an on-chain EntryPoint-like smart contract to verify and guarantee proper bundle construction and execution.

I read the Atlas white paper, which seemed to be focused on pairing user messages with searcher messages. I’m going to assume that Execution Abstraction could be extended to construct bundles that don’t require searchers to benefit for transactions to be included in bundles. I’m also assuming that DApps would be able to restrict their ordering to a specific off-chain entity somehow.

Similarities:

- Neither solves for reverting.
- Both enable easier OFA to occur.
- Both involve somewhat trusted off-chain infrastructure to provide the bundling service.

The major difference I see is the use of Account Abstraction. If it could be considered a benefit, native transaction bundles offer a bundling solution that avoids reliance on buying into an AA solution. I think both solutions inherit the arguments pro/con account abstraction in general.

I want to argue that the native bundles allow for more generic bundling, but this is due to me not fully understanding what level of integration a DApp would need with the EntryPoint-like contract to have transactions bundled in it.

I’ll think more on other benefits/disadvantages and follow up. I’d be interested if you see explicit disadvantages of including an EIP like this.

Also I’ll followup on 7702 after I have more time to research it.

