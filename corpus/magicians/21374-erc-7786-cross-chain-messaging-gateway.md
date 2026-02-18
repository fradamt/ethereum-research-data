---
source: magicians
topic_id: 21374
title: "ERC-7786: Cross-Chain Messaging Gateway"
author: Amxx
date: "2024-10-14"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-7786-cross-chain-messaging-gateway/21374
views: 1160
likes: 18
posts_count: 9
---

# ERC-7786: Cross-Chain Messaging Gateway

Official discussion thread for [Add ERC: Cross-Chain Messaging Gateway by Amxx · Pull Request #673 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/673)

## Replies

**philippecamacho** (2024-12-06):

What is the purpose of the return argument (bytes4) in `executeMessage`?

---

**frangio** (2024-12-06):

This is to mitigate selector clashes, to make sure the receiver acknowledges the protocol it’s engaging in.

---

**philippecamacho** (2024-12-10):

What would be an example of an attack / things going wrong if the Gateway does not check the return value of `executeMessage`?

---

**philippecamacho** (2024-12-11):

I think I get it now, this is for ensuring that the Destination Gateway only can call the `executeMessage` function of the receiving application and not something else.

---

**ellie** (2024-12-12):

I love this ERC!

This ERC uses a ‘push’ mechanism rather than a ‘pull’ mechanism for messaging.  In my mind, a ‘push’ mechanism like the one described essentially uses a ‘pull’ mechanism under the hood - Whoever is calling the `executeMessage` function is pulling the message from the `Destination Gateway`.  I don’t think there’s anything wrong with either approach; I just find it to be a useful mental model.

---

**ernestognw** (2025-01-07):

Links to reference implementation with Axelar Network and audits:

- Audit
- AxelarGatewayBase
- AxelarGatewayDestination
- AxelarGatewayDuplex
- AxelarGatewaySource
- ERC7786Receiver

---

**u59149403** (2025-05-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amxx/48/1647_2.png) Amxx:

> Official discussion thread for Add ERC: Cross-Chain Messaging Gateway by Amxx · Pull Request #673 · ethereum/ERCs · GitHub

ERC contains this text: “The sender account (in the source chain) and receiver account (in the destination chain) MUST be represented using CAIP-10 account identifiers”. Unfortunately CAIP-10 for Ethereum addresses ( [EIP155 Namespace, aka EVM Chains - Addresses | Chain Agnostic Namespaces](https://namespaces.chainagnostic.org/eip155/caip10) ) contains this: “Anywhere [“Postel’s Law”](https://www.rfc-editor.org/rfc/rfc760#section-3.2) can apply, implementers SHOULD produce checksum-case secure addresses (whether in CAIP-10 or native format), and SHOULD accept both checksum case and legacy lowercase addresses, except where the security concerns of the particular usecase outweigh interoperability”.

In other words, CAIP-10 for Ethereum doesn’t contain definitive answer whether address should be lowercase or EIP-55 encoded. I think this is bad, so I reported this to CAIP: [CAIP-10 and CAIP-19: mandate case-normalization · Issue #351 · ChainAgnostic/CAIPs · GitHub](https://github.com/ChainAgnostic/CAIPs/issues/351) . But, as well as I understand, CAIP editors don’t plan to change anything here.

So, ERC-7786 should make its own decision here.

Also, another option may be to use CAIP-50 instead (it is binary) or CAIP-350 a. k. a. ERC-7930 (it is binary, too) ( [New CAIP profile: interoperable address binary specification by 0xteddybear · Pull Request #350 · ChainAgnostic/CAIPs · GitHub](https://github.com/ChainAgnostic/CAIPs/pull/350) , [ERC 7930: Interoperable Addresses](https://ethereum-magicians.org/t/erc-7930-interoperable-addresses/23365) )

---

**frangio** (2025-08-22):

This ERC is now in Last Call.

