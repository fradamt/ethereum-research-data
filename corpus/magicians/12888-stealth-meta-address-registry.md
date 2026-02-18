---
source: magicians
topic_id: 12888
title: Stealth Meta-Address Registry
author: Nerolation
date: "2023-02-09"
category: EIPs
tags: [erc]
url: https://ethereum-magicians.org/t/stealth-meta-address-registry/12888
views: 3323
likes: 7
posts_count: 12
---

# Stealth Meta-Address Registry

**Stealth Meta-Address Registry contract.** The standardization of [stealth address](https://vitalik.ca/general/2023/01/20/stealth.html) generation holds the potential to greatly enhance the privacy capabilities of Ethereum by enabling the recipient of a transfer to remain anonymous when receiving an asset. By introducing a central smart contract for users to store their stealth meta-addresses (consisting of a spending and a viewing public key), EOAs and contracts can programmatically engage in stealth interactions using a variety of stealth address scehemes.

This EIP builds upon [EIP-5564](https://github.com/nerolation/EIP-Stealth-Address-ERC/blob/main/eip-5564.md) which lays a very minimalistic standard to standardize the usage of different stealth address schemes (e.g. elliptic curve-based, lattice-based, ect).

The following repo is used for development:



      [github.com](https://github.com/nerolation/EIP-Stealth-Address-ERC/blob/main/eip-registry.md)





####



```md
---
eip: TODO
title: Stealth Meta-Address Registry
description: A registry to map addresses to stealth meta-addresses
author: Matt Solomon (@mds1), Toni Wahrstätter (@nerolation), Ben DiFrancesco (@apbendi), Vitalik Buterin
discussions-to: TODO
status: Draft
type: Standards Track
category: ERC
created: 2023-01-24
---

## Abstract

This specification defines a standardized way of storing and retrieving an entity's stealth meta-address, by extending [EIP-5564](./eip-5564.md).

## Motivation

The standardization of stealth address generation holds the potential to greatly enhance the privacy capabilities of Ethereum by enabling the recipient of a transfer to remain anonymous when receiving an asset. By introducing a central smart contract for users to store their stealth meta-addresseses, EOAs and contracts can programmatically engage in stealth interactions using a variety of stealth address scehemes.

```

  This file has been truncated. [show original](https://github.com/nerolation/EIP-Stealth-Address-ERC/blob/main/eip-registry.md)

## Replies

**metony** (2023-08-14):

gm [@Nerolation](/u/nerolation)

This is Antonio from the Stealth Safes / Sefu team. I’ve been delving deep into Stealth Addresses and also looked into this proposed EIP. I wanted to highlight a few doubts and questions that arose in the process.

1. My first doubt revolves around the concept of the schemeId. If I’ve grasped it correctly, the essence of the schemeId is focused on the creation of stealth addresses and their retrieval and not necessarily the origin of the meta-stealth keys used. Drawing from the current implementation in Umbra.js, a signature is required during key generation, which is later used for key derivation. Shouldn’t the signed message be defined within the schemeId or be associated in some way? Imagine diverse protocols building atop Stealth Addresses. When a wallet syncs with a dApp and checks the registry, it might identify a previously registered meta-stealth address. But how can we discern the originating signed message for those keys? I think a metaGenerationScheme function (or similar) should be included in the schemeId definition. If this request should be move into EIP-5564 discussion, correct me.
2. Question not directly linked to the technicalities: When do you envision transitioning the EIP from a draft to a final, stable implementation, and consequently deploying the registry as a definitive singleton?
3. I’m truly captivated by the idea that an EIP-6538 compatible registry should exist as a singleton within a chain. However, how do we ensure this uniqueness? I foresee that once a registry is established, others might follow suit.

I’d greatly appreciate your insights on the aforementioned points.

Thanks,

---

**bendi** (2023-08-15):

Hi [@metony](/u/metony), thanks for the questions. These are all really great.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/metony/48/10254_2.png) metony:

> I think a metaGenerationScheme function (or similar) should be included in the schemeId definition. If this request should be move into EIP-5564 discussion, correct me.

In creating the standard, we wanted to make things as lightweight and simple as possible, to make adoption and conformity easy, and to avoid foreclosing on usecases we can’t currently imagine. I think the essence of your question here is whether we’ve erred *too far* in that direction, so as to not include enough in the standard to allow for easy interoperability. I think this is a very fair question and one worth reflecting on more. I’m curious what [@Nerolation](/u/nerolation) and [@mds1](/u/mds1) think about that.

One argument would be that the functionality you described better belongs as convention, and/or in an extension EIP of some kind.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/metony/48/10254_2.png) metony:

> I’m truly captivated by the idea that an EIP-6538 compatible registry should exist as a singleton within a chain. However, how do we ensure this uniqueness? I foresee that once a registry is established, others might follow suit.

Our current plan is to rely on the standard create2 deployer which exists across most chains. This, along with the eventually-finalized bytecode of the registry contract, will determine an address that will act as the standard’s “official” registry across all chains.

Of course, there’s nothing we can do if someone clones the registry and tries to create a shelling point around their alternative. Nor would we want to. Such is the nature of permissionless systems. That said, if we do things right, the stanard registry should accrue some measure of network effects.

---

**metony** (2023-08-15):

Thanks for the answer!

I think your strategy to enforce, as much as possible, uniqueness across chains is a perfect one. If then the registry is cloned, I totally understand there’s nothing you can do. This is why we’re in an open system ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)  But I agree that’s hard, as there’s not a direct monetary incentive in doing so.

Regarding key generation, looking forward for [@Nerolation](/u/nerolation) and [@mds1](/u/mds1) answers too!

---

**metony** (2023-08-28):

I’ve been thinking more over this problem during the weekend and I came to a possible solution that changes close to nothing in the current EIP proposal, while increasing flexibility.

Recap:

- the issue we’re facing is around the key generation method - as two different services implementing Stealth Addresses can have two different key generation methods while using the same schemeId
- we should make the EIP flexible so that a user can utilize multiple services providing Stealth Addresses, potentially with different keys behind, all implementing the same schemeId

Looking at the current implementation of the EIP, I’d keep it as it’s now, but removing the following part:

`This MUST be a singleton contract, with one instance per chain.`

Along with point #4 in the [Rationale section](https://eips.ethereum.org/EIPS/eip-6538#rationale)

## Rationale

Having multiple registries deployed allows to have different key generation logic, as each registry maps a specific generation logic, created by the registry deployer.

For example, a company creating a wallet wants to derive keys directly from the seed phrase of the user, in a way that is not reproducible with a malicious signature. This is a completely different method compared (for example) to the current Umbra one, while still producing a key with a `schemeId` that could be the same as Umbra’s.

With this change, any stealth address provider (e.g. a wallet) can deploy an EIP-6538 compatible contract and use it as a registry. A regular user of the wallet would then be able, to use multiple stealth address services, such as Umbra and another wallet offering stealth address features. Of course, payments received using the Wallet system won’t be visible in Umbra UI and viceversa, unless the Wallet implements also the scanning of events with keys generated on Umbra (implementing also Umbra key generation method).

What do you think about this improvement?

---

**mds1** (2023-08-28):

It seems there are two questions that we’re blending together:

1. Given a recipient’s ordinary wallet address, how is the stealth-meta address (SMA) and it’s corresponding private keys derived?
2. Given a recipient’s ordinary wallet address, what are a sender’s options for sending them funds via a stealth address, i.e. how does the sender compute the stealth address and how does the recipient decrypt Announcement logs?

This ERC provides an answer to question 2 by mapping an address to a scheme ID to an SMA, this way a sender can look up all the scheme IDs available for a recipient and choose one to use. How the SMA was derived for the recipient doesn’t matter much from the sender’s perspective. Given that you know how to find/derive your own private keys, it also doesn’t matter from a scanning perspective.

But it does matter so a new app can help you scan for and withdraw funds—your comment does raise two good questions around this that the ERCs don’t currently address:

1. Should we standardize the options for deriving an SMA and its private keys from a wallet address?
2. The registry only supports a 1:1 mapping of address to SMA, but this doesn’t necessarily have to be the case—a user can have multiple SMAs for a given address. Should the ERCs support a 1:n mapping here, or stick with 1:1?

For question 3, we probably should, but this feels like a separate ERC since it’s a different scope. This is arguably not specific to just stealth addresses, as the ERC can answer the generic question of “how to generate app-specific private keys for a user”. Then, all apps and stealth address wallets—even wallets with native stealth address support—can use the same approach. Perhaps it’s something like “Sign this message to generate app-specific private keys for [APP_NAME] on chain [CHAIN ID]. Only sign this message for a trusted client”. (TBD how to robustly expand this to contract wallet users). It would also need to address how to mark a set of keys as compromised and generate new case.

For question 4, it sounds like you want to support a `1:n` mapping, but I’d push back that. In my opinion a `1:1` mapping is the most common use case, and I can’t think of a compelling reason to use a `1:n` mapping:

- If a user’s wallet does not have native stealth address support, then to avoid copying private keys into applications, signing a message to generate their keys and provide them to a trusted client to scan for/withdraw funds is the best approach. Signing multiple messages to generate multiple SMAs doesn’t add any privacy benefits (unless keys are leaked, but I don’t think that threat vector should be in scope for the ERCs).
- If a user’s wallet does have native stealth address support, and does not use the same signature to derive the SMA, then the wallet should expose RPC methods for apps to scan and withdraw funds. If the user wants to migrate to a new wallet that no longer has native stealth address support, they can sign a message to generate new keys and overwrite the old wallet-generated keys in the registry.

Deriving keys for the user in question 1 feels similar to hardware wallet derivation paths: Different apps may have different default derivation paths, and when you connect your hardware wallet to an app, you have to choose one or more derivation paths to show accounts for. It can be similar here, where you have to choose a message to sign, and/or choose to use the wallet’s regular public key, and/or choose an approach to derive it for contract wallets. In any of those cases, an app that wants you to scan for funds can support one or more of these key-derivation approaches, and may ask you choose one more approaches so it knows how to get your keys.

---

**metony** (2023-08-29):

Thank you so much for your reply, [@mds1](/u/mds1)

I fully agree with you on points 1, 2, and 3. Especially point #3, I think we should leave the standardization of options for deriving an SMA and its private keys to another ERC.

Regarding point #4, I’d like to offer a slight clarification around my proposal. I think we should allow for multiple registries, creating a `1:n` keys scenario, where the `n` keys for a given user are spread across `n` `1:1` registries. This approach would be akin to `ERC-20` or `ERC-721`, where anyone can bring in their implementations with their own logic, while adhering to a standard.

Allowing multiple registries to be deployed adds flexibility. For example, I might want to receive payments and share my viewing private key with a trusted service, while receiving other payments using a different viewing key that I don’t want to share. I know a user can accomplish this with two different addresses, but if we can establish a standard that works with just one address, I think that’s preferable.

Additionally, in a `1:1` scenario with a singleton registry, the user must remember which service they used to generate the keys. So when using a trusted party to assist in scanning payments, the user would need to specify which service they used.

Personally, I don’t envision a scenario with hundreds of registries deployed, but I do think there could be situations where a user may want 2 or 3 different MSAs, and a singleton registry can’t support this.

What do you think about it?

---

**bokkypoobah** (2023-12-26):

Hi [@Nerolation](/u/nerolation) , I’m doing some testing on the ERC-6538 registry and cannot retrieve the `registrant` field from the event logs:

```auto
event StealthMetaAddressSet(
    bytes indexed registrant, uint256 indexed scheme, bytes stealthMetaAddress
  );
```

Because `registrant` is of type `bytes`, a hash of `registrant` is stored in the event log, instead of registrant. This is a similar to the encoding of strings in event logs.

Would the type `bytes32` be more appropriate for the `registrant` field?

---

**zemse** (2024-01-04):

Or if registrant could possibly be > 32 bytes, `bytes registrant` can be appended in the log data.

```auto
event StealthMetaAddressSet(
    bytes indexed registrant, uint256 indexed scheme, bytes stealthMetaAddress, bytes _registrant
  );
```

so that we also have the preimage of the topic.

---

**Nerolation** (2024-02-14):

First, as a data guy, I totally feel your pain.

Bytes decoding can be buggy but check out eth-abi or web3 (using eth-abi). You can use it to decode event topics + data into the demanded types.

The reason why it is bytes and not bytes32 is to allow many different cryptographic schemese to be developed around the same registry contract. E.g. post quantum secure keys might be much larger than 32 bytes.

EDIT: In the latest version, the registrant is in address format and not in bytes anymore. In the above, I mixed it up with the ephemeral public key.

---

**Nerolation** (2024-02-14):

Having it indexed allows better to search for it by enabling filtering. Furthermore it’s simpler to parse them from a topic instead of the data field.

---

**eawosika** (2024-12-04):

For those interested in understanding how ERC-6538 works under the hood, [2077 Research](https://research.2077.xyz/) created a deep dive on the standard: [ERC-5564 &amp; ERC-6358: Unlocking Privacy on Ethereum with Stealth Addresses](https://research.2077.xyz/erc-5564-erc-6358-unlocking-privacy-on-ethereum-with-stealth-addresses#practical-benefits-of-erc-5564-erc-6538)

