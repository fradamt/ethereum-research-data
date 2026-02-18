---
source: magicians
topic_id: 14734
title: "EIP Draft: Struct Inheritance"
author: SinaTadayon
date: "2023-06-18"
category: EIPs
tags: [erc, extended-mapping, composition, type-casting, inheritance]
url: https://ethereum-magicians.org/t/eip-draft-struct-inheritance/14734
views: 532
likes: 2
posts_count: 3
---

# EIP Draft: Struct Inheritance

This EIP proposes a standardized approach to struct inheritance using composition over inheritance. It introduces the concept of extended-mapping, extended-array, and extended-functions, allowing for the extension of structs and type-casting between base and derived structs.

[Medium - Struct Inheritance In Solidity](https://medium.com/@sina.tadayyon/struct-inheritance-in-solidity-143c712f9092)

[EIP Draft - Struct Inheritance](https://github.com/SinaTadayon/EIPs/blob/master/EIPS/eip-struct-inheritance.md)

[Github - Struct Inheritance](https://github.com/SinaTadayon/structInheritance.git)

While working on a large project over the past year, I encountered certain limitations with structs in Solidity. To overcome these limitations, I developed an innovative solution by combining struct inheritance with mapping type. Recognizing the potential usefulness of this approach in projects with numerous similar structs, I decided to generalize my solution to dynamic arrays and overloaded functions.

I have written a draft EIP and implemented a solution to address challenges in struct inheritance. I invite the community to review, contribute, and provide insights to refine this proposal.

Let’s collaborate and start conversation!

## Replies

**wjmelements** (2023-06-27):

This is the wrong forum to discuss solidity. I recommend you open an issue against the ethereum/solidity github.

---

**SinaTadayon** (2023-06-27):

Your mention of the issue from certain aspects is correct because I have specifically investigated this issue in the Solidity language. However, we can also consider this issue from another perspective, which is the casting of smart contract entities in the memory and storage of the EVM.

thanks for your suggestion

