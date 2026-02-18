---
source: ethresearch
topic_id: 17142
title: "Eip-6956: Asset-bound Non-Fungible Tokens"
author: xiaolou86
date: "2023-10-20"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/eip-6956-asset-bound-non-fungible-tokens/17142
views: 600
likes: 0
posts_count: 2
---

# Eip-6956: Asset-bound Non-Fungible Tokens

thanks to author: Thomas Bergmueller (@tbergmueller), Lukas Meyer (@ibex-technology)

Asset-bound NFTs anchor a token 1-1 to an asset and operations are authorized through oracle-attestation of control over the asset.

## Replies

**xiaolou86** (2023-10-20):

This standard allows integrating physical and digital ASSETS without signing capabilities into dApps/web3 by extending ERC-721.

An ASSET, for example a physical object, is marked with a uniquely identifiable ANCHOR. The ANCHOR is bound in a secure and inseperable manner 1:1 to an NFT on-chain - over the complete life cylce of the ASSET.

Through an ATTESTATION, an ORACLE testifies that a particular ASSET associated with an ANCHOR has been CONTROLLED when defining the `to`-address for certain operations (mint, transfer, burn, approve, …). The ORACLE signs the ATTESTATION off-chain. The operations are authorized through verifying on-chain that ATTESTATION has been signed by a trusted ORACLE. Note that authorization is solely provided through the ATTESTATION, or in other words, through PROOF-OF-CONTROL over the ASSET. The controller of the ASSET is guaranteed to be the controller of the Asset-Bound NFT.

The proposed ATTESTATION-authorized operations such as `transferAnchor(attestation)` are permissionless, meaning neither the current owner (`from`-address) nor the receiver (`to`-address) need to sign.

