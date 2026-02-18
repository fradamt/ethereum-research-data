---
source: magicians
topic_id: 380
title: Web3 Providers for the Future
author: andytudhope
date: "2018-05-17"
category: Web > User Experience
tags: []
url: https://ethereum-magicians.org/t/web3-providers-for-the-future/380
views: 2162
likes: 4
posts_count: 4
---

# Web3 Providers for the Future

I would like to start a thread about injecting web3 providers and what the plans are for that going forward, especially given this interesting piece from the one and only [@ricburton](/u/ricburton):

https://medium.com/@ricburton/metamask-walletconnect-js-b47857efb4f7

We just added a way for DApps to identify that it is a Status client which is the provider here: [[#4227] Allow DApps to identify status host by jeluard · Pull Request #4233 · status-im/status-mobile · GitHub](https://github.com/status-im/status-react/pull/4233)

And think this is an interesting and good topic to pick up across the ecosystem which might also dovetail well into better and more secure signing schemes in general.

Would love to get [@danfinlay](/u/danfinlay)’s input too.

## Replies

**danfinlay** (2018-05-20):

My current best ideas on this topic have been captured in this proposal:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/bitpshr/48/190_2.png)
    [EIP-1102: Opt-in provider access](https://ethereum-magicians.org/t/opt-in-web3-access/414) [EIPs](/c/eips/5)



> Hi everyone. My name is Paul Bouchon and I recently joined the MetaMask team.
> MetaMask and most other tools that provide access to Ethereum-enabled environments do so automatically and without user consent. This exposes users of such environments to fingerprinting attacks since untrusted websites can check for a provider object and reliably identify Ethereum-enabled clients.
> This proposal outlines a new dapp initialization strategy in which websites request access to an Ethereum provider API i…

Sorry for not seeing this first, it would have been a good place for outlining the constraints in public before sharing a proposal, please add any constraints there that (any reader here) feels we’ve missed.

---

**ricburton** (2018-05-21):

This is fantastic. I definitely want to make sure all of this infrastructure is shared and available on all wallets.

We should compete on approaches and focus. In my mind: Balance wants to become a bank. Status wants to take aim at Facebook. Metamask is the most pragmatic tool to kick off desktop dapp development.

---

**p0s** (2018-11-29):

I know this thread is older, but we finally opened a Provider Ring for more structured (dis)agreement on topics like EIP1102: https://ethereum-magicians.org/c/working-groups/provider-ring

