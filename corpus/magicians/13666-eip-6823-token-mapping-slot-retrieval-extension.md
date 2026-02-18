---
source: magicians
topic_id: 13666
title: "EIP-6823: Token Mapping Slot Retrieval Extension"
author: qdqd
date: "2023-04-03"
category: EIPs
tags: [erc, token, erc-721, erc-20, erc1155]
url: https://ethereum-magicians.org/t/eip-6823-token-mapping-slot-retrieval-extension/13666
views: 1727
likes: 0
posts_count: 4
---

# EIP-6823: Token Mapping Slot Retrieval Extension

This proposal suggests an approach to improving the accuracy of off-chain transaction simulations that involve contracts that comply with the ERC-20/ERC-721/ERC-1155 standards. The proposal provides a standardized entry point to obtain the reserved storage slot of a mapping responsible for tracking ownership of tokens in a contract. This approach not only helps capture state changes more precisely but also enables external tools and services to do so without requiring expertise in specific implementation details.

Due to the unique storage layout for different contracts, it is challenging to simulate transactions that involve smart contracts, specifically due to the use of mappings. The storage location of a value in a mapping depends on a specific storage slot, which can only be determined through knowledge of the contract’s implementation. This prevents external platforms and tools from capturing/validating changes made to a contract’s state with certainty.

This proposal introduces a function named `getTokenLocationRoot` as an extension to ERC-20/ERC-721/ERC-1155 contracts, allowing off-chain callers to retrieve the reserved storage slot for the mapping type. This approach eliminates the reliance on events, enhances the precision of data access from storage, and improves the accuracy of off-chain simulations.

https://github.com/ethereum/EIPs/pull/6830

Feel free to use this thread to discuss the proposal.

## Replies

**RenanSouza2** (2023-04-03):

Is there any tool that does this given the contract code?

Does this needs to be implemented in the smart contract?

---

**qdqd** (2023-05-04):

Sorry, I completely missed the answer in this thread, I definitely need to enable notifications!

The goal of this proposal is to establish a standardized method for obtaining the mapping slot, regardless of the specific implementation of the contract. Although it’s relatively simple to retrieve the mapping slot off-chain if you are familiar with a contract’s implementation, it’s challenging to do so for different implementations of a standard (e.g., ERC-721) that may have differently ordered storage slots or mappings with arbitrary names.

The proposed pure function offers a solution that enables off-chain tools to access the mapping slot with certainty, regardless of the specific contract implementation. This helps to verify the information provided by on-chain events with greater accuracy. As someone who also prioritizes minimizing contract bytecode, I would be pleased to figure out a 100% off-chain alternative that is as reliable as the solution outlined in the proposal. Until such an alternative is found, the proposed method remains in my opinion the most effective option for achieving the desired level of trust and accuracy, even knowing that it increases the deployment cost by a few dust.

---

**SamWilsn** (2023-05-30):

> this approach has limitations, and events should only be informative and not relied upon as the single source of truth. The state is and must be the only source of truth.

I don’t believe the state alone is the source of truth, and any simulations need to execute the code of the contract. For example, a malicious ERC-20 could easily triple the balance of an account after a certain block number with no changes to state.

At the very least, I think this needs to be mentioned in the security considerations section.

