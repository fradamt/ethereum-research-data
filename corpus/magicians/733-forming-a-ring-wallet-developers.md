---
source: magicians
topic_id: 733
title: "Forming a Ring: Wallet Developers"
author: ligi
date: "2018-07-15"
category: Web > Wallets
tags: [wallet]
url: https://ethereum-magicians.org/t/forming-a-ring-wallet-developers/733
views: 6184
likes: 54
posts_count: 59
---

# Forming a Ring: Wallet Developers

As an action item after the Berlin Summer Council there is consensus we need more rings. I think we should form a ring for wallet developers. Wallet developers need to talk more to improve UX, interoperability, …

I for sure want to join such a ring - who else is in?

## Replies

**boris** (2018-07-16):

Is this [Login, Identity, and Wallets](https://ethereum-magicians.org/t/logins-wallets-and-identity/718/7) [@ligi](/u/ligi) topic (which I think has a bunch of UI/UX components too), or do you think more narrowly scoped to Wallet Apps & Dapps?

I think writing up a purpose / scope / charter is the first step in the TBD Ring process. I am reading up on IETF, and WGs are typically formed into Areas, so Wallet Devs could be in a larger Ring / Circle.

Love the momentum!

---

**ligi** (2018-07-16):

I like the wider scope of a wallet ring. Login and Identity are some topics inside the this ring.

---

**ligi** (2018-07-16):

Trying to scope it a bit and put some corner stones - contributions welcome:

- Wallet Interoperability

 URI EIPs

ERC-831 - base
- ERC-681 - transactions
- ERC-961 - token definitions

Addresses

- ERC-55 Address Checksums (category for this?)

Transactions

- EIP-155 Simple replay attack protection

Key management/exchange

- BIP-32  Hierarchical Deterministic Wallets
- BIP-39  Mnemonic code for generating deterministic keys
- BIP-44  Multi-Account Hierarchy for Deterministic Wallets

Contract interfacing EIPs

- ERC-165 - Interface detection
- ERC-20 - Tokens
- ERC-721 - NFTs

WIP - please comment and contribute!

---

**boris** (2018-07-16):

Great. Suggest that you help inform [Ring Formation](https://ethereum-magicians.org/t/process-for-ring-formation/747) – the wikis here are OK for simple things, but not sure if it works well enough, use HackMD if useful as I have suggested.

---

**ligi** (2018-07-16):

Thanks - will try to do it here first to prevent media disruption. Also suggest to inline all the google-docs things that where posted regarding the sessions for the same reason.

---

**boris** (2018-07-16):

Yep!

Having as much as possible in one tool / space helps a lot. The Ring Formation I need to turn into a formal EIP, so I figured HackMD was a good in between.

---

**ligi** (2018-07-16):

Just wondering if we need CIPs (Crypto Improvement Proposals for things that are not Ethereum specific. Seeing this problem now with the BIPs in this context.) - What do you think?

---

**jpritikin** (2018-07-16):

What happened to [EIP 777](https://eips.ethereum.org/EIPS/eip-777)? Isn’t there consensus for this New Advanced Token Standard?

---

**boris** (2018-07-16):

It was interesting to hear this brought up.

I worry that “we” don’t have the bandwidth.

Should “someone” work on a cross-crypto standards? Seems like a good idea. Are there existing bodies like the IETF where this might happen?

---

**ligi** (2018-07-16):

[@jpritikin](/u/jpritikin) I do not yet se much adoption of 777. That said I think we should improve token contracts and the interface. But perhaps we should not try to replace 20 with something new (AFAIK there have been multiple not that successufll attempts) - but add modules. I would love to see a module for deprecation of (token) contracts (see https://www.reddit.com/r/ethereum/comments/8xncoa/token_deprecation_metadata_and_ux/e254fot - not an EIP yet) - also I would love to see token contracts implementing the interface standard (eip-165)

[@boris](/u/boris) I wonder if CIPs could perhaps optimize things and increase bandwidth in the end ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=9)

---

**ligi** (2018-07-17):

We will have the digest of things here now: https://github.com/ethereum-magicians/scrolls/wiki/Wallet-Ring

---

**pedrouid** (2018-07-17):

I’m in for the Wallet Ring!

[@jpritikin](/u/jpritikin) I agree completely, I’m a big fan of the 777 but it would have to probably go through another ICO boom to overshadow all of the existing ERC20 tokens. Its an effort that requires both Dapp and Wallet developers

---

**pascuin** (2018-07-17):

We’re working on the wallet project [AirGap](https://airgap.it) and would also be interested in participating in this ring and help working on standards and patterns.

---

**ligi** (2018-07-17):

[@pedrouid](/u/pedrouid) [@pascuin](/u/pascuin) - great! added you both!

---

**pascuin** (2018-07-17):

Thanks! [@ligi](/u/ligi) what next steps do you have in mind, like a kick off call?

---

**ligi** (2018-07-17):

[@pascuin](/u/pascuin)  Actually yes. I would love it if we get something like the plasma implementers call together in this ring. Monthly - or bimonthly would be great from my side. What do you think?

---

**pascuin** (2018-07-17):

[@ligi](/u/ligi) The best thing to do is probably schedule a first call, define the action points and see what the response is from the participants on the frequency.

---

**ligi** (2018-07-18):

Makes sense - but I want to see some more people join and we have some more discussion points on the table before the first call. I think we need a bit more substance first and there is no hurry ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=9)

---

**kerman** (2018-07-18):

Working on EIP1192 and would love to get input from wallet ring devs about what you’d like to see/need in a recurring payments interface. https://github.com/ethereum/EIPs/issues/1217.

---

**ligi** (2018-07-18):

Great! - added it here: https://github.com/ethereum-magicians/scrolls/wiki/Wallet-Ring

and created a separate page for it here: https://github.com/ethereum-magicians/scrolls/wiki/1192

Feel free to add things!


*(38 more replies not shown)*
