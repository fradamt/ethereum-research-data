---
source: magicians
topic_id: 9662
title: "EIP Draft: Article NFTs Standard"
author: xarraxyl
date: "2022-06-17"
category: EIPs
tags: [nft]
url: https://ethereum-magicians.org/t/eip-draft-article-nfts-standard/9662
views: 604
likes: 0
posts_count: 2
---

# EIP Draft: Article NFTs Standard

---

eip:

title: An Article NFTs Standard

description: A standard describing text-based NFTs for articles.

author: xarraxyl

discussions-to: [tbd]

status: Draft

type: Standards Track

category: ERC

created: 2022-06-15

---

## Abstract

This standard describes a simple protocol for creating and displaying NFT articles.

## Motivation

NFTs are associated with art, yet any kind of digital asset can be wrapped in an NFT. By providing a protocol for creating and displaying NFT articles, we unlock the interoperability needed for content writers to create and show their articles, which in turn can facilitate the article’s exchange using the already existing NFT infrastructure.

## Specification

An article NFT is an NFT whose URL points to a `txt` file that complies with the following rules:

1. MUST begin with a paragraph of arbitrary length that MUST begin with “title: ”.
2. MAY be followed by a paragraph of arbitrary length that MUST begin with “authors: “ which in turn MUST be followed by the authors’ names, separated by a comma.
3. MAY be followed by a paragraph of arbitrary length which MUST begin with “abstract: “
4. MAY be followed by a paragraph of arbitrary length, which MUST begin with “keywords: “ which in turn MUST be followed by the keywords, separated by a comma.
5. MAY be followed by “markdown: “ and then followed by a word describing the markdown schema. “none” is also acceptable if no markdown schema is used. The markdown schema keywords are not specified in this proposal but will be subject to organic community effort.
6. MUST contain at least one more paragraph.

Here is an example of the simplest possible txt file that would comply with the protocol:

===

title: Can trees talk to each other?

Scientists have discovered that trees may indeed be able to alert each other to danger by sending electrical messages through their roots.

===

Let’s take a look at an article that makes use of “authors”, “abstract”, “keywords”, and “markdown”.

===

title: Can trees talk to each other?

authors: xarraxyl

abstract: What can scientists say regarding tree-to-tree communication?

keywords: trees, communication, science

markdown: none

Scientists have discovered that trees may indeed be able to alert each other to danger by sending electrical messages through their roots.

===

Note that the order of the optional paragraphs is significant. This means:

- “abstract” must be after “authors”.
- “keywords” must be after “authors” and “abstract”.
- “markdown” must be after “authors”, “abstract”, and “keywords”.

### Glossary:

**Authors**. Creators of article NFTs.

**Platforms and marketplaces**. Web3 apps like LooksRare, OpenSea, Foundation, etc… which provide the ability for users to create and exchange digital assets.

**Paragraph**. Text of arbitrary length that ends with two carriage returns.

## Rationale

The design seeks the sweet spot between:

1. Ease of use for authors.
2. Ease of implementation by platforms and marketplaces.

The title and the body of the article are the only part of the protocol that are mandatory. This provides a minimal skeleton for articles.

The authors may provide additional metadata regarding the contents of the article by using “authors”, “abstract”, and “keywords”.

The “markdown” keyword is intended to instruct the UI on how best to display the body of the article.

## Backwards Compatibility

Not applicable. Text-based NFTs that do not comply with the standard are not considered article NFTs.

## Test Cases

A regex tool can be written to aid the implementation of NFT articles by testing if a file complies with the standard.

## Security Considerations

There are security risks for platforms and exchanges parsing the article NFTs’ text files to display their contents. A reasonable approach is to save the contents of these files in a database for a faster display to the end users.

A malicious article NFT may take advantage of an automated articles crawler and perform an SQL injection.

## Copyright

Copyright and related rights waived via CC0

## Replies

**MidnightLightning** (2022-06-20):

This draft to me seems like it’s very close to other standard “frontmatter” formats, but enough different that it would be its own new, competing standard? This draft accommodates authors who want to do non-markdown (with `markdown: none` as one of the examples indicates), but for the most part, if someone writes just plain text it’s also valid markdown. Is there a specific use-case you’re thinking of where it’s critical for someone seeking to be compliant with this standard to be able to create a text file that’s not valid markdown?

The preamble you’re describing here is close to what EIP-1 describes for [EIP preambles](https://eips.ethereum.org/EIPS/eip-1#eip-header-preamble), but not quite. The EIP-1 structure uses “[RFC 822](https://www.ietf.org/rfc/rfc822.txt) style header preamble”, a.k.a. “Jekyll-style [front matter](https://jekyllrb.com/docs/front-matter/)”, which has several apps that already know how to parse (e.g. GitHub parses it and shows it as a table at the start of the file if formatted like this). So, rather than inventing a new standard, using something like that which is already established seems like not a huge change, with the upside of already being compliant with several existing tools?

