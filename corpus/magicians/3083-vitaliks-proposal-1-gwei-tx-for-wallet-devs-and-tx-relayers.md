---
source: magicians
topic_id: 3083
title: "Vitalik's proposal: 1 gwei/tx for wallet devs and tx relayers"
author: Ethernian
date: "2019-04-03"
category: Web > Wallets
tags: [wallet, eth1x, funding]
url: https://ethereum-magicians.org/t/vitaliks-proposal-1-gwei-tx-for-wallet-devs-and-tx-relayers/3083
views: 1361
likes: 4
posts_count: 12
---

# Vitalik's proposal: 1 gwei/tx for wallet devs and tx relayers

Some times ago Vitalik has proposed to allow wallets collecting 1gwei gas for transaction they are constrution.


      [twitter.com](https://twitter.com/VitalikButerin/status/1103997378967810048)




####



  https://twitter.com/VitalikButerin/status/1103997378967810048








I mean it was a very reasonable approach to incentivize all the infrastructure preparing transactions to be signed: wallets, relays, bridges, dapplets (shameless self-promotion ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=9) ).

What is the current mood of the community about it?

If it is positive, we should start thinking about enabling multisends in transactions.

CC: [@pedrouid](/u/pedrouid), [@ligi](/u/ligi), [@danfinlay](/u/danfinlay)

## Replies

**timbeiko** (2019-04-03):

One major downside is that this reduces (removes?) privacy for people using clients and sending transactions.

---

**Ethernian** (2019-04-04):

Could you explain, please? I don’t see the problem.

---

**timbeiko** (2019-04-04):

So, in the best case, where there is one donation address per client, it leaks which client each transaction is using (because it also donates to the address).

If you only have 1 address/client, then these become significant honeypots, so clients may move to a different model (i.e. 1 address/client version), which leaks even more information.

---

**danfinlay** (2019-04-04):

Clients could also generate a recipient address per user, and then transfer funds through aztec protocol or a zk-rollup exchange, so I don’t think privacy is a fundamental problem with this proposal.

---

**timbeiko** (2019-04-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danfinlay/48/4187_2.png) danfinlay:

> a recipient address per user

Wouldn’t this be worse, given that one user may then link their N accounts if they send all their txns via the same client? Could 1 address/transaction be possible?

---

**danfinlay** (2019-04-04):

Sorry, I should have said per account.

---

**Ethernian** (2019-04-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> it leaks which client each transaction is using (because it also donates to the address).

What if the wallet would generate an additional raiden payment for every Tx sent? It could be possible to use one channel for all addresses in the wallet… So it will leak just raiden payments, but with no correlation to main accounts.

---

**timbeiko** (2019-04-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> What if the wallet would generate an additional raiden payment for every Tx sent?

I’m not super familiar with the ins and outs of Raiden, but I doubt that all major clients + wallets would add a 3rd party dependency to handle this. I could be wrong, though ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) !

---

**charles-cooper** (2019-04-08):

This is kind of neat! As a complementary idea, maybe transaction recipients (the `to` field of a tx) can also receive part of the transaction fee. The miner should be willing to provide this ‘kickback’ because the recipient ‘brought them’ some business. This would be intended as a standard, decentralized (and uncensorable and plausibly deniable) way for contract developers to build a revenue stream.

---

**Alexintosh** (2019-08-22):

I would love to see this idea being reconsidered.

---

**Ethernian** (2019-08-22):

Maybe we could resolve it as part if the dapplets proposal.

Catch me in Berlin this week for a small talk.

Telegram: [@ethernian](/u/ethernian)

