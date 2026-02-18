---
source: magicians
topic_id: 1563
title: ERC-681 (again)
author: ligi
date: "2018-10-11"
category: ERCs
tags: [wallet]
url: https://ethereum-magicians.org/t/erc-681-again/1563
views: 844
likes: 5
posts_count: 5
---

# ERC-681 (again)

I really beg all wallet developers to support ERC-681 - otherwise we end up with horrible UX like this:



      [github.com/Dappos/Dappos](https://github.com/Dappos/Dappos/issues/30#issuecomment-428851717)












####



        opened 03:54PM - 10 Oct 18 UTC



        [![](https://ethereum-magicians.org/uploads/default/original/2X/a/a4093a41d1065a78be0bc8665856d5d08e2f3542.png)
          ligi](https://github.com/ligi)










Just wanted to try the DAI integration after your announcement on reddit - but t[…]()he QR-Code is extremely wrong. Does not encode at all that DAI is requested. Also it is completely invalid 681:

![selection_244](https://user-images.githubusercontent.com/111600/46749040-3c713880-ccb5-11e8-89a3-43cbd31741cf.png)












please.

What is stopping you from supporting it? We really need to fix this ..

## Replies

**kaichen** (2018-10-16):

Hi [@ligi](/u/ligi)

ERC-681 came out at Aug. 2017, and imToken define this invalid format in late 2016. At that time we think about support eth only. I don’t know why other wallets follow this wrong URL support.

For backward compatibility, we have to keep this support. Our recent dapp browser module upgrade(not release yet) includes standard ERC-681 and related URL format standard.

---

**ligi** (2018-10-16):

thanks for the info [@kaichen](/u/kaichen) - looking forward to the update!

---

**gerrywon** (2018-10-25):

imToken already open source with token-core code, looking forward to discussing with you about wallet improvement and development

---

**frani** (2025-04-15):

Hi everyone ! I am proposing an improvement extension for ERC-681



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frani/48/14852_2.png)

      [EIP-7933: Ethereum Intent URI (EI-URI): A Universal Action URI format for Ethereum](https://ethereum-magicians.org/t/eip-7924-ethereum-intent-uri-ei-uri-a-universal-action-uri-format-for-ethereum/23554)




> Discussion thread for Add EIP: Ethereum Intent URI (EIURI) by frani · Pull Request #9644 · ethereum/EIPs · GitHub

## Abstract

This EIP introduces a standardized URI format for representing and triggering Ethereum JSON-RPC requests, allowing users to execute blockchain actions directly via URLs or QR codes. It extends the existing `ethereum:` URI scheme by supporting full RPC methods, optional chain identifiers, and additional semantic metadata such as `intent`, enhancing Web3 UX and interoperability across wallets.

## Motivation

ERC-681 introduced a way to encode Ethereum payment requests via URIs, laying the foundation for user-friendly interactions such as QR-code based payments. However, its scope is limited to eth_sendTransaction and lacks flexibility for more complex interactions, such as multi-call sequences, RPC methods beyond simple transfers, and chain-specific contexts.

As the ecosystem matures, users are increasingly performing a variety of Web3 actions—depositing into vaults, interacting with smart contracts, switching chains, or batch-signing transactions—all of which are not easily represented within the current URI standard.

This proposal aims to extend the URI pattern introduced in ERC-681 to support:

Arbitrary RPC calls (e.g., wallet_addEthereumChain, eth_call, eth_signTypedData)

Chained or multi-step requests via base64-encoded payloads

A clear and consistent way to encode the target chain (via chainId)

A more versatile way to encode intent (e.g., “deposit”, “swap”, “vote”, etc.)

Seamless QR-based user interactions without requiring wallet connection or dapp session

By standardizing this flexible URI format, wallets can parse and act on requests directly from a link or QR code, enabling smoother real-world interactions and improving onboarding, security, and UX across Ethereum applications.

