---
source: magicians
topic_id: 14973
title: "EIP-7291: Purpose Bound Money"
author: orchid-dev
date: "2023-07-07"
category: EIPs
tags: [erc, pbm, purpose-bound-money]
url: https://ethereum-magicians.org/t/eip-7291-purpose-bound-money/14973
views: 2230
likes: 4
posts_count: 4
---

# EIP-7291: Purpose Bound Money

The  team is proposing to standardise the implementation of purpose-bound money (PBM) in an EIP. The aim is to provide a common specification for wallet players to be able to interact freely with PBM smart contracts issued by various PBM creators for various business use cases.

What are PBMs?

PBMs are a hybrid form of programmable payment and programmable money, which are bearer instruments, with self-contained programming logic and are transferrable between two parties without intermediaries.

What are the practical uses?

Purpose-bound money can be used to implement government disbursement tokens, shopping voucher tokens, prepaid tokens, rewards points token, purpose bound donation token, school allowance token etc. For additional information on PBM, please refer to:

- Project Orchid Whitepaper and media release
- PBM Technical Whitepaper and media release by Monetary Authority of Singapore (Singapore’s central bank and financial supervisory authority)
- Live Demo Videos from Singapore Fintech Festival 2022

What are our goals?

To develop a minimal interface that can promote interoperability between various payment market players. The proposed interface builds upon ERC-1155 to ensure widespread compatibility with existing wallets.

Our team would appreciate any comments on the proposal’s design, feasibility as well as any security concerns. As the proposal is in the draft stage, the proposal will continue to evolve as we receive comments from the community.

Github link:

https://github.com/ethereum/EIPs/pull/7292

## Replies

**vic** (2023-07-07):

Adding some other relevant links:

- Project Orchid Whitepaper and media release
- PBM Technical Whitepaper and media release by Monetary Authority of Singapore (Singapore’s central bank and financial supervisory authority)

