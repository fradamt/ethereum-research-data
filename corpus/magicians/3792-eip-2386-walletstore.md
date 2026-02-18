---
source: magicians
topic_id: 3792
title: "EIP-2386: Walletstore"
author: mcdee
date: "2019-11-21"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-2386-walletstore/3792
views: 2558
likes: 1
posts_count: 2
---

# EIP-2386: Walletstore

Discussion thread for https://github.com/ethereum/EIPs/pull/2386

## Replies

**mratsim** (2020-10-06):

NCC had the following concerns while auditing the EIP-2386 implementation in Nimbus, see [Ethereum 2 walletstore by mcdee · Pull Request #2386 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/2386#issuecomment-693575270:)

> Hi,
>
>
> I was reviewing nim-blscurve and nim-beacon-chain and had some observations on EIP 2386 as a dependency. Note that a companion/copy to this comment is at status-im/nim-blscurve#85
>
>
> The EIP 2386 specification is silent on a number of aspects including:
>
>
>
>
> The maximum length of the name string and expectations regarding Unicode normalization.
>
>
>
>
> The type or maximum allowed nextaccount value.
>
>
>
>
> The type or maximum expected version value (though this is currently hardcoded and thus not yet necessary).
>
>
>
>
> Required or expected behavior when extraneous fields are present.
>
>
>
>
> For example, allowing a name string of length one gigabyte is not necessary and may surface downstream impacts stemming from unexpected/unnecessary memory allocations.
>
>
> While the name string is a simple identifier, different UTF-8 encodings may arise from malicious intent or simply the broad range of participating devices, operating systems, languages and applications. Characters with accents or other modifiers can have multiple correct Unicode encodings. For example, the Á (a-acute) glyph can be encoded as a single character U+00C1 (the “composed” form) or as two separate characters U+0041 then U+0301 (the “decomposed” form). In some cases, the order of a glyph’s combining elements is significant and in other cases different orders must be considered equivalent. Normalization is the process of standardizing string representation such that if two strings are canonically equivalent and are normalized to the same normal form, their byte representations will be the same. Only then can string comparison and ordering operations be relied upon. Performing this step is best practice to support user expectations related to rendering consistency.
>
>
> Regarding nextaccount, values beyond 253 are likely not necessary and may encounter problems related to the JavaScript number type having a 53-bit floating-point mantissa. Further, if this value is related to an index in EIP 2333, then a constraint of 232 is more reasonable.
>
>
> Specifying similar constraints for version can be done alongside other modifications for completeness, though this is not currently necessary.
>
>
> Specifying required or expected behavior when extraneous fields are present will improve implementation interoperability.
>
>
>
> ## Mitigation Recommendation
>
>
>
> To summarize, it is recommended to consider a maximum string length for name and to indicate that implementations should immediately normalize this value to the NKFC form per section 2.11.2.B.2 of Unicode Technical Report #36. Additionally, consider specifying the type and maximum values for both the nextaccount and version values, as well as what should happen if extraneous fields are present.

