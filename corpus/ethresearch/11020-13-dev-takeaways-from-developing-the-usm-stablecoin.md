---
source: ethresearch
topic_id: 11020
title: 13 dev takeaways from developing the USM stablecoin
author: jacob-eliosoff
date: "2021-10-16"
category: Decentralized exchanges
tags: []
url: https://ethresear.ch/t/13-dev-takeaways-from-developing-the-usm-stablecoin/11020
views: 3778
likes: 7
posts_count: 7
---

# 13 dev takeaways from developing the USM stablecoin

We recently (finally…) [launched](https://twitter.com/usmfum/status/1447437647727763456) our stablecoin [USM](https://github.com/usmfum/USM) (which I’ve [written about here before](https://ethresear.ch/t/usm-minimalist-decentralized-stablecoin-could-use-final-feedback-before-v1-launch/8594)), and I thought I’d briefly list some of the juicier questions/novelties-to-me that came up during the ~15 months of developing it from an idea to a deployed smart contract.  Many of the lessons learned are relevant to other projects having nothing to do with USM.

(I’m *definitely* not a Solidity expert, this was all quite new to me, though I do have pre-blockchain coding experience.  Don’t take any of this as gospel, just my 2c up for discussion, and I apologize if some of these are obvious to the more seasoned smart contract devs among y’all.)

1. Immutable contracts?  I decided from early on to make the smart contracts immutable, on the principle that the crudest way to ensure decentralization/prevent abuse of power is to just “throw away the keys”.  This is a long topic (the downside of giving up the ability to fix bugs kinda speaks for itself…) but I think it’s a model worth exploring further, especially for relatively simple, minimalist projects like ours.  (It should be obvious that there are many projects where deploying immutably isn’t practical.)  Uniswap and Tornado.cash are two other projects I know of deployed this way, I’m sure there are many more.
2. Immutability → versioning.  If you can’t change your code, then your options are either a) instant total ossification or b) release new versions (while leaving the old one running) and hope people migrate to them.  (Again, we’re following in Uniswap’s footsteps here.)  We considered releasing our token with symbol “USM1” rather than “USM”, to emphasize that we expect to release future versions like “USM2”, not fungible with v1.  Similarly, we released “v1” (really “v1-rc1” - still a “release candidate” for now), not “v1.0”, because v1.0 could suggest that it might be upgraded to a compatible (“non-breaking”) v1.1.  But v1 can never be upgraded: only perhaps followed by a v2.
3. Simple sends (eg MetaMask) as UI.  The essence of USM is you either give some ETH and get back some USM, or vice versa.  Rather than build a real UI, for now we opted to just make the contract process sends of ETH or USM as operations: if you send it ETH, it will send back some USM in the same transaction, and vice versa (see USM.receive()/USM._transfer()).  This is a little risky (presumably some users will send to the wrong address…) but I gotta say, it’s addictive to be able to do complex ops via just a send in MetaMask!