The team is working on commercialising it, here’s a  [Live Demo Videos from Singapore Fintech Festival 2022](https://drive.google.com/drive/folders/1lF7PlRbpyrNa5VO4heQbBX0ZvDVNcgXU?usp=sharing)

There will be another live pilot involving real-time PBM payments at various select merchants in Singapore this coming August!

The upcoming pilot will involve SEA’s largest consumer wallet - Grab, StraitsX, Singapore tourism board, MAS and a few local banks.

---

**timlrx** (2023-07-24):

I definitely see the practical use case for the proposal though I feel that the proposed interface is too monolithic. There should be a clearer technical specification on what is required vs what is recommended, especially in terms of interfaces / events.

There are discrepancies between the proposed definitions, whitepaper and the sample implementation, so I will just focus on what was submitted on Github.

1. Does the sovToken necessary need to be a ERC 20 compatible token? I feel that is too restrictive. It’s quite possible for the native token or ERC1155 or ERC721 tokens to be store of value as well.
2. “PBM business logic” is a key part of the proposal and should be expounded. Is it restricted to access control logic or are there other parts to it? If it’s about access control, how about aligning it with ERC-5982: Role-based Access Control
3. I don’t think there’s a need to specify that PBM tokens should be ERC-1155. Why can’t they be ERC-20 and the decision of what form a PBM token should take is more of a business use case anyway.
4. “PBM MUST ensure the destination address for unwrapped sovToken is in a whitelist of Merchant/Redeemer addresses and not in a blacklist of banned addresses prior to unwrapping the underlying sovToken.” This is implementation specific e.g. do you need a blacklist, a whitelist or both. As long as the access control logic is well defined and auditable, this is again more of a use case specific implementation.
5. Implementation wise, I don’t think the PBM wrapper should be bound to the Token Manager. The ERC-20 contract can be wrapped to ERC-1155 (e.g. GitHub - 0xsequence/erc20-meta-token: General ERC20 to ERC1155 Token Wrapper Contract) first before wrapped to a PBM. This would reduce the requirement of being a PBM while making it more interoperable with existing standards out there.

---

**orchid-dev** (2023-08-17):

Timlrx,

Thank you for your comments. We have made some changes to the EIP-7291 to address some of your questions. We have also included our rationale for some choices below:

***1. Does the sovToken necessary need to be a ERC 20 compatible token? I feel that is too restrictive. It’s quite possible for the native token or ERC1155 or ERC721 tokens to be store of value as well.***

While we agree that a SOV token can literally be in the form of any token standards format published on https://eips.ethereum.org/ , we choose to focus on ERC20 as it’s:

As PBM is envisioned to **have functionality of money**, it has to be a **fungible token with stable value**. Currently, the major stablecoins in the market are mainly based on the ERC 20 interface. ERC 20 or ERC 20-compatible tokens are the most widely supported by existing wallets, defi apps, and used also by protocol design such as ERC4337 and more importantly they are the de facto standard for fungible tokens.

With regards to ERC721 and ERC 1155:

- ERC 721 is not suitable given that it is a standard for non-fungible tokens, which cannot fulfil the functions of money.
- While ERC 1155 tokens could be used for fungible tokens, we decided not to include it because there is a lack of ERC 1155 stablecoins in the market. Requiring the PBM interface to support both ERC 20 compatible and ERC 1155 compatible sovToken would complicate PBM interface without adding much practical utility. Furthermore, the base ERC 1155 does not support decimals, but this is not a dealbreaker as there can be workarounds. However, should there be changes in the stablecoin market in future, a revision can be considered.

***2. “PBM business logic” is a key part of the proposal and should be expounded. Is it restricted to access control logic or are there other parts to it? If it’s about access control, how about aligning it with ERC-5982: Role-based Access Control***

“PBM business logic” can contain access control logic, PBM unwrapping logic, api logic to integrate with non-blockchain IT systems,

In our proposed architecture, business logic can be divided into three types: core, plugin and hook logic. Core logic contains essential functionalities and validation checks and should be included in the PBM Wrapper contract. Plugin logic extends the core logic by adding functionality, e.g. custom data collection, additional administrative functions etc which a subset of PBMs may need. Hook logic implements additional validation checks which are only applicable for a subset of PBMs.

As PBM can be used for a wide variety of use cases, ranging from government disbursement tokens, shopping vouchers, prepaid tokens, rewards points tokens, purpose bound donation token, school allowance token etc, with each use cases having a separate business logic, it was intentionally left undefined so that implementation authors can have maximum flexibility.

***3. I don’t think there’s a need to specify that PBM tokens should be ERC-1155. Why can’t they be ERC-20 and the decision of what form a PBM token should take is more of a business use case anyway.***

The core aim of our proposal is to standardize the implementation of PBM proposed in Project Orchid. Hence, we have surveyed existing interface standards and decided to build upon ERC 1155 standard for the PBM tokens for the following reasons:

- ERC 1155 allows a single contract to support multiple tokens. This is very useful for the PBM use cases as a single contract can support issuance of tokens with different denominations, expiry dates, business logics.
- ERC 1155 also has batch transfer support, which is absent in ERC 20, which could lead to gas savings when tokens have to be airdropped to a large number of recipients.
- ERC 1155 is able to support semi-fungible tokens which could be very useful for PBM use cases as a PBM can be converted into a collectible after its expiry.
- ERC1155 allows for a visual representation of a PBM token on the UI of a wallet issuer.

***4. “PBM MUST ensure the destination address for unwrapped sovToken is in a whitelist of Merchant/Redeemer addresses and not in a blacklist of banned addresses prior to unwrapping the underlying sovToken.” This is implementation specific e.g. do you need a blacklist, a whitelist or both. As long as the access control logic is well defined and auditable, this is again more of a use case specific implementation.***

This actually forms the core of what we are trying to propose - a PBM can only be unwrapped when it is transferred to pre-approved endpoints. PBM can be transferred freely, but the target allowed to unwrap the PBM and take delivery of the underlying sovToken must be limited to differentiate it from plain vanilla stablecoins that are wrapped by smart contracts (in some implementations we can also define that a whitelisted address is something that is dynamically determined at run time as well, such as presence of an NFT in a wallet address, or relying on an oracle etc) .

*Why we need a whitelist?*

The whitelist is a compulsory requirement because a PBM is purpose-bound, i.e. it should be unwrapped only if all conditions are fulfilled and it is transferred to someone in the predefined whitelist.

*Why we need a blacklist?*

The blacklist is a compulsory requirement to ensure that accounts which were banned for various reasons (e.g. address owner has re-registered a new account, address owner suspended/withdrawn/expelled due to complaints or law enforcement reason etc).

*Why we can’t have either a whitelist or a blacklist?*

While the same effect can be obtained by only having a whitelist, repeatedly redeploying the whitelist to the blockchain to ban one person is not gas efficient. Using a blacklist to implement purpose-bound money is not practical as you would need to have a list of all addresses to be excluded and update it whenever a new account is created.

***5. Implementation wise, I don’t think the PBM wrapper should be bound to the Token Manager. The ERC-20 contract can be wrapped to ERC-1155 (e.g. GitHub - 0xsequence/erc20-meta-token: General ERC20 to ERC1155 Token Wrapper Contract) first before wrapped to a PBM. This would reduce the requirement of being a PBM while making it more interoperable with existing standards out there.***

In our proposal, the Token Manager is used to create, store and retrieve token details. The PBM wrapper is a separate contract that stores the PBM business logic and the address of the _pbmWrapperLogic contract is passed into the PBMRC1 base interface at the initialisation. The PBM Wrapper is not bound to the token manager. Rather the PBM Wrapper is bound to the PBMRC1 base interface.

The choice to wrap ERC20 directly inside a PBM based on ERC1155 is to improve compatibility with existing wallet providers and to keep complexity to the minimum. Could you explain why would double wrapping the ERC20 token - once inside the [0xsequence/erc20-meta-token](https://github.com/0xsequence/erc20-meta-token) (essentially a ERC1155 wrapper) and a second time in a PBM wrapper - make it more interoperable? It seems to add additional complexity and introduce overlapping ERC1155 functionalities.

If you find the existing functionality of the [0xsequence/erc20-meta-token](https://github.com/0xsequence/erc20-meta-token) useful, you could incorporate its functionality into the PBM wrapper directly instead of double wrapping it. The proposal specify a core set of minimum functionalities, it does not restrict developers from including additional functionality into the PBM.

In the latest draft, we have elaborated on the PBM wrapper architecture consisting of core, plugin and hook logics. This would convey our intention that developers can extend the functionality of the PBM implementation beyond what is specified in this proposal clearly by adding plugin and hook logics. The PBM address list, token manager and the PBMRC base interface would be part of the PBM core as it is linked to the core definition of a PBM.

