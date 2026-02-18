---
source: magicians
topic_id: 11513
title: "EIP-5851: On-chain Verifiable Credentials"
author: GrandGarcon01
date: "2022-10-29"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-5851-on-chain-verifiable-credentials/11513
views: 3156
likes: 7
posts_count: 14
---

# EIP-5851: On-chain Verifiable Credentials

This standard defines the interface for issuing on-chain DID identifiers for the wallet address which have done their off-chain verification.

link of the documentation is [here](https://github.com/ethereum/EIPs/pull/5851) is currently under review and will be added as draft section.

we will also organize soon some workshops on this topic in order to get more feedback from the KYC providers and other use cases in the space in order to  get adoption of the standard that the DeFI desperately needs in order to comply with the standards like EBSI

## Replies

**kjhman21** (2022-11-07):

Hello, [@GrandGarcon01](/u/grandgarcon01). It looks like the EIP number is wrong.

5185 → 5851

---

**GrandGarcon01** (2022-11-07):

thanks for correction, this is changed . happy to address other queries that you might have

---

**Jooeys** (2022-11-07):

**EIP-5851: Zero-Knowledge KYC Certificates**, I really believe this could be a solution for reusable KYC and could be a good implementation of Proof of Identity to benefit everyone involved with regulations and compliance required scenarios.

However, centralization and decentralization in this world are not binary oppositions, they should coexist to serve all sovereign individuals. We need to obtain trusted public certificates (e.g., national identity cards and/or ePassports, resident permits, driving licenses and eSIM, etc.) from a centralized party like governments and financial institutions or corporations as an original identity certificate, from this source ID, to derivate a federated identity architecture to allow implementing zero-knowledge proof of identity in order to access a real trustless and permissionless blockchains to build trust from anonymous.

---

**zlace** (2022-11-08):

You could link the EIP here for ease of reference.

The diagram shows ERC6595 (I’m assuming refers to this EIP) needs to be updated.

---

**GrandGarcon01** (2022-11-08):

Apologies for the mismatch of the details . the EIP was recreated that’s why some of the details are being re-written . i will get the details corrected

---

**GrandGarcon01** (2022-11-08):

Thanks [@Jooeys](/u/jooeys)  for your great optimism,

but it will be great if you can define the specific specifications that we need to add in the standard. currently, we are modeling the standard based on the W3C DID standards with the possibility of the admins being able to adapt to the changes in the requirements and being uniquely recognizable across various platforms. if you have example of the jurisdictions and the usecases that we need to integrate, will be great to check out.

---

**SamWilsn** (2022-12-09):

We’re trying a new process where we get a volunteer peer reviewer to read through your proposal and post any feedback here. Your peer reviewer is [@kalloc](/u/kalloc)!

If any of this EIP’s authors would like to participate in the volunteer peer review process, [shoot me a message](https://ethereum-magicians.org/new-message?username=SamWilsn&title=Peer+Review+Volunteer)!

---

[@kalloc](/u/kalloc) please take a look through [EIP-5851](https://github.com/ethereum/EIPs/pull/5851) and comment here with any feedback or questions. Thanks!

Normally we don’t request peer review until the proposal has reached the Draft status (and its associated pull request is merged), but in this case I do not feel qualified to judge if the EIP is understandable by someone more familiar with the zero knowledge space.

---

**GrandGarcon01** (2022-12-09):

Thanks, [@SamWilsn](/u/samwilsn)  for the response and greetings [@kalloc](/u/kalloc).

Recently we are in process of restructuring the EIP standard  to  create verifiable claims rather than zero-knowledge focused standard, and thus you will not find the  **Specification** section which is up to date, we will do the changes this afternoon and will edit the details on this board also. thanks

---

**michelangelo** (2023-01-17):

We (https://togggle.io/) implemented this solution in partnership with Polygon ID, looking forward to do the same with you.

---

**GrandGarcon01** (2023-01-20):

Thanks [@michelangelo](/u/michelangelo)  for the response.

Happy to discuss further on personal channel.

Also we are going to organise some seminars with Ethereum Magicians and other projects interested in collaborating on  onchain / privacy preserving VC standards and will share the followup soon.

---

**tahpot** (2023-01-24):

Do you have a diagram showing the flow of how this is intended to be used? That would certainly help to explain how this EIP works.

Where does the root of trust lie? ie: Is the trust in the minter of the SBT or is there cryptographic data placed on chain that can be used to independently verify the credential?

KYC can have a lot of composable elements, especially when looking at the breadth of VC standards. This appears to be a simpler, cut down verification mechanism. Perhaps the name of the EIP should be more generic, but have KYC as a potential use case?

Is there a demo of this you can link to?

---

**GrandGarcon01** (2023-01-27):

Hi,

We do have a general workflow diagram of how its intended to be used in the case of providing KYC services for DeFI protocols [here](https://github.com/yuliu-debond/KYC_verifier-/blob/main/EIP/KYC%20standard%20work%20flow.pdf).

```auto
Where does the root of trust lie? ie: Is the trust in the minter of the SBT or is there cryptographic data placed on chain that can be used to independently verify the credential?
```

On this part maybe the author  [@yuliu-debond](/u/yuliu-debond)  can give more precise response. but in my understanding, it will be based on the minter of the SBT(that will be first onboarding the KYC identity of the wallet holder as shown in diagram link before).

```auto
KYC can have a lot of composable elements, especially when looking at the breadth of VC standards. This appears to be a simpler, cut down verification mechanism. Perhaps the name of the EIP should be more generic, but have KYC as a potential use case?
```

This is indeed you are correct, and indeed we have changed the name of the EIP to `On-Chain Verifiable Credentials`, thanks for the reminder and we will do the updating here also.

```auto
Is there a demo of this you can link to?
```

We are currently building a non custodial wallet, this will be launched most probably till Q1/Q2  2023.

---

**GrandGarcon01** (2023-03-09):

Hi ,

I think also there needs to be variable corresponding to whether the SBT status needs to be verified periodically or is issued for once for lifetime.  this distinction is needed in order the developers being more conscious in developing required logic for claimer to accordingly re-certify the user their claim as SBT based on the condition.

