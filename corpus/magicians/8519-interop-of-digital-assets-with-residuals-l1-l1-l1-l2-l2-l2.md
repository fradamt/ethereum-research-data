---
source: magicians
topic_id: 8519
title: Interop of Digital Assets with Residuals (L1 <-> L1, L1 <-> L2, L2 <-> L2)
author: highlander
date: "2022-03-04"
category: Magicians > Primordial Soup
tags: [token, layer-2, interop, residuals, digital-asset]
url: https://ethereum-magicians.org/t/interop-of-digital-assets-with-residuals-l1-l1-l1-l2-l2-l2/8519
views: 1180
likes: 0
posts_count: 1
---

# Interop of Digital Assets with Residuals (L1 <-> L1, L1 <-> L2, L2 <-> L2)

The [Layer 2 Working Group](https://github.com/eea-oasis/L2), an EEA - OASIS Community Project, would like to solicit feedback on one of its work items: Network interoperability of Digital Asset with Residuals.

Currently bridging digital assets such as ERC20 tokens or NFTs between networks (L1 ↔ L1, L1 ↔ L2, L2 ↔ L2, L1 ↔ sidechain), immobilizes the assets on the origin network and then instantiates them on the target network.

This approach works well if the digital asset has no associated business rules associated that infer rights or obligations to asset owners such as stable coins or simple NFTs. Examples of important digital assets that infer rights to the digital asset owner are residual payments/asset grants such as dividend-paying equities, bonds, annuities, asset-backed securities, digital assets with royalties, etc.

Unfortunately, such digital assets can currently not be transferred between networks because a transfer would break the connection between the asset, and the rights or obligations associated with it.

Given the importance of residual bearing digital assets in traditional finance and the emerging proliferation of DeFi assets that mimic traditional assets such as bonds or asset-backed securities while more and more value is locked in bridges and L2s, what would be possible solution approaches to this conundrum?

A first attempt has been made with the [GPACT protocol](https://github.com/ConsenSys/gpact) and it is currently being standardized within the [EEA Interop WG](https://entethalliance.github.io/crosschain-interoperability/).

Very much looking forward to the communities feedback!

Andreas Freund on behalf of the EEA-OASIS Layer 2 Community Project.

P.S: If you are interested in the work of the [Layer 2 WG](https://github.com/eea-oasis/L2), join our bi-weekly meetings, mailing list and slack channel.
