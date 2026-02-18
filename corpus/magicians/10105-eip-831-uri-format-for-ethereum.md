---
source: magicians
topic_id: 10105
title: EIP-831 - URI Format for Ethereum
author: ligi
date: "2022-07-25"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/eip-831-uri-format-for-ethereum/10105
views: 3298
likes: 5
posts_count: 8
---

# EIP-831 - URI Format for Ethereum

This thread acts mainly as the `discussions-to` thread for EIP-831. Currently resurrecting it on the request of [@3esmit](/u/3esmit) and now this field is required by the EIP bot.

Also we should discuss the “eth” shortcut for the schema that is suggested.

Here the link to the EIP:



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-831)





###



A way of creating Ethereum URIs for various use-cases.










Here the PR for resurrecting the EIP from it’s current stagnant state:

https://github.com/ethereum/EIPs/pull/5335

## Replies

**qizhou** (2022-08-25):

I would suggest adding an alternative way to present a request as

```auto
request_alt                 = "eth" [ "ereum" ] [ "-" prefix ] ":" payload
```

The motivation is that mixing the payload with the prefix can be confusing, especially if “-” is accepted in the payload.  For example, in EIP-4804, using the old format for “app-uniswap-org.eth” dweb will be

```auto
ethereum://web3-app-uniswap-org.eth/
```

Using the alternative request format, then the request is

```auto
ethereum-web3://app-uniswap-org.eth/
```

which is much clearer.

BTW: I also found Microsoft is using similar way to format their request (see attached image from iana website)

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/a/a14de714d528ac82de687256ec1f510e73d2c67e_2_690x136.png)image2962×584 195 KB](https://ethereum-magicians.org/uploads/default/a14de714d528ac82de687256ec1f510e73d2c67e)

---

**ligi** (2022-08-28):

Thanks for chiming in. The disadvantage is that you then need to go through the IANA registration for every prefix. Also it makes the intent-filters on android suboptimal (all in manifest not in code). Lastly it is also breaking compatibility with already rolled out stuff. So not really thinking we should change it. But would also love to hear what others think.

Are you in Berlin on the 15th by any chance? We will discuss IANA registrations for URIs there very likely at the CASA gathering.

---

**qizhou** (2022-09-05):

Thanks for the response.  I understand there are a couple of concerns about the change such as IANA registration and backward compatibility. I am thinking if we could make some non-compatible changes such as adding an optional alternative prefix?

Thanks for the invitation. I am afraid that I am not able to be in Berlin on the 15th, but I am be definitively to join online if possible.

---

**TimDaub** (2022-09-05):

How will EIP-831 and [EIP-3770: Chain-specific addresses](https://eips.ethereum.org/EIPS/eip-3770) interact?

---

**ligi** (2023-02-10):

[@TimDaub](/u/timdaub)

I think we should not add EIP-3770 support to 831. Even though it is still in review IMHO we should not change it to not break assumptions. Also I think it is out of scope for this EIP.

That said: there can be another EIP - inheriting from 831 (like EIP-5094) does having support

[@qizhou](/u/qizhou)

would really love to not make breaking changes to this EIP - I think this would do more damage than good. Maybe another EIP with these ideas in mind could be the better solution and then try to move over - but breaking this EIP is bad IMHO

---

**MidnightLightning** (2024-01-15):

This EIP was revived in 2022, but it has gone stagnant again… In August 2022, it [was updated](https://github.com/ethereum/EIPs/pull/5432) to be in Review (as a dependency of ERC4804), but in March 2023, was [auto-updated](https://github.com/ethereum/EIPs/pull/5432) to Stagnant.

ERC4804 has been approved as part of the Standards Track, but no longer seems to cite EIP831 as a dependency (only EIP137). And, EIP6860 is in draft-form looking to update ERC4804.

The stagnant draft of EIP831 defines the desired IRI schemas as `eth:` and `ethereum:`, while the standards-track ERC4804 defines IRI schemas of `ethereum-web3:`, `eth-web3:`, `web3:`, and `w3:`. Those don’t overlap at all (and `ethereum-web3:`, `eth-web3:` would be dropped, if EIP6860 is accepted).

However, `ethereum:` [was registered](https://ethereum-magicians.org/t/consider-iana-registration-of-uri-scheme-for-ethereum/4285) with IANA as a schema for Ethereum. Since this EIP has gone stagnant again, should that IANA registration be withdrawn, and allow ERC4804/EIP6860 to be a replacement of EIP831? The `web3:` and `w3:` schemas [were registered](https://ethereum-magicians.org/t/eip-4804-web3-url-to-evm-call-message-translation/8300/22) for ERC4804, which can then continue the goals this EIP had?

---

**PatrickAlphaC** (2025-12-28):

I’d love this not to be stagnant… Having a URI like this would be great for something like a SEAL safe harbor agreement, as we could point to an on-chain address instead of relying on IPFS (which has a persistence issue), combined with something like Arweave.



      [github.com/security-alliance/safe-harbor](https://github.com/security-alliance/safe-harbor/pull/37)














####


      `main` ← `PatrickAlphaC:feat/eip-831`




          opened 08:22PM - 28 Dec 25 UTC



          [![](https://avatars.githubusercontent.com/u/54278053?v=4)
            PatrickAlphaC](https://github.com/PatrickAlphaC)



          [+1
            -1](https://github.com/security-alliance/safe-harbor/pull/37/files)







There isn't an issue tab for this repo, so I just made a PR instead (not final, […](https://github.com/security-alliance/safe-harbor/pull/37)please don't merge!).

It would be cool if we could have the agreementURI as an eip-831 ethereum URI (or, a chain agnostic URI like so: https://github.com/ChainAgnostic/CAIPs/issues/67)

