---
source: magicians
topic_id: 3206
title: EIP-1108 Reduce alt_bn128 precompile gas costs
author: cdili
date: "2019-04-26"
category: EIPs
tags: [precompile, alt_bn128]
url: https://ethereum-magicians.org/t/eip-1108-reduce-alt-bn128-precompile-gas-costs/3206
views: 5158
likes: 10
posts_count: 8
---

# EIP-1108 Reduce alt_bn128 precompile gas costs

A champion is needed for

https://eips.ethereum.org/EIPS/eip-1108

“It can be added to the Istanbul list if someone were to spend the time to champion it. It will also need to be updated with a section on new test vectors (likely just an update for the old ones) and a section on security considerations, since we are adjusting gas prices.”

https://gitter.im/ethereum/AllCoreDevs?at=5cbf16602e2caa1aa6a6b92d

## Replies

**zac-williamson** (2019-05-03):

Hi there!

AZTEC is quite interested in getting this EIP into Istanbul and we’re happy to try and push this forward. I’ve submitted a [pull request](https://github.com/ethereum/EIPs/pull/1987) to update the EIP and also to add it as a proposed EIP in eip-1679

Cheers,

Zac.

---

**Shadowfiend** (2019-05-09):

Original author of the EIP from Keep here, just to register support and thank Zac for picking up the baton here and filling in a bunch of details ![:bowing_man:](https://ethereum-magicians.org/images/emoji/twitter/bowing_man.png?v=9) Please let me know if there’s anything I can do to help ensure EIP-1108 slots on in!

---

**cdili** (2019-05-14):

Thank you [@zac-williamson](/u/zac-williamson) and [@Shadowfiend](/u/shadowfiend)  !!

It has been added to https://en.ethereum.wiki/roadmap/istanbul

---

**axic** (2019-07-04):

[@Shadowfiend](/u/shadowfiend) [@zac-williamson](/u/zac-williamson) it seems [@vbuterin](/u/vbuterin) [proposed a similar reduction here](https://github.com/ethereum/EIPs/issues/1187). Can you put that as a reference into the EIP so that we can close the issue?

---

**Shadowfiend** (2019-07-05):

[Done](https://github.com/ethereum/EIPs/pull/2177).

---

**Shadowfiend** (2019-07-31):

[@zac-williamson](/u/zac-williamson) I opened a PR for this on go-ethereum that I can move forward (https://github.com/ethereum/go-ethereum/pull/19904)—shall I take a crack at Parity as well or do you already have something cooking?

---

**fulldecent** (2019-12-02):

I have reviewed this EIP. Everything looks great, no reservations. Good work. I recommend for passage to Final.

