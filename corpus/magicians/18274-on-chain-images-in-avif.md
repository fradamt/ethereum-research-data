---
source: magicians
topic_id: 18274
title: On-chain images in AVIF?
author: MidnightLightning
date: "2024-01-22"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/on-chain-images-in-avif/18274
views: 557
likes: 2
posts_count: 1
---

# On-chain images in AVIF?

When contracts wish to save/generate image data on-chain, I’ve typically seen contracts generate SVG (vector) or PNG images (raster) as the output. For raster-style graphics, the [AVIF](https://en.wikipedia.org/wiki/AVIF) image format is making some headway as an updated and more flexible (can be lossy or loss-less, still or animated) means to save graphics. General guides I’ve read indicate it can be smaller in filesize than JPEG or PNG, but that it’s more CPU-intensive to achieve that.

The CPU-intensity seems to be from finding the most optimized way to compress arbitrary image data, so smart contracts may not be able to do the most optimum compression of a dynamic image (since “more CPU” would equate to “more gas cost”), but if the resulting file (if an off-chain process generated it) is a smaller filesize, saving that directly on-chain would be more cost-effective.

Has anyone else attempted generating AVIF files from a smart contract? With many NFT imagery consisting of different graphics for different traits being layered on top of each other, AVIF’s ability to create spatial layers may be an effective way to present dynamic content of that type?
