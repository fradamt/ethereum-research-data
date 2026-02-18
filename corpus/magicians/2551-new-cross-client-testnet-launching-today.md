---
source: magicians
topic_id: 2551
title: New (cross client) Testnet launching today
author: ligi
date: "2019-01-31"
category: Web > Wallets
tags: [wallet]
url: https://ethereum-magicians.org/t/new-cross-client-testnet-launching-today/2551
views: 1048
likes: 8
posts_count: 6
---

# New (cross client) Testnet launching today

Today will be the launch of the görli testnet at [GörliCon](https://goerli.net) (with chainID and networkID 5) - prepare your wallets! This testnet is exciting as it brings geth and parity closer together. Before geth and parity had separate PoA testnets (geth:rinkeby | parity:kovan) - now there will be a PoA tetnet where both clients (and more clients) can work together in harmony.

## Replies

**lrettig** (2019-01-31):

Here is [@5chdn](/u/5chdn)’s original post about Goerli: https://dev.to/5chdn/the-grli-testnet-proposal---a-call-for-participation-58pf. TIL that it actually has support for five clients! In addition to geth and parity there’s pantheon, nethermind, and ethereumjs. Very cool.

---

**pedrouid** (2019-02-08):

Is there a public rpcUrl available for Goerli right now?

---

**ligi** (2019-02-08):

Yes multiple - find them here: https://mudit.blog/getting-started-goerli-testnet/

we should really add them to chainid.network https://github.com/ethereum-lists/chains/issues/12

---

**pedrouid** (2019-02-08):

Thanks! Yeah, I agree. I’m going to do that

---

**pedrouid** (2019-02-08):

[github.com/ethereum-lists/chains](https://github.com/ethereum-lists/chains/pull/20/)














####


      `master` ← `rpc_url`




          opened 11:11PM - 08 Feb 19 UTC



          [![](https://avatars.githubusercontent.com/u/10136079?v=4)
            pedrouid](https://github.com/pedrouid)



          [+78
            -41](https://github.com/ethereum-lists/chains/pull/20/files)







Fix #12