(We even implemented a slightly wacky scheme for specifying limit prices via the least significant digits of the sent quantity, though that may be a tad overengineered…)
4. Preventing accidental sends of (eg) v2 tokens to the v1 address.  One pitfall of the op-via-send approach is, supposing in the future we release a v2 contract, a very natural user error will be to send USMv2 tokens to the USMv1 contract, or vice versa (or for v3, etc): naively this would irretrievably destroy the tokens.  We tried to mitigate this risk via OptOutable, a mechanism for letting contracts tell each other “Reject sends of your token to my address.”  There may be better ways to handle it, but anyway this user hazard is worth mitigating somehow.
5. Uniswap v3 oracles.  USM uses the Uniswap v3 TWAP oracle infra and I can strongly recommend it: our code using the v3 oracles is much simpler (~25 lines excluding comments) and better-UX than the code we were going to resort to for the v2 oracles.  (This is one small reason I’m glad we launched in October, rather than last January as originally planned…)  The v3 oracles still seem quite hot-off-the-presses (one annoyance is lack of support thus far for Solidity 0.8), so some users may want to wait till they’re more battle-tested, but I think their fundamental design is fantastic.  I believe Uniswap are also working on some further v3 oracle helper libs - if they do, definitely use those rather than code like ours.
6. MedianOracle.  Fundamentally, USM uses a “median of three” price oracle: median of (Chainlink ETH/USD, Uniswap v3 ETH/USDC TWAP, Uniswap v3 ETH/USDT TWAP).  There are various circumstances in which this could go down in flames but given some of the clunkier/riskier alternatives we considered, I’m pretty happy with it.  You’re welcome to use or adapt the oracle contract yourself (eg just call latestPrice()): like USM, the oracle is immutable and since the Uniswap pairs are too, in theory it should run forever.  (But please keep in mind that this is still relatively un-battle-tested code, caveat emptor!  Also keep an eye on @usmfum on Twitter for news of urgent bugs, re-releases etc.)
7. Gas-saving hack: inheritance instead of composition .  MedianOracle inherits from three oracle classes (including UniswapV3TWAPOracle and, uh, UniswapV3TWAPOracle2).  The much more natural design would be to give it three member variables holding the addresses of three separate oracle contracts and call latestPrice() on each of them: but that would mean three calls to external contracts, which eats a lot of gas.  So to save gas, we instead have a single contract that implements all three oracle classes + MedianOracle itself.  See the code for the gruesome details.

We drew the line at combining USM and MedianOracle into a single contract (just too gross, though would have saved a bit more gas).  We also kept USM and FUM (the other ERC-20 token in the USM system) discrete contracts: there may be some cunning way to make a single contract implement two distinct ERC-20 tokens, but again that exceeded our grossness/cleverness threshold.
8. ls = loadState(), pass around ls (the loaded state), _storeState(ls).  The main purpose of this pattern is to avoid loading state variables repeatedly in the code, since those loads are pricey in gas terms.  Instead we load once at the top-level start of each operation, and pass around the state as an in-memory struct, then call _storeState(ls) at the very end to write any modified elements.

Another benefit of this pattern is, since the stored format is only accessed in two places (loadState() and _storeState()), those two functions can get quite cute in how they pack the bits.  In our case we store two timestamps, two prices, and an adjustment factor (all to reasonable precision) in a single 256-bit word ( the StoredState struct).  By contrast, the unpacked LoadedState struct that’s actually used by all the other functions is much more legible (all 256-bit values) and intuitive.
9. Don’t store ETH balance in a separate variable.  It’s a simple thing, but we originally had an ethPool var that we updated to track the total amount of ETH held in the contract.  This was redundant: just use address(this).balance.  (Which we call once, in loadState().)
10. WAD math everywhere.  Fixed-point math sucks, but one way to make it suck even harder is to try to do math on a bunch of different vars all storing different numbers of decimal/binary digits - multiplying a 1018-scaled number, by a 296-scaled number, divided by a 1012-scaled number…  We just store everything as wads, ie, with 18 decimal digits (123.456 stored as 123,456,000,000,000,000,000).  When we encounter numbers scaled differently (eg from our price sources, Uniswap and Chainlink), we immediately rescale them to wads.  I think this avoided a lot of scary little oopsies.
11. Logarithms/exponents on-chain.  USM needs to calculate some exponents so we used some clever/hairy math (WadMath), partly adapted from various StackOverflow threads, partly from way-over-our-heads mathemagic from the brilliant ABDK guys.  This was all pretty scary and I dearly hope good standard libs emerge (maybe @PaulRBerg’s PRBMath?) to spare amateurs like us from wading into these waters.
12. Put convenience/UI/view-only functions in their own stateless contracts, separate from the key balance-changing contracts.  We kept the core, sensitive transactional logic in the USM and FUM contracts, and carved out peripheral dependent logic into separate contracts with no special permissions: USMView for those (eg, UIs) that just want to grab handy view stats like the current debt ratio, and USMWETHProxy for users who want to operate on WETH rather than ETH.  This is especially important for an immutably-deployed project like USM: if it turns out there’s a bug in USMView/USMWETHProxy, we can fix it and redeploy them without needing to redeploy the key ETH-holding USM/FUM contracts.
13. Fergawdsake mark your immutable vars as immutable.  This is the easiest way to save a considerable chunk of gas and we almost missed a couple…

