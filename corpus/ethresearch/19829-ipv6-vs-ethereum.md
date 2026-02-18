---
source: ethresearch
topic_id: 19829
title: IPv6 vs Ethereum?
author: peersky
date: "2024-06-15"
category: Networking
tags: []
url: https://ethresear.ch/t/ipv6-vs-ethereum/19829
views: 3477
likes: 3
posts_count: 3
---

# IPv6 vs Ethereum?

I started writing this after a few days of unsuccessful attempts to run solo node behind CGNAT, as just a brainbreeze on whether it could be somehow done differently to ease up solo node setup.

So far It does not seem to be an answer, however I want to share some thoughts on analogies seen with ipv6 networking to see if anyone has ideas on how this can be useful . .

## ipv6 101

An IPv6 address consists of 128 bits, represented as eight groups of four hexadecimal digits separated by colons. Each group is called a hextet. For example:

`2001:0db8:85a3:0000:0000:8a2e:0370:7334`

where

- Global Routing Prefix: 2001:0db8 (Assigned by the Regional Internet Registry)
- Subnet ID: 85a3:0000 (Identifies a specific subnet within the network)
- Interface ID: 0000:8a2e:0370:7334 (identify the individual interface or device on the subnet)

This hierarchical structure allows for efficient routing of IPv6 packets. Routers can quickly determine the destination network based on the global routing prefix, then further refine the path based on the subnet ID.

*Multiple gateways* from ipv6 subnet may exist to public ipv6 space. Addresses within ipv6 sub network may access global ipv6 address space. Routing protocols such as [OSPFv3](https://datatracker.ietf.org/doc/html/rfc5340) or [BGP](https://en.wikipedia.org/wiki/Border_Gateway_Protocol) may be used.

## Subnet Gateway analogy

Just as an IPv6 router directs traffic to devices within its subnet, an RPC node facilitates communication with nodes and smart contracts within its respective blockchain network.

When we consider the concept of Chain IDs. In blockchain, Chain IDs are unique identifiers for different networks (e.g., Ethereum Mainnet has Chain ID 1, while various testnets have different IDs). Similarly, in IPv6, a subnet is identified by its unique prefix, which is a portion of the IPv6 address.

## Address analogy

Since Interface Ids in IPv6 are only 64 bits long, they are too small to fit in 160 bits address of Eth.

However, what could be useful is using InterfaceIds to identify the nodes in the P2P network, forming VPC for Ethereum.

In IPv6, organizations or individuals can assign themselves a unique subnet prefix, effectively creating their own independent addressing space.

### Cryptography for IPv6 address generation

[Secure Neighbor Discovery (SEND)](https://en.wikipedia.org/wiki/Secure_Neighbor_Discovery) is a security extension to the Neighbor Discovery Protocol (NDP) in IPv6, designed to address the vulnerabilities in the original NDP.

There are several papers and RFCs (Requests for Comments) relevant to cryptography for IPv6 address generation, particularly focusing on enhancing privacy and security:

**[RFC 3972](https://datatracker.ietf.org/doc/html/rfc3972) - Cryptographically Generated Addresses (CGA)**: This RFC introduces the concept of CGA, where the interface identifier of an IPv6 address is generated using a cryptographic hash function from a public key and other parameters. This approach aims to bind a public key to an address securely, deterring address theft and enhancing authentication.

**[RFC 7721](https://datatracker.ietf.org/doc/html/rfc7721) - Security and Privacy Considerations for IPv6 Address Generation Mechanisms**: This RFC discusses the security and privacy implications of different IPv6 address generation mechanisms, including SLAAC, privacy extensions, and CGAs. It provides recommendations for mitigating potential risks and improving privacy protection.

**[IPv6 Cryptographically Generated Address: Analysis, Optimization and Protection](https://www.researchgate.net/publication/350518202_IPv6_Cryptographically_Generated_Address_Analysis_Optimization_and_Protection)**:  This paper delves into the details of CGAs, analyzing their security and performance characteristics. It proposes optimizations to improve the efficiency of CGA generation and suggests additional security measures to strengthen the protection they offer.

**[IPv6 Bitcoin-Certified Addresses, Mathieu Ducroux](https://arxiv.org/pdf/2311.15842)**: proposes mechanism for enhancing the security and privacy of IPv6 addresses by leveraging the Bitcoin blockchain.

In essence, BCAs are IPv6 addresses where the interface identifier is derived from a Bitcoin address.

## How could this be beneficial?

If we can think of ethereum ecosystem as one big VPN where chains are subnet addressable that potentially solves fragmentation issues, allowing to use already established discovery protocols to route traffic between different nodes, use features like [multicast](https://en.wikipedia.org/wiki/Multicast_address) etc.

## Replies

**Mirror** (2024-06-16):

I agree with your point that using IPv6 interface identifiers to identify nodes in a P2P network can simplify node discovery and communication. Adding some test data might be beneficial. The hierarchical structure and auto-configuration features of IPv6 addresses are known to be effective and can help improve address allocation and management for Ethereum nodes.

Here are some additional thoughts, not limited to Ethereum:

- Blockchain Network Interoperability: A multi-chain interconnect architecture similar to IPv6 can enhance interoperability between different blockchain networks, reducing the problem of isolated chains.
- Dynamic Node Allocation: Using IPv6’s auto-configuration and dynamic address allocation features can enable dynamic management of Ethereum nodes, increasing network flexibility and adaptability.
- Enhanced Security Model: Combining blockchain and IPv6 encryption technologies can create a more secure and reliable model for node authentication and communication.
- Cross-Chain Communication: Drawing an analogy to IPv6 multicast and broadcast technologies, efficient cross-chain communication protocols can be designed to facilitate the execution and data sharing of cross-chain smart contracts.

---

**peersky** (2024-06-23):

Ultimately blockchain must “come down” from it’s abstraction in to physical layer. DePIN is a fancy word for it, however, eventually it’s a big telecom companies that must start entering market in order to make adaption really global.

It would be much easier for them to think in terms of “hey these blockchain guys are those who finally figured out really power use-case for IPv6”

