---
source: magicians
topic_id: 13232
title: "EIP-6662: AA Account Metadata for Authentication"
author: dongshu2013
date: "2023-03-09"
category: EIPs
tags: [erc, auth]
url: https://ethereum-magicians.org/t/eip-6662-aa-account-metadata-for-authentication/13232
views: 3527
likes: 9
posts_count: 12
---

# EIP-6662: AA Account Metadata for Authentication

pull request: [Add EIP-6662: AA Account Metadata](https://github.com/ethereum/EIPs/pull/6662)

---

## eip: 6662
title: AA Account Metadata For Authentication
description: An ERC-4337 extension to define a new authentication model
author: Shu Dong (), Zihao Chen (), Peter Chen ()
discussions-to:
status: Draft
type: Standards Track
category: ERC
created: 2023-03-09
requires: 712, 4337, 4804

## Abstract

This ERC proposes a new **IAccountMetadata** interface as an extension for ERC-4337 to store authentication data on-chain to support a more user-friendly authentication model.

## Motivation

In this proposal, we propose a new **IAccountMetadata** interface as an extension for ERC-4337 **IAccount** interface. With this new interface, users can store authentication data on-chain through one-time publishing, allowing dApps to proactively fetch it from the chain to support a more flexible and user-friendly authentication model. This will serve as an alternative to the current authentication model where users need to log in with a wallet every time and push account-related information to dApps by connecting the wallet in advance.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

### Authentication Flow

[![Authentication Flow](https://ethereum-magicians.org/uploads/default/optimized/2X/1/1fbd3f7c22e590afdc49313108a16c5a6b214a4c_2_690x325.png)Authentication Flow1300×613 16.9 KB](https://ethereum-magicians.org/uploads/default/1fbd3f7c22e590afdc49313108a16c5a6b214a4c)

In the new authentication workflow, users use AA compatible smart contract accounts as their wallet addresses. **Authenticator** could be anything but holding the private key to sign users’ operations. For example, it can be an offline authenticator mobile app or an online cloud service. **Relay** is an online service responsible for forwarding requests from dApps to the Authenticator. If the authenticator is online, it can play the role of Relay service and listen to dApps directly.

### Interface

To support the new authentication workflow, this ERC proposes a new **IAccountMetadata** interface as an extension of **IAccount** interface defined by ERC-4337.

```auto
interface IAccountMetadata {
  struct AuthenticatorInfo {
    // a list of service URIs to relay message from dApps to authenticators
    string[] relayURI;
    // a JSON string or URI pointing to a JSON file describing the
    // schema of AuthenticationRequest. The URI should follow ERC-4804
    // if the schema file is stored on-chain
    string schema;
  }

  function getAuthenticationInfo() external view returns(AuthenticatorInfo[] memory);
}
}
```

The relay endpoint should accept an AuthenticationRequest object as input. The format of the AuthenticationRequest object is defined by the schema field at AuthenticationInfo.

Following is a schema example which supports end to end encryption, where we pack all encrypted fields into an encryptedData field. The symbol **“$e2ee”** indicates that the field is encrypted and the encrypted value is stored at the encryptedData field. Here we only list three basic fields but there may be more fields per schema definition.

```auto
{
    "title": "AuthenticationRequest",
    "type": "object",
    "properties": {
        "entrypoint": {
            "type": "string" | "$e2ee",
            "description": "the entrypoint contract address",
        },
        "chainId": {
            "type": "string" | "$e2ee",
            "description": "the chain id",
        },
        "userOp": {
            "type": "object" | "$e2ee",
            "description": "UserOp defined by ERC-4337 without signature",
        },
        "encryptedData": {
            "type": "string",
            "description": "contains all encrypted fields"
        },
    }
}
```

## Rationale

To enable the new authentication workflow we described above, dApp needs to know two things:

1. Where is the authenticator? This is solved by the relayURI field in struct AuthenticationInfo. Users can publish the uri as the account metadata which will be pulled by dApp to do service discovery.
2. What’s the format of AuthenticationRequest? This is solved by the schema field in struct AuthenticationInfo. The schema defines the structure of the AuthenticationRequest object which is consumed by the authenticator. It can also be used to define extra fields for the relay service to enable flexible access control.

### Relay Service Selection

Each authenticator can provide a list of relay services. dApp should pull through the list of relay services in order to find the first workable one. All relay services under each authenticator must follow the same schema.

### Signature Aggregation

Multisig authentication could be enabled if multiple AuthenticatorInfos are provided under each smart contract account. Each authenticator can sign and submit signed user operations to bundler independently. These signatures will be aggregated by the Aggregator defined in ERC-4337.

### Future Extension

The **IAccountMetadata** interface could be extended per different requirements. For example, a new alias or avatar field could be defined for profile displaying.

## Security Considerations

### End to End Encryption

To protect the user’s privacy and prevent front-running attacks, we should keep the data encrypted during transmission from dApps to authenticators. This could be done by adopting the JWE (JSON Web Encryption, RFC-7516) method. Before sending out AuthenticationRequest, we generate a symmetric CEK(Content Encryption Key) to encrypt fields with end to end encryption enabled, then encrypt the CEK with the signer’s public key. dApp will pack the request into a JWE object and send it to the authenticator through the relay service. Relay service has no access to the end to end encrypted data since only the authenticator has the key to decrypt the CEK.

### Signing

We will follow the EIP-712 standard to improve the usability of off-chain message signing.

## Backwards Compatibility

The new interface is fully backward compatible with ERC-4337.

## Copyright

Copyright and related rights waived via CC0.

## Replies

**dror** (2023-03-12):

This is a nice possible extension, but goes against the core spirit of ERC4337, which is full decentralization - each contract is expected to supply its own centralized url for authorization.

The idea itself is not bad - but it is not general.

Also, there are different type of transactions, which might use different authentications. Your model supports a single authentication per wallet.

We do believe that major number of wallets will try to be decentralized - that is, not rely on external service, maybe except for recovery

Also, there is no mention how the actual on-chain validation is done with relation to the "Authenticator’

---

**dongshu2013** (2023-03-12):

Thanks for your feedbacks!

> This is a nice possible extension, but goes against the core spirit of ERC4337, which is full decentralization - each contract is expected to supply its own centralized url for authorization.

A: May I ask what do you mean by “centralized url”? The url is stored on-chain so the storage is decentralized. The relay service itself can be centralized, federated or completely decentralized. For example, each user can set up their own relay service at their home router(e.g. through edge computing), or we can build a decentralized relay service network serving all users. In the current version, we leave the choice to the user.

> The idea itself is not bad - but it is not general.
> Also, there are different types of transactions, which might use different authentications. Your model supports a single authentication per wallet.

A: We updated our EIP per your feedback to support multiple authenticators per smart contract account. Each authenticator can have their own authentication strategy so it’s flexible enough to support different authentications. In the latest version, we also support multiple relay URIs per authenticator so users can diversify their choices.

> We do believe that major number of wallets will try to be decentralized - that is, not rely on external service, maybe except for recovery

A: We believe the “Wallet” concept itself brings too much confusion for users with no crypto/blockchain background so our goal is to provide a more user-friendly authentication model without wallet involved. There is always a tradeoff, since we want to get rid of wallets from the authentication workflow, we need to introduce an extra external service. However, the external service could be completely decentralized per our explanation above.

> Also, there is no mention how the actual on-chain validation is done with relation to the "Authenticator’

A: Authenticator is just a private key container to sign transactions. How on-chain validation is done is defined by the IAccount interface at ERC-4337. The implementation of the on-chain validation falls into the scope of ERC-4337 and is not the focus of this EIP.

---

**dongshu2013** (2023-03-12):

Some more contexts to help people to understand our proposal:

We have been thinking “why wallet is needed to login dApps?”. Is it possible for user to login all dApps, including future ones, automatically? then we came up with the idea that, instead of let user login dApps, can we let dApps to find users instead?

Following the thoughts, we decompose today’s “Wallet” into three independent components: the smart contract account as the identity layer(previous public address), the authenticator as the signer(previous private key) and the relay service(to bridge dApps and offline authenticators). In the new model, users don’t have to connect wallet anymore. Instead, tx/signature requests will be pushed to user’s mobile app(either an authenticator app or a wallet) for users to confirm/approve. Users will only need to publish authentication information once, after which they will be able to login all dApps.

---

**xinbenlv** (2023-03-13):

Hi [@dongshu2013](/u/dongshu2013) glad to see this new proposal.

This proposal reminded me about a proposal that [@frozeman](/u/frozeman)  shared with me and seems in somewhat related to each other.

- ERC-725
- LSP0 - ERC725 Account | LUKSO Tech Documentation
- LSP3 - Universal Profile Metadata | LUKSO Tech Documentation

Are you aware of these two standards? Do you want to consider reach out for potential collaborations?

---

**zihaoccc** (2023-03-13):

[@xinbenlv](/u/xinbenlv) Thx for your comments and for sharing the info. Our team definitely is seeking and welcoming all potential possible collaboration. Next step we will spend time on those proposals, try to understand as much as possible the starting point and motivation to find the commonalities between us, and use them as a starting point for potential collaboration discussions.

---

**dongshu2013** (2023-03-13):

Hey [@xinbenlv](/u/xinbenlv) thanks for flagging the EIP out. I was not aware of it before but I just read through the doc and following are my thoughts:

EIP-6662 focus more on the concrete data type of the AuthenticatorInfo object and the new authentication model powered by it, so we don’t really care how the data is stored. The way to store/read the data could be separated from the detailed data schema definition and use cases. That is to say, we can keep this EIP for AuthenticatorInfo object definition and corresponding new authentication model, but re-use ERC725 for data read/write.

To re-use the interface, we can replace the **getAuthenticationInfo** function with the general **getData** function defined at ERC725Y. A new predefined data key at **LSP3-UniversalProfile-Metadata** could be added as following:

```auto
{
  "name": "eip6662.AuthenticatorInfo[]",
  "key": "0x4469e57160c56adaa536cfef547ed123246117cf4efdda447289d97315343be4",
  "keyType": "Array",
  "valueType": "bytes",
}
```

dApps will need to parse the bytes to AuthenticatorInfo object before consuming.

One potential problem of ERC725 is that ERC725 is designed for smart contract following ERC173(i.e. each contract has a EOA owner). It is not the assumption of  ERC-4337 smart contract accounts anymore. We need a more general interface to support signature based verification instead of simple **onlyOwner** modifier. (One trick we can do to support existing ERC725Y interface is to set the owner of the contract as itself and use UserOp to do **address(this).call()** to set the data but it will introduce extra function call).

Anyway, we are open to collaborate with others to make it happen! I would appreciate it if you can help to connect us : )

---

**qzhodl** (2023-03-13):

Nice EIP-4337 extension! Actually, in the context of AA, the wallet concept is a little out of date because the smart contract holds the asset, and the private key that the users hold plays an authenticating role. I totally agree that we should rename it to Authenticator.

Can the existing wallet (like Metamsk, imToken, etc.) be an authenticator or a relayer? Making the established players easier to support may make this EIP more popular ![:grinning:](https://ethereum-magicians.org/images/emoji/twitter/grinning.png?v=12)

---

**xinbenlv** (2023-03-13):

[@frozeman](/u/frozeman) it seems EIP-6662 poses a solution related to the direction that you’ve shared a similar idea about keeping authentication in the account (universal profile in your word). Love to get your idea on this!

---

**dongshu2013** (2023-03-13):

Thanks! That’s exactly what we are thinking about! Technically all wallets serve as the purpose of authenticator and we are willing to engage more wallets. We are exploring how to fit Metamask and WalletConnect in our new setup

---

**sk1122** (2023-06-05):

Nice concept!

As I understand, this solution provides a universal profile for all smart wallet users which dApps can use to authenticate users with?

This will work very well if paired with session keys, generate a onchain session key and let dApps access that profile for limited time which can be configured in the session key logic itself!

---

**dongshu2013** (2023-09-01):

hey sorry for the late late late response but yes, it can definitely combined with session keys. We are working on zk-based session key registration and we hope combing it with current the authentication data we can improve the user experience into next level.

