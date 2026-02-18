---
source: magicians
topic_id: 13671
title: Eliminating the middleman from KYC verification of blockchain addresses
author: hurricane247
date: "2023-04-03"
category: EIPs
tags: [identity, kyc, verifiable-claims, self-sovereign-ident]
url: https://ethereum-magicians.org/t/eliminating-the-middleman-from-kyc-verification-of-blockchain-addresses/13671
views: 1052
likes: 4
posts_count: 3
---

# Eliminating the middleman from KYC verification of blockchain addresses

Tl:dr; The goal of this discussion is to create a verification standard which any dApp can use to check if a certain wallet address fulfills certain identity requirements. The underlying assumption is that the verification is done off-chain using real-life standardized W3C Verifiable Credentials e.g., national identity card or passport. Identity verification and linking with the wallet address is done decentrally without any centralized KYC provider.

# Background

In the past few years, there have been many regulations in the fintech space surrounding KYC of users. Most exchanges/dApps do this KYC in a centralized off-chain manner, creating identity honeypots. There have also been a lot of discussions regarding creating a decentralized, blockchain-native and privacy-preserving identification mechanism in the past months. Such a solution will not only provide dApps a chance to survive these new regulations but also enable plethora of new use cases e.g., under-collaterized lending, tokenization of real-life assets, mortgage lending using risk profiles of addresses etc.

Self-Sovereign Identity (SSI) provides the necessary building-blocks to create a peer-to-peer identity verification scheme based on standardized W3C verifiable credential models. There are ways now to get your real-life credentials like Passport, Identity Card in your SSI wallet (see [here](https://www.bundesdruckerei.de/en/innovation-hub/euid-digital-identity-electronic-wallet) and [here](https://verimi.de/presspost/verimi-app-wird-intuitives-id-wallet-fuer-personalausweis-fuehrerschein-und-eu-covid-zertifikate/)). Many European governments are now working on providing the national identity card as Verifiable Credentials. Using these credentials, one can create numerous Decentralized Identifiers (DIDs) and various proofs in a privacy preserving manner using selective disclosure, essentially putting users in control of their identity. More details can be read [here](https://medium.com/@plurality.web3/improving-kyc-processes-using-self-sovereign-identity-ab0f984e93d9).

There seems to be a huge potential in bringing SSI to the blockchain world thus enabling a blockchain-native decentralized identity solution.

# Goal

Any dApp that has identification requirements from its users can verify them on its own without the need of a centralized KYC provider.

In this way, identity honeypots will not be created and the identification mechanism will be according to the web3 ethos of decentralization and giving control back to users. Moreover, the dApps can easily secure themselves from any future identification regulations that might affect their business. [[link](https://www-theblock-co.cdn.ampproject.org/c/s/www.theblock.co/amp/post/223215/crypto-aml-rules-passed-meps)] [[link](https://www.bankingcircle.com/mica-regulation-what-does-it-mean-for-crypto-0113521)]

# How to achieve this goal?

The SSI world already has the building blocks available for issuing and verifying credentials against a DID. However, it is not Ethereum-blockchain-aware. If we make the SSI prover and verifier components blockchain-aware, we can combine these two worlds. The user can create SSI-based off-chain proofs and then sign it from its Ethereum wallet using EIP-712 signatures to link its SSI identity with its Ethereum identity.

Once the dApp’s verifier verifies the user’s claim in a peer-to-peer & off-chain fashion, it can let the dApp smart contract know about the verified addresses. There can be different ways to achieve this:

- The verifier can “allow” or “whitelist” the verified address so that the dApp smart contract can know which addresses are allowed or disallowed.
- The verifier can publish a zero-knowledge proof of verification to be consumed by the dApp smart contract, so that nobody can see a list of verified addresses

[![thoughts2](https://ethereum-magicians.org/uploads/default/optimized/2X/2/29eb2db9819d384434dede312c16edb9231cb66b_2_690x339.png)thoughts24086×2012 230 KB](https://ethereum-magicians.org/uploads/default/29eb2db9819d384434dede312c16edb9231cb66b)

# Problem Space

A new EIP can be created for such a verification contract which any dApp can use to check if a certain address is verified or not based on its identification requirements.

To achieve this goal, there are certain considerations:

- The issuance of credentials must happen off-chain because we want this to be compatible with standardized W3C credentials which will be issued by governments.
- The verification must happen off-chain: Verification process is complex and not suitable to be done on a smart contract. The credential details are also not on public blockchains since they are issued using SSI framework. Moreover, there can be Personally Identifiable Data in the proofs and processing them on-chain can lead to GDPR compliance problem.
- To link the proof with Ethereum address, EIP-712 seems to be the best fit since it can show structured data that needs to be signed. Proof data is also structure JSON so it seems like the best fit.
- The proof requirements must not be pushed on-chain as it can also lead to privacy concerns. For example, if it’s known that a certain dApp contract only allows people from US that have a bank account balance >100k$, and there is an address that’s allowed by that dApp, it might be a privacy concern for the wallet owner. What are the community’s thoughts on this?
- The verified addresses should be revocable if in case the dApp’s identification requirements change and the verified address no longer meets the criteria. OR the credential expired.

Looking forward for discussions and comments on the best way to achieve this.

## Replies

**cynic-1** (2023-04-10):

I guess the problem should be: how to verify SSI?

---

**hurricane247** (2023-04-10):

Well, you could the problem is how to put verified addresses on smart contract without losing trust, privacy factor and revocability.

I have been looking into possible solutions and one solution I am currently considering is usage of Semaphores because it can prove that an address belongs to a group with zero knowledge properties of privacy preservation and trust, and is also capable of revoking membership of addresses.


      ![image](https://docs.semaphore.pse.dev/img/favicon.ico)

      [docs.semaphore.pse.dev](https://docs.semaphore.pse.dev)



    ![image](https://docs.semaphore.pse.dev/img/social-media.png)

###



Overview










What do you think?

