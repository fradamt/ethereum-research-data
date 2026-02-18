---
source: magicians
topic_id: 15761
title: EIP 7516 - BLOBBASEFEE Opcode
author: CarlBeek
date: "2023-09-12"
category: EIPs > EIPs core
tags: [opcodes]
url: https://ethereum-magicians.org/t/eip-7516-blobbasefee-opcode/15761
views: 2800
likes: 0
posts_count: 10
---

# EIP 7516 - BLOBBASEFEE Opcode

Same ideas as `BASEFEE`, but for EIP-4844 blobs.



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-7516)





###



Opcode that returns the current data-blob base-fee

## Replies

**chfast** (2023-09-13):

EIP-4844 does not define `G_base` nor “blob base-fee”.

---

**CarlBeek** (2023-09-13):

Thanks [@chfast](/u/chfast), you’re correct those terms were not explicitly defined. I clarified these points in [PR #7701](https://github.com/ethereum/EIPs/pull/7701).

`G_base` was a hold over from starting with EIP-3198 and is not relevant to this EIP.

“blob base-fee” is the colloquial name given to the result of the function `get_blob_gasprice(header)` as defined in EIP-4844.

---

**adietrichs** (2023-09-13):

This is a sensible addition. I can’t quite remember why 4844 does not include an opcode like this, I think it might have been that we were originally aiming for Shanghai inclusion and wanted to limit to the minimal viable feature set. For the same reason, I am uncertain whether this is high priority enough now to justify a last-minute inclusion into Dencun. Would be useful to hear how much of a priority this would be for L2s.

Separately, I think that there is a general desire to move away from these special-case opcodes, towards a more general form of exposing EVM context info. E.g. have a way to query fields from previous headers that abstracts away the specific format of the header. If we don’t include this EIP into Dencun, I would prefer for us to explore this direction further and see if we could add something general like that into the next fork instead. If we do want to move ahead with this EIP for Dencun, I would suggest as a compromise to at least make it forward compatible with future fee market dimension additions, by taking a “dimension index” from the stack (with 0 and 1 for the current normal basefee and data basefee respectively)

---

**CarlBeek** (2023-09-13):

While I appreciate the intent to future proof this, I’m not convinced that we can predict what would happen here and so it’s easy to end up over-optimising for future extensions that may never come to life. It is also not quite as simple as you make out as these values are not “just” fetched from the head, `BASEFEE`, can just return the value from the header, whereas `BLOBBASEFEE` is the result of running a calculation  over the header (`get_blob_gasprice(header)`), future additions (eg. for L2 prover costs etc) might have siginificantly more complicated functions which require complicated gas accounting etc.

---

**chfast** (2023-09-14):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/c/df788c/48.png) CarlBeek:

> “blob base-fee” is the colloquial name given to the result of the function get_blob_gasprice(header) as defined in EIP-4844.

Why to use the colloquial name in the instruction name when you literally used `get_blob_gasprice` code example?

---

**chfast** (2023-09-14):

What is the expected range of values it returns? This should be put in the EIP.

---

**CarlBeek** (2023-09-15):

> @chfast
> Why to use the colloquial name in the instruction name when you literally used get_blob_gasprice code example?

Because `BLOBBASEFEE` is the most accurate description of what it is, it is litralley the 1559 style base fee for blobs.

> @chfast
> What is the expected range of values it returns? This should be put in the EIP.

Is this actually helpful? Auditors should treat it as a standard EVM uint. I practice it is limited by burning through the ETH supply to get the 4844 blobs full in the previous blocks. It is not something we define for the `BASEFEE` EIP

---

**chfast** (2023-09-16):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/c/df788c/48.png) CarlBeek:

> Because BLOBBASEFEE is the most accurate description of what it is, it is litralley the 1559 style base fee for blobs.

Then 4844 should be changed accordingly.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/c/df788c/48.png) CarlBeek:

> Is this actually helpful? Auditors should treat it as a standard EVM uint. I practice it is limited by burning through the ETH supply to get the 4844 blobs full in the previous blocks. It is not something we define for the BASEFEE EIP

This is helpful for API design. I.e. how to deliver this information to EVM.

---

**poojaranjan** (2023-11-20):

Learn more about [EIP-7516 : BLOBBASEFEE opcode](https://www.youtube.com/watch?v=VUita9Yl9gY&list=PL4cwHXAawZxqu0PKKyMzG_3BJV_xZTi1F&index=2&t=384s&pp=gAQBiAQB) and the future of Ethereum scaling with [@adietrichs](/u/adietrichs)

