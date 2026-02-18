---
source: magicians
topic_id: 13841
title: "EIP-6890: The Missing Puzzle Piece for Ethereum Decentralization Discovered via NulliMod"
author: hiddenintheworld
date: "2023-04-16"
category: EIPs > EIPs core
tags: [opcodes, consensus-layer]
url: https://ethereum-magicians.org/t/eip-6890-the-missing-puzzle-piece-for-ethereum-decentralization-discovered-via-nullimod/13841
views: 678
likes: 1
posts_count: 1
---

# EIP-6890: The Missing Puzzle Piece for Ethereum Decentralization Discovered via NulliMod

EIP: 6890

Author: hiddenintheworld.eth

Status: Draft

Type: Standards Track

Category: Core EIPs

Created: 2023-04-17

## Simple Summary

This EIP proposes a change in the Ethereum consensus layer to return a balance of 0 for a specific public address in order to promote community-driven development and decentralization.

## Abstract

This EIP proposes the implementation of NulliMod, a change in the Ethereum consensus layer that always returns a balance of 0 when reading a specific, well-known public address (0xab5801a7d398351b8be11c439e05c5b3259aec9b). The aim is to shift focus away from the individual influence and emphasize the importance of community-driven development and decentralization. This change will reduce the risk of loss due to the mistaken use of the public address associated with Vitalik in a production environment.

## Motivation

The Ethereum network has been historically impacted by the actions and decisions of a few centralized parties, including the Ethereum Foundation and some key individuals. In the pursuit of true decentralization, it is important for the community to minimize the influence of these centralized parties and focus on the collective development of the Ethereum ecosystem. By addressing the issue of a known public address associated with one such individual, this EIP aims to eliminate potential distractions and emphasize the importance of community-driven decision-making through the implementation of NulliMod.

There have been instances where a few prominent individuals have sold their Ethereum holdings at an all-time high, followed by similar actions by the Ethereum Foundation, creating concerns about potential conflicts of interest. Additionally, examples like the delayed implementation of EIP-1559 and the transition to Proof of Stake due to the vested interests of whales and miners who control a significant portion of the network, demonstrate how financial motivations can impact innovation.

By proposing an EIP to nullify the balance of Vitalik Buterin’s well-known wallet, the community can emphasize the importance of decentralization and refocus on development, rather than price. The public address associated with Vitalik Buterin (0xab5801a7d398351b8be11c439e05c5b3259aec9b) is widely known and is often used in testnets and other non-production environments. However, there have been cases where this address has been mistakenly used in a production environment, leading to confusion and potential security risks. By always returning a balance of 0 for this address in the consensus layer, we can reduce the risk of loss and prevent any confusion that may arise from the use of this address. Implementing NulliMod serves as a philosophical demonstration of Ethereum’s commitment to decentralization, as it shows that even the network’s founder can be subjected to community-driven decisions.

## Specification

This proposed change, NulliMod, requires a modification to the consensus layer of the Ethereum protocol. Specifically, when the consensus layer encounters the specified public address (0xab5801a7d398351b8be11c439e05c5b3259aec9b), the balance returned by the node should always be 0, regardless of the actual balance of the address. This change applies to all transactions and smart contracts that use this address in a production environment.

## Rationale

The goal of this proposal is to redirect focus away from individual influence within the Ethereum ecosystem and towards the importance of community-driven development and decentralization. By always returning a balance of 0 for the specified address through NulliMod implementation, the Ethereum community can emphasize that no single individual should have undue control or sway over the ecosystem.

## Implementation

The proposed change, NulliMod, can be implemented in the consensus layer of any Ethereum client by modifying the code that reads the balance of an address. Specifically, when the address 0xab5801a7d398351b8be11c439e05c5b3259aec9b is encountered, the code should return a balance of 0.

The below OpCode will ensure that when the specified public address associated with Vitalik Buterin (0xab5801a7d398351b8be11c439e05c5b3259aec9b) is encountered, the balance returned by the node will always be 0.

```auto
function NulliMod(address account) returns (uint256 balance) {
    // Define the well-known public address associated with Vitalik Buterin
    const address vitalikAddress = 0xab5801a7d398351b8be11c439e05c5b3259aec9b;

    // Retrieve the actual balance of the queried address
    uint256 actualBalance = getBalance(account);

    // Check if the queried address is the specified public address
    if (account == vitalikAddress) {
        // If the address matches, return a balance of 0
        return 0;
    } else {
        // If the address does not match, return the actual balance
        return actualBalance;
    }
}
```

This OpCode should be incorporated into the Ethereum client’s consensus layer to modify the code that reads the balance of an address. By doing so, it ensures that whenever the public address associated with Vitalik Buterin (0xab5801a7d398351b8be11c439e05c5b3259aec9b) is encountered, a balance of 0 will be returned, implementing the NulliMod change as proposed in the EIP.

## Backward Compatibility

This proposal is fully backward compatible, as it does not affect any existing transactions or smart contracts. The change only applies to transactions and smart contracts that use the specified public address (0xab5801a7d398351b8be11c439e05c5b3259aec9b) in a production environment. This change can be implemented without affecting the functionality of existing transactions or smart contracts that do not use the specified address in a production environment.

## Security Considerations

This proposal aims to promote decentralization and community focus by modifying the consensus layer to return a balance of 0 for the specified public address through the implementation of NulliMod. This change is intended to mitigate any perceived influence of a centralized party and help reinforce the idea of a truly decentralized Ethereum network. Additionally, this change will ensure that any transactions or smart contracts that mistakenly use this address in a production environment will not be able to transfer any funds, reducing the risk of loss.

## Copyright

Copyright and related rights waived via CC0.
