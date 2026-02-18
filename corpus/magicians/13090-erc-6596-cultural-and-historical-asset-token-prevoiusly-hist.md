---
source: magicians
topic_id: 13090
title: "ERC-6596: Cultural and Historical Asset Token (prevoiusly: Historical Asset Metadata JSON Schema)"
author: dhl
date: "2023-02-28"
category: ERCs
tags: [nft]
url: https://ethereum-magicians.org/t/erc-6596-cultural-and-historical-asset-token-prevoiusly-historical-asset-metadata-json-schema/13090
views: 2440
likes: 2
posts_count: 6
---

# ERC-6596: Cultural and Historical Asset Token (prevoiusly: Historical Asset Metadata JSON Schema)

[EIP-6596: Historical Asset Metadata JSON Schema](https://eips.ethereum.org/EIPS/eip-6596) establishes a metadata standard for *Historical Asset Tokens* (HATs).

HATs are tokens that represent a specific historical asset, such as a collectible or a rare item, and provide comprehensive context and provenance needed to establish historical significance and value, with the goal to enhance the discoverability, connectivity, and collectability of historically significant HATs.

Based on our experience tokenizing historical artifacts, and we have curated and defined dozens of metadata attributes, captured in the EIP. The proposed attributes had been shared with organizations working in NFTs and preserving historical artifacts such as *Aniomca Brands*, *British Museum* and *Christie’s*.

By extending the Metadata JSON Schema defined in ERC-721 and ERC-1155, we aim to create a ubiquitous language on top of widely accepted NFT standards, that would historical NFTs to flow between applications and conversations.

## Replies

**stoicdev0** (2023-03-03):

This seems highly specific which kind of defeats the purpose of an standard IMO, you’re even making most fields required.

Have checked [ERC-5773](https://eips.ethereum.org/EIPS/eip-5773)? It allows you to add multiple assets, each with it’s own metadata so you can use it to keep a historical record.

---

**avirm2000** (2023-03-29):

Thank you for your inquiry about our ERC-6596 standard. We appreciate the opportunity to clarify our approach.

We understand your concern that our standard may seem highly specific and defeat the purpose of a standard. However, our intention was to provide a metadata standard that addresses the needs of institutions such as museums, cultural institutions, and media companies that require comprehensive context and provenance for historical assets. Our standard aims to make it easier for these institutions to track and manage their extensive catalogs of historical assets, which often have 20-30 fields. We have positioned our standard to solve the problem of tracking and managing historically significant assets, making it easy to adopt and maintain.

Our mandatory fields are designed to connect collections together and provide enhanced discoverability for historical assets. However, beyond these mandatory fields, holders are free to add additional data points if desired. We believe that our standard adds significant value to historically significant assets by providing comprehensive context and provenance.

Moreover, we are aware of ERC-5773 and its ability to allow for multiple assets with their own metadata. While we recognize its potential applications in other use cases, our ERC-6596 standard is tailored specifically to provide comprehensive context and provenance for historical assets. We have designed our standard to address the challenges that institutions face during the onboarding process from web2 to web3, and by aligning key data points and fields, we are making the transition into web3 easier and more seamless.

To add on, we are proud to have developed a solution that allows institutions to migrate from off-chain databases to an on-chain system that provides a standardized approach. By using our ERC-6596 standard, historical assets can be more easily understood and interconnected, building a synergistic approach between all the institutes in the space.

We are open to supporting ERC-5773 in any way we can and welcome any ideas you may have. Our goal is to develop industry standards that support the tokenization of historically significant assets, and we appreciate your interest in our ERC-6596 standard. If you have any further questions or feedback, please do not hesitate to let us know.

---

**stoicdev0** (2023-03-30):

Sounds fair. Is there a existing standard outside of web3 already? It would make sense to stick to that.

Besides that, I’d just recommend to keep it flexible so it really can be used by any institution. A good approach for EIPs is to require the minimum possible to make it more usable, that may include making less fields required in your schema, but it could also be just a lack of domain knowledge from me.

---

**avirm2000** (2023-04-12):

Thank you for your recent comment and inquiry regarding our ERC-6596 standard. We greatly appreciate your interest in our work and welcome the opportunity to provide further clarification.

To address your first question, we have gone to great lengths to develop a standard that is specifically tailored for use within the web3 ecosystem. In doing so, we have consulted with numerous clients and experts in the field, including leading museums from around the world, to ensure that our standard is both robust and easy to adopt. Our goal is to facilitate the potential transition of traditional museums into web3 while also streamlining the integration of ERC-6596 for historical and cultural institutions.

Regarding your recommendation to keep the standard flexible, we fully agree that this is an important aspect to consider. We have designed our standard to be as usable as possible for different institutions, with the ability to add additional data points beyond the mandatory fields, allowing for customization to fit specific needs. However, we have also ensured that our mandatory fields provide comprehensive context and provenance for historical assets. While we are open to feedback on the required fields, we believe they are necessary to achieve our goal.

We value feedback from the community and will continue to consider adjustments to the schema based on domain knowledge and feedback. Once again, thank you for your interest in our ERC-6596 standard. Please do not hesitate to reach out if you have any further questions or feedback.

---

**dhl** (2023-11-30):

Hi folks. We have pushed a significant update to our previous draft and advanced the ERC-6596 proposal to be ready for peer review.

The update to the draft is motivated primarily to improve interoperability with existing NFT platforms, and to reflect our latest understanding of the domain space as we apply the standard to more cultural and historical assets, particularly real-world art pieces.

The updated proposal also includes an example of how the proposal is applied to the “[The Great Wave off Kanagawa](https://www.artic.edu/artworks/24645/under-the-wave-off-kanagawa-kanagawa-oki-nami-ura-also-known-as-the-great-wave-from-the-series-thirty-six-views-of-mount-fuji-fugaku-sanj%E7%AC%9Brokkei)” to make the application of the proposed metadata spec more relatable.

We invite and welcome your critiques, feedback, and discussions.

