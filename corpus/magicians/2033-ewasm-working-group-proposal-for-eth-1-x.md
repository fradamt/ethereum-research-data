---
source: magicians
topic_id: 2033
title: Ewasm working group proposal for Eth 1.x
author: lrettig
date: "2018-11-27"
category: Working Groups > Ethereum 1.x Ring
tags: [ethereum-1x, ewasm]
url: https://ethereum-magicians.org/t/ewasm-working-group-proposal-for-eth-1-x/2033
views: 4246
likes: 14
posts_count: 5
---

# Ewasm working group proposal for Eth 1.x

We just published the proposal from the Ewasm working group, one of the three main [Eth 1.x](https://ethereum-magicians.org/t/ethereum-1-dot-x-a-half-baked-roadmap-for-mainnet-improvements/1995/2) working groups (the other two are state rent and data collection). This is a “pre-EIP” document and lays out the background, motivations, and high-level goals of the initiative. The document is public and commenting is turned on (or we can discuss here, of course).

Hugo kudos and thanks to [@AlexeyAkhunov](/u/alexeyakhunov) [@axic](/u/axic) [@cdetrio](/u/cdetrio) and many others who did the heavy lifting here.


      [docs.google.com](https://docs.google.com/document/d/1phHgp_h_EshH1HhSHEHf5jpI6zqIc6KRc95Xg1icJRM/edit)


    https://docs.google.com/document/d/1phHgp_h_EshH1HhSHEHf5jpI6zqIc6KRc95Xg1icJRM/edit

###

Ethereum 1.x - Ewasm Working Group Initial Report 26/11/2018  Executive Summary Enhancement of the Ethereum protocol is hindered by the inflexibility of the EVM architecture. The method of extending the execution layer has been the introduction of...

## Replies

**AlexeyAkhunov** (2018-11-27):

Thanks a lot for this publication! Looking forward to more details, specifically on deterministic interpreters/compilers, and interface between EVM and eWASM.

I just wanted to comment, that linear cross-contract storage proposed in the Storage Rent proposal would integrate nicely with eWASM, because it is linear. You could imagine memory-mapping part of linear storage (in R/O or R/W mode) before calling eWASM routing.

---

**gballet** (2018-11-27):

turbo-ewasm has an upcoming proposal for memory-mapping, we are going to study the cross-contract storage proposal and update it. Thanks for pointing this out.

---

**seven7hwave** (2018-11-28):

(Hello Magicians. Porting this over from twitter…thanks Lane)

Regarding security…does the existence of two parallel VM’s introduce systemic risk? The increased complexity of having separate VM’s, executing separate instruction sets, seems to increase the attack surface. In other words, the security benefits gained from eliminating dependance on precompiles might be countered by the resulting complexity stemming from the above proposal. Or can those risks be managed? And loosely speaking, how would you go about testing this setup? Could you throw fuzzers at it, similar to how Geth/Parity is tested?

On another note, it seems like this would make life a bit easier for end-user DApp developers. If so, that’s a nice win : )

---

**AlexeyAkhunov** (2018-11-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/seven7hwave/48/1190_2.png) seven7hwave:

> Regarding security…does the existence of two parallel VM’s introduce systemic risk

First of all, what is systemic risk in this context? ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) I only heard this term used in relation to bank collapsing causing collapse of the financial system and economy going into recession.

Sure, it is risky to have two VMs. It might not be super elegant, and in the hindsight, EVM could have been done better. But waiting for pure eWASM chain is basically waiting for Eth2.0.

Whether this risk is worth it? I think it is. Introducing it sooner rather than later would solve chicken and egg problem - to give motivation for creation specialised WASM interpreters and compilers for adversarial environments - with guarantees on compilation times and runtimes of opcode (currently this motivation is lacking). And if those new compilers and interpreters are creators, I am sure they will be ingested back into the Web world, where WebAssembly came from - to improve security of Web browsers.

Way to manage this risk? I think it is already in the proposal - first using eWASM for precompiles, before making it available for all contract developers.

On testing and fuzzing - I suspect eWASM team have some fuzzing experts onboard ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

