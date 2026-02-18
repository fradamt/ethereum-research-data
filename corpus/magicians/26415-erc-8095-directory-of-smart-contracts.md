---
source: magicians
topic_id: 26415
title: ERC-8095 directory of smart contracts
author: joseluu
date: "2025-11-04"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-8095-directory-of-smart-contracts/26415
views: 168
likes: 6
posts_count: 4
---

# ERC-8095 directory of smart contracts

Dear all,

We are proposing a new ERC for a smart-contract whitelist management infrastructure.

The intent is that recognized authorities will deploy one or several such smart contracts to allow vetted actors to register and update themselves their smart-contract addresses and statuses. The intended effect is to protect the users of the smart-contract by allowing them to verify the authenticity of the addresses.

Full proposal: [ERCs/ERCS/erc-8095.md at master · joseluu/ERCs · GitHub](https://github.com/joseluu/ERCs/blob/master/ERCS/erc-8095.md)

Below are the Abstract and Motivation parts of the draft

Looking forward to your thoughts and improvements

## Abstract

This ERC is an **administered blockchain whitelist** addressing the proliferation of addresses by ensuring their authenticity for important transactions. It allows an organisation, called a **registrant**, to list the valid smart contract addresses it has deployed and it operates. Once an administrator of the recognized authority approves a registrant, that registrant can then record their service-related smart contract addresses in the **“references” list**. Overall this ERC facilitates on-chain verification and the identification and management of smart contract ecosystems.

## Motivation

The rapid proliferation of smart contract addresses poses a challenge to users  calling to implement robust mechanisms for **authenticity verification** for any transactions using them. This proposal aims to standardize a type of **administered blockchain whitelist**, addressing this issue by providing a structured solution for managing trust on-chain. The proposal for newcommers as well as for seasonned users will greatly facilitate and bring certainty to the “do your homework” address validation phase.

To achieve the goals to have both a decentralized administration of the whitelist while also having the ability to be trusted by the users we have a design where a trusted supervisor delegates the contracts management to vetted actors or operators.

The smart-contract operators, known as **registrants**, securely expose and maintain the valid smart contract addresses that they operate. Through an off-chain process, administrators of a recognized authority approve registrants using its own criteria, the operators then gain the ability to record their service-related smart contracts addresses in a dedicated **“references” list**.

In terms of automation, the directory allows **on-chain verification** allowing:

- smart wallets to check and validate the addresses upon usage or
- other smart contracts to perform addresses checks within their code possibly using standardized mechanisms

Information is maintained by the stake holders and therefore always uptodate.

## Replies

**vitali_grabovski** (2025-11-05):

Hello,

If the administrator is compromised, what happens to the registry? Do all records automatically become compromised as well? If so, consider adding protection using an *m-of-n* approach (for example, via [EIP-712](https://eips.ethereum.org/EIPS/eip-712)). This way, a single compromised administrator would not be sufficient to compromise the system.

Also, there are similar standards (eg [EIP-6224](https://eips.ethereum.org/EIPS/eip-6224)).

Do you think a comparison with these will help highlight how your approach differs and where this specific ERC could help?

---

**joseluu** (2025-11-05):

Thanks for the comments. EIP-6224 escaped my scan, I will look into it.

If the administrator is compromised it can either

- revoke the registrants (disableRegistrant) which would invalidate their smart-contracts addresses (called references)
- create a registrant under his control and then register contracts addresses that will fool users.

However, see URI cross references under **Security considerations**, when the initial administrator notices the compromission it will dereference the registry address in its URI metadata thus making it shown as invalid.

The same protection by URI cross reference applies to the any of the registrants that may have been compromised.

Users of this contract with write access (deployer or registrants) are expected to treat the security of this contract with the same security caution as their asset bearing contracts.

As for improving the signature process using an m-of-n signature process, this can of course be added in the **Optional Features** paragraph

---

**joseluu** (2025-11-07):

## Comparison with ERC-6226

While both ERCs maintain lists of contract addresses, there are several key differences:

ERC-6226 is geared towards the technical management by an actor (the deployer) of a set of related smart contracts  forming a protocol.

This ERC is designed to inform users about the contracts for the purpose of countering scams. It shows the authorship, version, and status of the listed contracts. The responsibility for maintaining the contract lists is decentralized among the registrants, each of whom is an actor responsible for their respective contracts. The contracts do not need to be technically related or form a protocol; however, they must be under the control of the registrant, who takes responsibility for their purpose and behavior by having listed them. There is a list of registrants vetted by the issuer of this ERC contract; therefore, there is an additional layer for maintaning the list of the registrants.

