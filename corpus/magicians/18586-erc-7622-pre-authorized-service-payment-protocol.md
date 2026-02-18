---
source: magicians
topic_id: 18586
title: "ERC-7622: Pre-Authorized Service Payment Protocol"
author: bizliaoyuan
date: "2024-02-10"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-7622-pre-authorized-service-payment-protocol/18586
views: 753
likes: 0
posts_count: 1
---

# ERC-7622: Pre-Authorized Service Payment Protocol

[github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/252)














####


      `master` ← `bizliaoyuan:master`




          opened 04:47PM - 11 Feb 24 UTC



          [![](https://avatars.githubusercontent.com/u/5671437?v=4)
            bizliaoyuan](https://github.com/bizliaoyuan)



          [+226
            -0](https://github.com/ethereum/ERCs/pull/252/files)







When opening a pull request to submit a new EIP, please use the suggested templa[…](https://github.com/ethereum/ERCs/pull/252)te: https://github.com/ethereum/EIPs/blob/master/eip-template.md

We have a GitHub bot that automatically merges some PRs. It will merge yours immediately if certain criteria are met:

 - The PR edits only existing draft PRs.
 - The build passes.
 - Your GitHub username or email address is listed in the 'author' header of all affected PRs, inside <triangular brackets>.
 - If matching on email address, the email address is the one publicly listed on your GitHub profile.












## Abstract

This proposal introduces a protocol for implementing pre-authorization capabilities in ERC-20 token payments, while simultaneously facilitating the aggregation of token funds. Users deposit ERC-20 tokens into the contract, acquiring a total authorized balance that can be distributed to various service providers for expenditure. The protocol empowers users to pre-authorize specific service providers to deduct funds up to a predetermined limit, ensuring seamless and secure transactions. Additionally, users retain the ability to withdraw unutilized authorized balances, modify, or revoke authorizations for specific service providers as needed. Through this framework, the protocol enhances the efficiency, security, and flexibility of ERC-20 token payments within decentralized applications.

## Motivation

In the current Ethereum ecosystem, users encounter the inconvenience of needing to manually confirm each transaction when transferring funds to third parties. This becomes particularly cumbersome for services necessitating frequent micro-payments. Additionally, in certain DApps, there’s a desire to obtain user fund authorizations without relying on ERC-20’s approve method. This reluctance stems from the fact that approve does not involve placing funds in a trusted third-party entity.

To address this concern, there’s a proposal to introduce a third-party contract capable of receiving and managing authorized funds. These third-party entities could include reputable organizations, such as charities or authoritative institutions. By channeling authorized funds into a dedicated pool, these entities could generate charitable returns or facilitate community benefits.

Furthermore, there’s potential to implement governance mechanisms, such as DAO governance or transparent public oversight, for managing the list of authorized service providers. This would enhance trust and transparency, allowing users to dynamically manage their authorizations while ensuring the integrity of the service provider ecosystem. Through these enhancements, the proposed Pre-Authorized Service Payment Protocol not only streamlines transaction processes but also fosters trust, transparency, and community engagement within the Ethereum ecosystem.

## Specification

The protocol specifies the following key functionalities:

- registerServiceProvider(address serviceProvider): Allows service providers to register themselves.
- deregisterServiceProvider(address serviceProvider): Allows service providers to deregister themselves.
- authorizeServiceProvider(address serviceProvider, uint256 amount): Allows users to pre-authorize a specified amount of tokens to a service provider.
- revokeAuthorization(address serviceProvider): Allows users to revoke the pre-authorization given to a service provider.
- deductFunds(address user, uint256 amount): Enables service providers to deduct funds from a user’s account based on the authorization.
