---
source: magicians
topic_id: 14569
title: A Proposal of on-chain verifiable Social Identity 2 Factor Authentication
author: yyd106
date: "2023-06-04"
category: EIPs
tags: [erc]
url: https://ethereum-magicians.org/t/a-proposal-of-on-chain-verifiable-social-identity-2-factor-authentication/14569
views: 736
likes: 0
posts_count: 1
---

# A Proposal of on-chain verifiable Social Identity 2 Factor Authentication

## Background

With the introduction of new standards like Account Abstraction (AA) and the growing adoption of Multi-Party Computation (MPC), wallets and DApps are able to utilize features such as Google, Email, and SMS two-factor authentication (2FA). These advancements create a seamless and user-friendly environment that mirrors the Web2 experience, thereby easing the adoption process for users.

### Current Issues with the Social Account Authentication in Web3

In the current Web3 landscape, the authentication process for users’ social accounts often relies on off-chain verification methods to kick-start on-chain transactions. This method sees a significant portion, ranging from one-third to half, of the on-chain signatures sourced from third-party entities, typically wallets. These include various types of wallets, like AA, Multi-sig, and MPC wallets that provide social authentication. However, the results of these wallets’ off-chain user authentication processes aren’t independently verifiable. This reality is the remaining centralized element in an otherwise decentralized system.

A further pressing concern related to the use of social accounts in the Web3 ecosystem is privacy. When a user authenticates their social account to a Web3 wallet, the wallet gains access to the user’s information, inadvertently becoming a centralized collector of user data. This access also leads to a merging of user information between Web2 and Web3. Such widespread collection and consolidation of user data can potentially expose users’ identities and assets, putting the security and privacy inherent in the Web3 world at risk. These challenges highlight the critical need for truly decentralized and privacy-focused solutions in Web3’s user authentication processes.

## The Proposed Paradim: Decentralized Provers for Social Account Authentication

Given the aforementioned challenges, a mechanism in the authentication process that generates a proof in a decentralized manner would be able to remove the dependency on a single centralized entity for validation. The proof it generates can be independently verified on-chain, aligning with Web3’s principles of trustlessness and on-chain verifiability. This approach of employing a decentralized prover strengthens aspects of privacy, speed, and reliability in the authentication process, all of which are pivotal for enhancing user experience and security within the Web3 ecosystem.

### Principles of Social Account Authentication in Web3

Several principles emerge that should guide the design of a Web3 native social account authentication protocol, particularly in its capacity as a Decentralized Prover (Fig. 1).

- On-chain Verifiability: The authentication process must yield outcomes that are verifiable on-chain. Once successfully verified, these outcomes should directly initiate on-chain transactions, ensuring a closer alignment with the principles inherent in Web3 native systems.
- Privacy: The authentication result should obscure or hash the user’s Web2 account, such as their email or Google account. Since this account acts as the link between Web2 and Web3 identities, it will safeguard the user’s personal and financial security.
- Speed: Social login and social 2FA should be quick to minimize any substantial impact on the user experience.
- Trustlessness: The authentication result and the corresponding proof generated should be decentralized, eliminating the reliance on any single authenticator.

[![2fa](https://ethereum-magicians.org/uploads/default/optimized/2X/7/717ede76c5f25f3a2e32187bb0bc67511d0e1f6d_2_655x500.png)2fa4800×3663 489 KB](https://ethereum-magicians.org/uploads/default/717ede76c5f25f3a2e32187bb0bc67511d0e1f6d)

## Using Hybrid-ZK for Proof Generation

Thanks to Zero-Knowledge (ZK) technology, it can reflect off-chain social account authentication on-chain in a completely decentralized manner. However, such proofs often require computation times ranging from tens to hundreds of hours with existing technology. This cost makes it impossible to directly use ZK technology in 2FA scenarios.

[Hybrid-ZK (Zero-Knowledge)](https://dauthnetwork.medium.com/hybrid-proofs-bridging-the-gap-for-decentralized-social-account-authentication-in-web3-8fc9fc8db51a) is a proof algorithm designed for social account verification, solving the costly and time-consuming issues associated with Zero-Knowledge (ZK) in two-factor authentication (2FA) scenarios. Using Hybrid-ZK as a decentralized prover, it can meet all the requirements of the new onchain 2FA paradigm based on social accounts.

We’re eager for your comments!
