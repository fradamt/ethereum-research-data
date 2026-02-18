---
source: magicians
topic_id: 1852
title: "Forming a Ring: Provider Ring"
author: p0s
date: "2018-11-09"
category: Working Groups > Provider Ring
tags: []
url: https://ethereum-magicians.org/t/forming-a-ring-provider-ring/1852
views: 1897
likes: 12
posts_count: 11
---

# Forming a Ring: Provider Ring

Hey all, we are announcing the Ethereum Provider Ring (Short: Provider Ring).

During Devcon [@wolovim](/u/wolovim) got some people around the topic of Ethereum providers together.

We kicked off a ring formation, and planned to establish more regular communication about fun stuff like EIP1102 + [EIP1193](https://ethereum-magicians.org/t/eip-1193-ethereum-provider-javascript-api/640).

We agreed that we will benefit from more structured conversations. Therefore this new **Provider Ring**.

Teams involved so far:

- Mist Browser: @wolovim, Ryan
- Metamask: @bitpshr, Bobby
- Status: @jeluard, @rachelhamlin, @andrey
- imToken: @p0s , @kaichen
- web3.js: Samuel
- ethers.js: Richard

*Who else is in?*

Topics (potential forum threads) so far:

- coordinate a tentative EIP 1193 release date; potential rescheduling EIP1102 + 1193 rollout
- discuss nonstandard convenience methods (e.g. isLocked)
- how to switch active account? (e.g. force + additional params)
- introducing specific new RPC methods (e.g. eth_changeNetwork )
- generic path for introducing new RPC methods (e.g. one EIP per method; first EIP establishes a template)
- … and communication: establishing regular communication (hangouts, discord), inviting remaining providers.

Next steps: I will follow the [how to](https://github.com/ethereum-magicians/scrolls/wiki/HOWTO-Form-A-Ring) and everybody is welcome to chime in and give feedback!

Who else is in?

## Replies

**p0s** (2018-11-09):

I added the ring charter on github [here](https://github.com/ethereum-magicians/scrolls/wiki/Provider-Ring).

---

**rmeissner** (2018-11-09):

Hey,

we would like to join too ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

I am Richard working on the Gnosis Safe

Cheers

---

**jeluard** (2018-11-09):

Thanks [@p0s](/u/p0s) for starting this! I am actually [@jeluard](/u/jeluard) here.

And please also add [@rachelhamlin](/u/rachelhamlin) and [@andrey](/u/andrey) to the Status team.

---

**p0s** (2018-11-10):

hey Richard! I didn’t know Gnosis Safe is a provider?! Is that a future plan?

Anyway, feel free to add yourself to the participants [here](https://github.com/ethereum-magicians/scrolls/wiki/Provider-Ring). Later, you will be able to add topics to the ‘Provider Ring’ category in this forum.

---

**p0s** (2018-11-10):

Added above ![:blush:](https://ethereum-magicians.org/images/emoji/twitter/blush.png?v=9) . Feel free to edit names and topics in [the wiki](https://github.com/ethereum-magicians/scrolls/wiki/Provider-Ring).

---

**rmeissner** (2018-11-10):

Currently we provide an chrome extension which allows easy interaction with the Safe app. This chrome extension is injecting a provider (similar to MetaMask).

I think a lot of the wallet folks (Wallet Ring) are working to some extend on providers (e.g. [@pedrouid](/u/pedrouid) for walletconnect) and some of the discussions that are assigned to the wallet ring might be interesting for the provider ring as well (e.g. [EIP 747: wallet_watchAsset](https://ethereum-magicians.org/t/eip-747-wallet-watchasset/1048) and [Add `wallet_` methods to improve dapp to wallet interaction](https://ethereum-magicians.org/t/add-wallet-methods-to-improve-dapp-to-wallet-interaction/1848))

Also there is still not clear definition how we could have something like a “provider” for mobile (at least a wallet provider maybe).

---

**p0s** (2018-11-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rmeissner/48/643_2.png) rmeissner:

> Currently we provide an chrome extension which allows easy interaction with the Safe app. This chrome extension is injecting a provider (similar to MetaMask).

Now I get it, great!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rmeissner/48/643_2.png) rmeissner:

> I think a lot of the wallet folks (Wallet Ring) are working to some extend on providers (e.g. @pedrouid for walletconnect) and some of the discussions that are assigned to the wallet ring might be interesting for the provider ring as well (e.g. EIP 747: wallet_watchAsset and Add wallet_ methods to improve dapp to wallet interaction)

I put some of them [on the list](https://github.com/ethereum-magicians/scrolls/wiki/Provider-Ring) to contact when a new ‘Provider Ring’ category is added.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rmeissner/48/643_2.png) rmeissner:

> Also there is still not clear definition how we could have something like a “provider” for mobile (at least a wallet provider maybe).

I guess there a two ways right now, in the mobile wallet or in the browser such as Opera.

---

**rmeissner** (2018-11-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/p0s/48/535_2.png) p0s:

> I guess there a two ways right now, in the mobile wallet or in the browser such as Opera.

Yeah, that are the current implementations. Either we have wallets that only really allow you do manage your assets (maybe some have some deep linking support, e.g. Trust) or we have a browser with an integrated wallet (imToken, Status, Opera, MetaMask)

It would be nice if there was something that works better with native apps, e.g a service on Android. But again this is something what I think would be nice to figure out and come up with a standard ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**ryanio** (2018-11-12):

Hey everyone! ![:wave:](https://ethereum-magicians.org/images/emoji/twitter/wave.png?v=12)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/p0s/48/535_2.png) p0s:

> introducing specific new RPC methods (e.g. eth_changeNetwork )

Would suggest this one to be `net_changeNetwork`, which I had seen previously suggested in GitHub.

---

**p0s** (2018-11-29):

The provider Ring is now officially a thing! Thanks [@jpitts](/u/jpitts) for adding the category!

Everybody feel free to add your topics for discussion and invite relevant people!

-> https://ethereum-magicians.org/c/working-groups/provider-ring

[@rmeissner](/u/rmeissner) [@ryanio](/u/ryanio) [@wolovim](/u/wolovim) [@bitpshr](/u/bitpshr) [@jeluard](/u/jeluard) [@rachelhamlin](/u/rachelhamlin) [@andrey](/u/andrey) [@kaichen](/u/kaichen)

