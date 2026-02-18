---
source: magicians
topic_id: 8093
title: Forking Metamask for multichains
author: kladkogex
date: "2022-01-24"
category: Web > Wallets
tags: [wallet]
url: https://ethereum-magicians.org/t/forking-metamask-for-multichains/8093
views: 3031
likes: 6
posts_count: 9
---

# Forking Metamask for multichains

Metamask is a great wallet but it is near impossible to use in the multichain world.

I am thinking about forking Metamask and doing the minimum amount of changes in order to support the following:

1. For a particular key, the wallet will show the total tokens held on ALL chains. Then, in the detailed view mode the split will appear showing the subamount for every chain.
2. Moving token from one chain to another will be abstracted out.
In particular, if you click  to use an app running on a particular chain, the required amount of tokens will automatically move to this chain.
3. Ideally there would be an open discovery process to discover new chains and interchain token transfers.
4. There will be no chain switching UI, for a particular key all chains will be immediately available.

Comments are welcome )

## Replies

**looneytune** (2022-01-24):

With the exponential growth in popularity of other chains I think it would be a great user experience improvement. Isn’t Metamask team working on better similar solutions for multichain interactions?

---

**kladkogex** (2022-01-24):

We at SKL would be happy to use it if they did …

Does not seem like this at the moment  …

---

**edmundedgar** (2022-01-26):

Unfortunately metamask is non-free software. You’re allowed to fork it, but your fork isn’t allowed to be successful.



      [github.com](https://github.com/MetaMask/metamask-extension/blob/develop/LICENSE)





####



```
Copyright ConsenSys Software Inc. 2020. All rights reserved.

You acknowledge and agree that ConsenSys Software Inc. (“ConsenSys”) (or ConsenSys’s licensors) own all legal right, title and interest in and to the work, software, application, source code, documentation and any other documents in this repository (collectively, the “Program”), including any intellectual property rights which subsist in the Program (whether those rights happen to be registered or not, and wherever in the world those rights may exist), whether in source code or any other form.

Subject to the limited license below, you may not (and you may not permit anyone else to) distribute, publish, copy, modify, merge, combine with another program, create derivative works of, reverse engineer, decompile or otherwise attempt to extract the source code of, the Program or any part thereof, except that you may contribute to this repository.

You are granted a non-exclusive, non-transferable, non-sublicensable license to distribute, publish, copy, modify, merge, combine with another program or create derivative works of the Program (such resulting program, collectively, the “Resulting Program”) solely for Non-Commercial Use as long as you:
 1. give prominent notice (“Notice”) with each copy of the Resulting Program that the Program is used in the Resulting Program and that the Program is the copyright of ConsenSys; and
 2. subject the Resulting Program and any distribution, publication, copy, modification, merger therewith, combination with another program or derivative works thereof to the same Notice requirement and Non-Commercial Use restriction set forth herein.

“Non-Commercial Use” means each use as described in clauses (1)-(3) below, as reasonably determined by ConsenSys in its sole discretion:
 1. personal use for research, personal study, private entertainment, hobby projects or amateur pursuits, in each case without any anticipated commercial application;
 2. use by any charitable organization, educational institution, public research organization, public safety or health organization, environmental protection organization or government institution; or
 3. the number of monthly active users of the Resulting Program across all versions thereof and platforms globally do not exceed 10,000 at any time.

You will not use any trade mark, service mark, trade name, logo of ConsenSys or any other company or organization in a way that is likely or intended to cause confusion about the owner or authorized user of such marks, names or logos.

If you have any questions, comments or interest in pursuing any other use cases, please reach out to us at metamask.license@consensys.net.
```










You could fork the version before they switched to a non-free license but it’ll be pretty old at this point - before EIP1559, for example.

IMHO it’s really unfortunate that we’ve got so much of the ecosystem depending on proprietary software, but it would be good if your efforts could go into a free alternative.

---

**danfinlay** (2022-01-29):

Hi Klad,

We definitely are building towards a full multi-chain experience. In fact, to ensure that it works wonderfully, we’ve done a ton of design work, user testing, and refactoring, to make sure that this is not just added, but allows existing applications to continue working while also providing a smooth path to multi-chain dapps.

In the meanwhile, I hope you did notice our EIP-3085 methods for adding & switching chains for the user. They’re made to help hold people over in the meanwhile. [RPC API | MetaMask Docs](https://docs.metamask.io/guide/rpc-api.html#unrestricted-methods)

---

**baselka** (2022-02-04):

Hi Klad,

We were able to fork MetaMask in July 2020,  before they switched to a non-free license.

We were able to customize it and make it a multi chains wallet, Ethereum, Tron, and currently adding BTC.

The main landing page displays all chains and tokens with balances then total balance of all chains and tokens.

User cannot change the network from the main page but instead in the detailed view.

So yeah it’s doable but I’m not sure about what you meant in your second point .

---

**kladkogex** (2022-02-04):

Hey, thank you! Can you point me out to your repo?

---

**baselka** (2022-02-04):

Hi Klad, please reach me in skype or email ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=10)

it’s a private repo, but I can demo to you what we’ve done to accomplish this.  ![:ok_hand:t6:](https://ethereum-magicians.org/images/emoji/twitter/ok_hand/6.png?v=10)

[easysatti@gmail.com](mailto:easysatti@gmail.com)

live:easysatti

---

**sbacha** (2022-02-06):

state management client side on frontends is especially poor to handle multichain states - that may be a real blocker in the short run