May think of more…  Big thanks to [Alberto Cuesta Cañada](https://github.com/alcueca) and [@alexroan](/u/alexroan) for guiding me on my smart contract journey!  I learned a shitload, for the first time in years honestly.

## Replies

**MicahZoltu** (2021-10-16):

While I’m skeptical of the oracle, I’m a fan of almost all of the other decisions you have outlined here and I wish more people would build things following these principles.  I haven’t looked deeply into the mechanism design, but the gist is reasonable at least and I am a fan of that general design concept for pegged coins.

---

**PaulRBerg** (2021-10-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/jacob-eliosoff/48/4185_2.png) jacob-eliosoff:

> This was all pretty scary and I dearly hope good standard libs emerge (maybe @PaulRBerg’s PRBMath?)

Thanks for the shout-out! Yeah, [PRBMath](https://github.com/hifi-finance/prb-math) is exactly what you need if you don’t want to implement logarithms yourself. Just follow the examples in the [README](https://github.com/hifi-finance/prb-math/tree/4d357662802076b5b6072f582162d0c156d0bb02/packages/prb-math).

![](https://ethresear.ch/user_avatar/ethresear.ch/jacob-eliosoff/48/4185_2.png) jacob-eliosoff:

> WAD math everywhere

In fact this is implicitly solved if you’re using PRBMath. Currently there are two typed “flavors” of the library (`SD59x18Typed` and `UD60x18Typed`), which I wrote using structs. But I [plan](https://github.com/hifi-finance/prb-math/issues/51) on implementing the newly introduced [user defined value types](https://t.co/zKIGKZuFYZ?amp=1) to make the UX even better.

---

**jacob-eliosoff** (2021-10-16):

Glad to hear it, you’re definitely someone whose views I take seriously…  Just out of curiosity (plus we could still redeploy if needed!), any specific concerns/attack vectors about the oracle, or ways you’d do it differently?

---

**MicahZoltu** (2021-10-17):

I personally wouldn’t include ChainLink in the oracle, and instead find as many custodial coins in different legal jurisdictions as possible to use.  Perhaps weight them by some metric like volume or TVL?  Oracles will always be problematic, all you can do is mitigate risk as much as you can and I think the best you can do is just make it so companies in as many jurisdictions as possible have to act inappropriately at the same time for the system to fail.

Of course, some people consider a big multisig to be better than multiple custodians.  ![:man_shrugging:](https://ethresear.ch/images/emoji/facebook_messenger/man_shrugging.png?v=9)

---

**jacob-eliosoff** (2021-10-17):

The oracle question is indeed challenging: when we started this project I thought it would be simple, but it ended up consuming maybe half the total time we spent on USM!

A lot of people are critical of Chainlink, and its infra isn’t as on-chain/decentralized as I’d ideally like, but it gives accurate rapidly-updating prices compared to most other options we looked at.  And note that with the median design, Chainlink could go down permanently tomorrow and our oracle would just be taking the less accurate of two Uniswap prices.  So Chainlink isn’t quite a critical dependency for USM.

The bigger picture is that I strongly expect on-chain price sources to get more and more numerous and reliable with time.  I’m optimistic future USM versions will have three sources more robust than the three we use now, or even be able to take the median of five robust sources.  So thorny though it is, I think the outlook for the oracle problem (at least for a quote as common as ETH/USD) is bright.

---

**MicahZoltu** (2021-10-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/jacob-eliosoff/48/4185_2.png) jacob-eliosoff:

> it gives accurate rapidly-updating prices compared to most other options we looked at.

Past success is not indicative of future results.  It’s design is not censorship resistant, and if you have to pick your poison for oracle results, I think TWAPs of custodial coins offer a better trade off compared to the CL solution.

