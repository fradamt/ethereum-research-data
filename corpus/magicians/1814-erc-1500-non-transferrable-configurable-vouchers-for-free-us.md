---
source: magicians
topic_id: 1814
title: "ERC 1500: Non-transferrable, configurable vouchers for free usage of dApps"
author: jamslevy
date: "2018-11-05"
category: EIPs
tags: [ux, erc-1500]
url: https://ethereum-magicians.org/t/erc-1500-non-transferrable-configurable-vouchers-for-free-usage-of-dapps/1814
views: 873
likes: 0
posts_count: 1
---

# ERC 1500: Non-transferrable, configurable vouchers for free usage of dApps

## Abstract

An on-chain system for facilitating sponsored vouchers that can be redeemed on a specified contract but cannot be transferred or sold, and can be configured to require identity verification to prevent abuse or other factors.

When paired with a gas relayer `meta transaction` system such as the ones designed by the [meta cartel](https://twitter.com/meta_cartel), this system allows for new users without funds in their account to not only send transactions, but to purchase collectibles, make transactions on marketplaces, and other operations requiring both gas fees and additional funding.

Redeemed voucher funds are sent as a normal transaction from the redeeming user, and support for this system does not require any front-end dApp code or the contract code used by dApps to be modified.

## Motivation

The overall goal of providing a more simple and low-friction onboarding process for new users is one of the main challenges for Ethereum to substantially broaden its addressable audience. For those who do not already have cryptocurrency funds available to spend and would like to try one or more decentralized apps, the only option typically available to them is to go through a lengthy fiat onramp process where their bank details must be verified before a purchase of some initial funds can be completed.

While the use of gas relayers and meta transactions helps to reduce this friction for new users, there are a limited number of decentralized apps that only require gas fees. Many of the applications and use-cases of interest require additional funds beyond gas to acquire tokens or NFTs.

Meanwhile, dApp developers struggle to acquire new users amongst an increasingly large volume of apps to choose from.

This system helps both the new users and the app developers seeking additional ways of acquiring users, without requiring dApp developers to modify either their contract code or front-end code.

[More information in the EIP](https://github.com/ethereum/EIPs/issues/1500).
