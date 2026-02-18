---
source: magicians
topic_id: 1468
title: "ERC Proposal: LDGRToken - A compatible security token for issuing and trading SEC-compliant securities"
author: johnshiple
date: "2018-09-25"
category: EIPs
tags: [security-token]
url: https://ethereum-magicians.org/t/erc-proposal-ldgrtoken-a-compatible-security-token-for-issuing-and-trading-sec-compliant-securities/1468
views: 3497
likes: 0
posts_count: 1
---

# ERC Proposal: LDGRToken - A compatible security token for issuing and trading SEC-compliant securities

We recently submitted a proposal for [LDGRToken](https://github.com/StartEngine/EIPs/blob/master/EIPS/eip-ldgrtoken.md), an ERC-20 compatible token that complies with the new Securities Act Regulations: Regulation Crowdfunding, Regulation D, and Regulation A.

**Abstract**

LDGRToken facilitates the recording of ownership and transfer of securities sold under the new Securities Act Regulations. The issuance and trading of securities is subject to the Securities Exchange Commission (SEC) and specific U.S. state blue sky laws and regulations.

LDGRToken manages securities ownership during issuance and trading. The Issuer is the only role that should create a LDGRToken and assign the RTA. The RTA is the only role that is allowed to execute LDGRToken’s mint, burnFrom, and transferFrom functions. No role is allowed to execute LDGRToken’s transfer function.

We welcome all feedback, commentary, and discussions.

Here is our ERC proposal: https://github.com/ethereum/EIPs/pull/1450
