---
source: ethresearch
topic_id: 12156
title: Interop of Digital Assets with Residuals (L1 <-> L1, L1 <-> L2, L2 <-> L2)
author: Therecanbeonlyone
date: "2022-03-04"
category: Layer 2
tags: [cross-shard, layer-2]
url: https://ethresear.ch/t/interop-of-digital-assets-with-residuals-l1-l1-l1-l2-l2-l2/12156
views: 2344
likes: 2
posts_count: 1
---

# Interop of Digital Assets with Residuals (L1 <-> L1, L1 <-> L2, L2 <-> L2)

The [Layer 2 Working Group](https://github.com/eea-oasis/L2), an EEA - OASIS Community Project, would like to solicit feedback on one of its work items: Network interoperability of Digital Asset with Residuals.

Currently bridging digital assets such as ERC20 tokens or NFTs between networks (L1 <-> L1, L1 <-> L2, L2 <-> L2, L1 <-> sidechain), immobilizes the assets on the origin network and then instantiates them on the target network.

This approach works well if the digital asset has no associated business rules associated that infer rights or obligations to asset owners such as stable coins or simple NFTs. Examples of important digital assets that infer rights to the digital asset owner are residual payments/asset grants such as dividend-paying equities, bonds, annuities, asset-backed securities, digital assets with royalties, etc.

Unfortunately, such digital assets can currently not be transferred between networks because a transfer would break the connection between the asset, and the rights or obligations associated with it.

Given the importance of residual bearing digital assets in traditional finance and the emerging proliferation of DeFi assets that mimic traditional assets such as bonds or asset-backed securities while more and more value is locked in bridges and L2s, what would be possible solution approaches to this conundrum?

**Identified Solution Challenges**

Using the simple example of Bond on Ethereum paying on a schedule in DAI, we outline some of the challenges

1. Since Alice (payor) of the scheduled bond payments is generally unaware that Bob (payee) moved a bond from Ethereum to Solana, Alice would send payment to the Bond smart contract with Bob’s address. Since Bob is no longer the owner of the bond, but rather the bridge contract is the payment would fail
2. If the bond contract were still aware that Bob was the payee, then the smart contract could still accept a bond payment but the payment would be owned by the bridge contract.
3. The previous bullet means that when the bond is locked in the bridge, the expected DAI bond payments must be instantiated on the Solana side in the Bond contract, now with Bob the owner of both the Bond token and the wrapped DAI
4. This means that when a payment is received into the Ethereum bond contract, the bridge network must be notified through an event of the payment and mint the payment amount as wrapped DAI on the DAI bridge contract on the Solana side, for Bob. That is problematic, because, there is no corresponding DAI in the bridge on the Ethereum side because it is associated with the Ethereum bond contract. This means that Bob’s WDAI on Solana would be worthless. Therefore, the payment amount in DAI can only be minted as an Ethereum IOU in the Solana Bond contract, since the DAI cannot be taken out of the Solana smart contract. That means the DAI payments the bondholder receives are useless on the Solana side. That is naturally not desirable.
5. If the bond is traded to Claire on Solana, Claire is now eligible to receive bond payments and no longer Bob. That means that after Claire purchased the Bond, the bridge network must create a placeholder for Claire’s payment to be received on the Ethereum side. That also means that Alice needs to know that she needs to send her bond payments indexed to Claire and not Bob. And once Claire receives a payment, the bridge network needs to create the same Ethereum DAI IOU on the Solana side. And so forth for every ownership change

And this is for a simple case of a bond, royalties for example, where the payments are mostly independent of token ownership and typically more than one party receives a portion of the payment are more complex because not all payments need to be bridged. However, the value of the digital asset is dependent on payment flows.

Generally speaking, it is unclear how to port complex digital assets between networks when the value of the asset depends on payments on the origin network but the asset is traded on the target network.

A first attempt has been made to address the challenge with the [GPACT protocol](https://github.com/ConsenSys/gpact) and it is currently being standardized within the [EEA Interop WG](https://entethalliance.github.io/crosschain-interoperability/).

Very much looking forward to the communities feedback!

Andreas Freund on behalf of the EEA-OASIS Layer 2 Community Project.

P.S: If you are interested in the work of the [Layer 2 WG](https://github.com/eea-oasis/L2), join our bi-weekly meetings, mailing list, and slack channel.
