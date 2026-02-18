---
source: magicians
topic_id: 7326
title: Rinkeby Faucet - a new one
author: PatrickAlphaC
date: "2021-10-23"
category: Protocol Calls & happenings
tags: [faucet, rinkeby]
url: https://ethereum-magicians.org/t/rinkeby-faucet-a-new-one/7326
views: 21930
likes: 22
posts_count: 14
---

# Rinkeby Faucet - a new one

This will be a duplicate of [Rinkeby Faucet - A new one · Issue #241 · ethcatherders/PM · GitHub](https://github.com/ethereum-cat-herders/PM/issues/241)

If we make an issue on something like Geth, it just gets spammed with rinkeby requests.

Right now, the Rinkeby faucet has been incredibly sportatic, and at the time of writing, it’s been down for a few days. https://faucet.rinkeby.io/

This makes new developers journies into the space borderline impossible, especially for NFT developers who might use something like opensea to test their NFTs, as opensea uses the rinkeby testnet.

I’d love for an initiative to happen to find out:

1. Who currently admins the current faucet?
2. How we can ask for 10,000,000 ETH (at least, as a starting point) to run a second faucet?

The current faucet has *plenty* to go around - 0x31b98d14007bdee637298086988a0bbd31184523

## Replies

**boris** (2021-10-23):

I’d also add — where is the source code of the rinkeby faucet?

I guess this is a Geth specific PoA testnet so likely the Geth team runs it?

---

**PatrickAlphaC** (2021-10-23):

I found out from a tweet the [@karalabe](/u/karalabe) runs it.

https://twitter.com/peter_szilagyi/status/1360643344930643968

[@karalabe](/u/karalabe) can we DM to maybe discuss giving you some help on the faucet? Either with a second faucet or having someone given access to go in and fix whatever is wrong?

This is on the critical path for new engineer adoption, and it’s causing a lot of new engineers to leave the space when the tools don’t work.

---

**jpitts** (2021-10-24):

If there is to be a larger pool of Rinkeby ETH, I would propose that a Rinkeby Gnosis Safe be used to manage it, then have a spending limit or periodic decisions by keyholders to send sufficient amounts to the well-run faucets.

---

**PatrickAlphaC** (2021-10-24):

I love this.

That way, if one goes down, we aren’t totally screwed. I think we need [@karalabe](/u/karalabe) to weigh in. Does he have sole access at the moment? Might be a cool rinkeby DAO to do with snapshot or something too.

Maybe that’s overengineering it though ahah.

---

**PatrickAlphaC** (2021-10-25):

So we sort of just have to wait on [@karalabe](/u/karalabe) for the ETH? Or is there another rinkeby whale we can delegate this too. I can make the gnosis safe and everything.

Who should be the wallets?

Also, perhaps rinkeby won’t be able to handle the load, and the faucet is intentionally sporatic? I sort of just think “oh, it’s Proof of authority, worst case they just dump old contracts or something. It’s a testnet so no one should complain”.

---

**jpitts** (2021-10-28):

In the meantime, we should consider setting up a test Gnosis Safe and begin collecting some Rinkeby ETH from those who have more than they need.

It really does not take very much of it for a dev to get started w/ using dapps and deploying contracts. If we collect even a few Rinkeby ETH in a Safe we can set up a moderate spending limit for faucet maintainers.

---

**PatrickAlphaC** (2021-10-29):

So I got ahold of him: yay!

He sent me some rETH and we [spun up a new faucet here](https://faucets.chain.link/rinkeby): Yay!

It seemed like it was time thing for him: awwww

I’m happy to send some ETH to a multisig so we can collectively decide what to do with it! I’m a bit nervous about bricking rinkeby though… rinkeby has been awesome since it hasn’t gotten out of control like ropsten.

EDIT: Use https://faucets.chain.link/ now since rinkeby is dying

---

**KimYoungSoo-NFT** (2021-11-08):

I was looking for Rinkeby ETH, and found this forum.

Thank you for sharing your knowledge.

---

**d10r** (2021-12-27):

Is there a place where I could buy Rinkeby ETH? I’d seriously be willed to pay for it. Or swap for Kovan ETH, I have plenty of that.

---

**ajascha** (2021-12-27):

Paradigm has a good faucet: https://faucet.paradigm.xyz/ However, this won’t help you right now since it’s empty but it’s worth bookmarking and checking in on.

---

**syedvkax** (2022-01-03):

Its really helped me a lot, as others are not working but [Faucets | Chainlink](https://faucets.chain.link/rinkeby) is really worked thanks Patrick

---

**tommycham** (2022-01-24):

Thanks Patrick. I finally can test on opensea, as they only accept rinkeby.

---

**abcoathup** (2022-01-24):

- Rinkeby social faucet is back!
- Alchemy’s Rinkeby faucet requires no auth

