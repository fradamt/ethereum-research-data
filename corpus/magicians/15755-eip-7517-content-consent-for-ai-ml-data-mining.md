---
source: magicians
topic_id: 15755
title: "EIP-7517: Content Consent for AI/ML Data Mining"
author: bofuchen
date: "2023-09-12"
category: EIPs
tags: [erc]
url: https://ethereum-magicians.org/t/eip-7517-content-consent-for-ai-ml-data-mining/15755
views: 2802
likes: 3
posts_count: 9
---

# EIP-7517: Content Consent for AI/ML Data Mining

A proposal adding “dataMiningPreference” in the metadata to preserve the digital content’s original intent and respect creator’s rights.

---

This EIP proposes a standardized approach to declaring mining preferences for digital media content on the EVM-compatible blockchains. This extends digital media metadata standards like ERC-7053 and NFT metadata standards like ERC-721 and ERC-1155, allowing asset creators to specify how their assets are used in data mining, AI training, and machine learning workflows.

**Motivation**

As digital assets become increasingly utilized in AI and machine learning workflows, it is critical that the rights and preferences of asset creators and license owners are respected, and the AI/ML creators can check and collect data easily and safely. Similar to robot.txt to websites, content owners and creators are looking for more direct control over how their creativities are used.

This proposal aims to propose a standardized method of declaring these preferences. Adding `dataMiningPreference` in the content metadata allows creators to include the information about how they want their work whether the asset may be used as part of a data mining or AI/ML training workflow. This ensures the original intent of the content is maintained.

For AI-focused applications, this information serves as a guideline, facilitating the ethical and efficient use of content while respecting the creator’s rights and building a sustainable data mining and AI/ML environment.

The introduction of the `dataMiningPreference` property in digital asset metadata covers the considerations including

- Accessibility: A clear and easily accessible method with human-readibility and machine-readibility for digital asset creators and license owners to express their preferences for how their assets are used in data mining and AI/ML training workflows. The AI/ML creators can check and collect data systematically.
- Adoption: As Coalition for Content Provenance and Authenticity (C2PA) already outlines guidelines for indicating whether an asset may be used in data mining or AI/ML training, it’s crucial that onchain metadata aligns with these standards. This ensures compatibility between in-media metadata and onchain records.

---

Please see the latest proposal [here](https://github.com/ethereum/EIPs/pull/7682/files) and provide your comments below. Thanks!

## Replies

**ProphetZX** (2023-09-19):

Very nice work! I‘d recommend to add and also first check what the rights of the corresponding owner in the jurisdiction and legal system are at the time the asset is created. To my knowledge, legal issues may arise if, e.g., a token is created within a blockchain with an existing body of law at the time of the token creation. Therefore, even if a license is missing (or, e.g., the owner missed or did not create one himself) for the blockchain, all rights belong to the blockchain owner by default, to the best of my knowledge. So, mining preferences might be rejected, in this case, or may create a legal grey area.

---

**Pandapip1** (2023-09-19):

This suffers from the [evil bit](https://www.rfc-editor.org/rfc/rfc3514) problem. This doesn’t necessarily need fixing, since many other standards that suffer from the same problem do exist (e.g. robots.txt), but due to the nature of how AI models are currently trained and the decentralized nature of Ethereum, it may be harder to enforce than other evil bit standards. Might be worth including in the Security Considerations?

---

**ProphetZX** (2023-10-02):

Please remember that in almost every jurisdiction nowadays, a person has the right to their personal data. They may decide to revoke consent to process it, may request their personal data/data porting, may ask for correcting false data or to erase any personal data (e.g. under GDPR/EU law or most cyber law). I myself would never allow for my personal data, out of blockchain data collections for example, to be processed by AI/ML data mining, so not sure this is really fashionable. Just saying…

---

**Pandapip1** (2023-10-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/prophetzx/48/10281_2.png) ProphetZX:

> I‘d recommend to add and also first check what the rights of the corresponding owner in the jurisdiction and legal system are at the time the asset is created.

Unfortunately, this depends on users’ jurisdictions and is likely impossible to codify.

---

**bquinn** (2024-02-05):

FYI we at the IPTC, in association with the PLUS Consortium, have already created a standard that covers this in the embedded photo metadata. I understand that this is a different use case but perhaps you might like to re-use our controlled vocabulary?

News post about the changes:


      ![](https://ethereum-magicians.org/uploads/default/original/2X/8/89276e65d331c845e20b15f2717ca12f759b3564.png)

      [IPTC – 12 Oct 23](https://iptc.org/news/exclude-images-from-generative-ai-iptc-photo-metadata-standard-2023-1/)



    ![](https://iptc.org/wp-content/uploads/2023/10/IPTC-PMD-example-datamining01-300x300.jpg)

###



IPTC is the global standards body of the news media. We provide the technical foundation for the news ecosystem.



    Estimated reading time: 3 minutes











The relevant part of the IPTC Photo Metadata Standard Specification, which links through to the PLUS specification including the controlled vocabulary (I would link to it directly here but I’m only allowed to include two links in my post):



      [iptc.org](http://iptc.org/std/photometadata/specification/IPTC-PhotoMetadata-2023.1.html#data-mining)





###

---

**tammyyang** (2024-02-13):

Sure, as the purpose of EIP-7517 is not to develop a new standard, but adding immutable blockchain record for the content consent, it is important to refer to the existing standards. The current 7517 leverages the [C2PA assertion standard for the content consent](https://c2pa.org/specifications/specifications/1.3/specs/C2PA_Specification.html#_training_and_data_mining).

Based on my knowledge of the two standards, C2PA has a richer definition in the “mining type” (data_mining, ai_inference, ai_generative_training, ai_training) while [IPTC](https://iptc.org/news/exclude-images-from-generative-ai-iptc-photo-metadata-standard-2023-1/) has a richer definition in the “permission type” (unspecified, allowed, prohibit, prohibited-exceptsearchengineindexing, etc). The current proposed EIP-7517 only specified three types of permissions (allowed, notAllowed and constrained). If we extend the permissions to the richer definitions as defined in IPTC, will that make 7517 compliant with IPTC?

If not yet, love to learn more about what’s the major missing part that you think should be added.

---

**tammyyang** (2024-02-13):

Totally agree that this is complex and hard to codify. That’s why I think this ERC should leverage the mainstream standards that are already out there and widely accepted, like IPTC and C2PA (more discussions can be found [here](https://ethereum-magicians.org/t/eip-7517-content-consent-for-ai-ml-data-mining/15755/7)). The main goal with this ERC is to use blockchain to keep a permanent record of who’s okayed what with their content, rather than trying to come up with a whole new system from scratch.

From what I’ve been seeing in the latest discussions, there’s still a lot of back-and-forth about the rules for text and data mining (TDM) and its exceptions. This means that we should expect to see more updates on the regulation side in the coming years. But one thing seems clear to me: being open and clear is key in developing big AI models like LLMs. Therefore, even if content owners can’t charge money for TDM uses, it is still important that the right owners can still use the blockchain to represent how they prefer their content to be used.

---

**bofuchen** (2024-04-26):

C2PA splits AI/ML training and data mining assertions from the tech spec v2.0 and creates a new Creator Assertions Working Group (CAWG) for discussing this topic since 2024-03-18.

CAWG: [Training and Data Mining Assertion :: Creator Assertions Working Group](https://creator-assertions.github.io/training-and-data-mining/1.0/)

