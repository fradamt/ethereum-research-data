---
source: magicians
topic_id: 16301
title: "Post EIP/ERC split : Create ERC-1, an ERC specific version of EIP-1"
author: Joachim-Lebrun
date: "2023-10-27"
category: Magicians > Primordial Soup
tags: [erc-1, eip-1]
url: https://ethereum-magicians.org/t/post-eip-erc-split-create-erc-1-an-erc-specific-version-of-eip-1/16301
views: 2195
likes: 22
posts_count: 19
---

# Post EIP/ERC split : Create ERC-1, an ERC specific version of EIP-1

With the recent decision to separate EIPs and ERCs into two distinct repositories, it’s become apparent that the preamble section, as defined in [EIP-1](https://eips.ethereum.org/EIPS/eip-1), requires some adjustments to better suit ERCs. Here are my thoughts on the necessary changes:

1. Change of Identifier: The eip field should be updated to erc to reflect the specific nature of the document. This change is straightforward but crucial for clarity and proper categorization.
2. Removal of Category: Given that all documents in the ERC repository will inherently fall under the ERC category, the category field becomes redundant. Removing it would streamline the preamble and avoid unnecessary repetition.
3. Reevaluation of Type: The type field, which currently seems to default to Standards Track for ERCs, might be redundant if all ERCs indeed fall under this type. However, I would advise caution here. If there’s even a small subset of ERCs that might require a different type classification in the future, retaining this field could be beneficial for flexibility and future-proofing. It’s worth a deeper analysis to confirm the uniformity of the type field across all ERCs.
4. Potential Additional Changes: While the above points address the most immediate concerns, we should also be open to other adjustments that might better tailor the preamble to the specific needs and nuances of ERCs. This could include additional fields or modifications to existing ones that reflect the unique aspects of ERCs.

I believe these changes will make the preamble more relevant and efficient for ERCs.

## Replies

**Joachim-Lebrun** (2023-10-27):

In addition to the adjustments in the preamble section, It could make sense to consider developing an `ERC-1` document. This would parallel `EIP-1` but with specific considerations for ERCs. For instance, ERC-1 could include:

1. Streamlined Process: Tailoring the proposal process specifically for ERCs, potentially simplifying or modifying steps that are more relevant to EIPs.
2. Dedicated Sections: Including sections that address common ERC-specific concerns, such as token standards, interoperability, and security considerations.
3. Updated Terminology: Ensuring that all terminology and references are directly relevant to ERCs, avoiding any EIP-specific language that might cause confusion.

This initiative would not only bring clarity but also establish a solid foundation for all future ERC proposals.

---

**matt** (2023-10-27):

These changes sound great! We have a bi-weekly meeting to discuss these types of things called EIPIP. I can add this to the agenda and if you can present it on wednesday next week we can try and make this happen. [EIPIP Meeting 93 · Issue #285 · ethereum-cat-herders/EIPIP · GitHub](https://github.com/ethereum-cat-herders/EIPIP/issues/285)

---

**joeysantoro** (2023-10-27):

I’d like to include [EIP-7539: ERC Extensions](https://ethereum-magicians.org/t/eip-7539-erc-extensions/16152) in these discussions for ERC-1, which has some new headers and dedicated sections and defines an “ERC Extension”

---

**0xMawuko** (2023-10-30):

Great initiative, and I 100% agree with the general direction of these modifications. I also believe we can fine tune some of the specifics to lay a clear and structured path for how a diverse set of app standards can be introduced via ERCs, in the future. Like so:

**Redefinition of Category for ERCs**

`Wallet` = For standardisation across wallets (hardware or software, full-node or light-node, program-managed or key-managed, etc.)

`Token` = For token design concepts and token contract development practises(NFTs, FTs, SFTs, SBTs, RWAs, etc.)

`Metadata` = For proposals around on-chain/off-chain metadata standards used in apps, tokens, etc. (Eg: Digital Art, collectibles, RWAs, Identity, Voting, etc.)

`DAO` = For proposals regarding DAO standards and practises.

**Reevaluation of Type**

It would be very beneficial to retain this indeed.

**Potential Additional Changes**

A great placeholder example to better ensure this flexibility and future adjustment is a `Subcategory` to allow for precision in the various categories, if ever need be.

**Add top-level Identifier** (Optional)

A top-level identifier with only two options to identify EIP from ERC might just be the cleaner path to take. Like so:

`Camp` = [EIP | ERC]  (`Class` might also be a good alternative  to `Camp`)

Example Header:

Camp: ERC

Number: 9027

Type: Standards

Category: Wallets

*Sub-category: Hardware wallet

*insert the other fields that usually follow here*

In conclusion, this suggestion can serve as the foundation for a detailed and robust taxonomy that all app-level developers and contributors, both technical and non-technical, can use when proposing app standards to the community.

---

**Joachim-Lebrun** (2023-10-30):

I just opened a PR with basic changes to the EIP-1 to create the ERC-1, please have a look at it and help improve it if you can ![:slightly_smiling_face:](https://ethereum-magicians.org/images/emoji/twitter/slightly_smiling_face.png?v=12) [Website: Ethereum Request for Comments Process by Joachim-Lebrun · Pull Request #61 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/61)

---

**Joachim-Lebrun** (2023-10-30):

As requested, i opened this [PR](https://github.com/ethereum/ERCs/pull/61) it is very incomplete atm of course, but given the short deadline (wednesday) i couldn’t do better for now, please take a look and tell me what you think about it

---

**Joachim-Lebrun** (2023-10-30):

please create a PR on my ERC-1 file with the modifications you would like to see. I already created some specific categories for ERCs but didn’t include all the ones you mention here. I like the idea of optional sub category, can you formalize it also to add in the current PR?

---

**0xMawuko** (2023-11-01):

Done ![:white_check_mark:](https://ethereum-magicians.org/images/emoji/twitter/white_check_mark.png?v=15)

https://github.com/Joachim-Lebrun/ERCs/pull/1

---

**Joachim-Lebrun** (2023-11-01):

Looks great, i just merged it. Still a lot of sub categories that should be added i believe, but it is a great start

---

**0xMawuko** (2023-11-01):

We discussed the proposal today at the EIPIP call and it had good support, check the discord server.

---

**sbacha** (2023-11-01):

Classification of ERCs is a premature decision that precludes new use cases that are atypical. Classification is a *forced choice*.

*Keywords*, or *Tags* seem more appropriate.

---

**0xMawuko** (2023-11-06):

1. Classification is an iterative process.
2. Tags are essentially what Subcategories provide.

Recommend joining the future EIPIP calls as this is where the Editors clarify quite a lot of this.

---

**joeysantoro** (2023-11-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sbacha/48/4661_2.png) sbacha:

> Keywords, or Tags seem more appropriate.

Strongly agree with a preference for Tags. ERCs are not a hierarchical taxonomy in nature and treating them as having cleanly divisible categories and subcategories is a mistake.

The category section is useful for creating broad strokes classes, and using tags to provide granularity is a more desirable option than subcategories. Tags accounts for the combination of concepts within and across categories which are common in ERCs.

---

**joeysantoro** (2023-11-06):

Added a PR to ERC-1 with a minimum viable framework for Extensions: [Add Extensions to ERC-1 by Joeysantoro · Pull Request #2 · Joachim-Lebrun/ERCs · GitHub](https://github.com/Joachim-Lebrun/ERCs/pull/2)

---

**Aboudjem** (2023-11-12):

Splitting ERCs and EIPs was a smart move !

Great initiative on ERC-1 draftt by the way. It’s a solid start and a much-needed step for the community. I’ve submitted a PR to build on this foundation to enhance clarity and utility. Here’s a quick overview:

1. ERC Dependency Classification: Introduced to distinguish between standalone and dependent ERCs, aiding in understanding their interrelations.
2. Code Quality and Documentation: Emphasized adherence to standard coding practices and comprehensive documentation for clarity and consistency.
3. Refined Content Guidelines: Updated to ensure content is direct, relevant, and accessible.
4. Separate ERC for Subcategory Management: Proposed for streamlined updates and uniform categorization.
5. Auxiliary File Optimization: Ensures efficient repo management.
6. Simplified ERC Ownership Transfer Process: Outlined straightforward guidelines for transferring ERC ownership.

Looking forward to your thoughts on these enhancements. Keep up the great work

---

**Aboudjem** (2023-11-13):

Since the **ERC** and **EIP** repositories have split, the numbering based on PRs is no longer practical, leading to confusion. A new process for number attribution is needed also addressing the **anti-sniping** concern with ERC number allocation can be quite straightforward. Here’s a streamlined proposal:

1. Sequential Automation: ERCs automatically get the next number in line after approval only approval, meaning that your number will be attributed only after the review. This ensures a tight sequence without gaps, starting from the last one, say, ERC-9001.
2. Random Blocks: Numbers within specific ranges are randomly assigned to new ERCs. This means that any plate number falling within a block, like ERC-9001 to ERC-9049, is assigned randomly to prevent predictability.
3. Interval Assignments: Allocate numbers at set intervals within reserved ranges for different categories. Each standard type, like wallets or tokens, would have its block (xx10, xx20, xx30).
4. Editor Queue: Editors assign numbers, but there’s a transparent queue for all to see which ERCs are up next. This balances fairness with editorial discretion and prioritizes readiness and quality over submission timing.

your input on these suggestions is needed ![:eyes:](https://ethereum-magicians.org/images/emoji/twitter/eyes.png?v=12). Any other ideas or feedback? Let’s maybe take this detailed discussion to a separate thread to keep our main ERC-1 talk straightforward.

---

**Joachim-Lebrun** (2023-11-20):

Thanks [@Aboudjem](/u/aboudjem) i merged your proposed changes to the PR.

It starts to look good imo, but it is obviously still very incomplete

---

**Aboudjem** (2023-11-27):

Just wondering [@Joachim-Lebrun](/u/joachim-lebrun) what are there specific areas you think are still incomplete or need more attention here?

