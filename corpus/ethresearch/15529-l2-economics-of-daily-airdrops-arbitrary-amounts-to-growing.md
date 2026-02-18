---
source: ethresearch
topic_id: 15529
title: L2 Economics of Daily Airdrops (Arbitrary Amounts to Growing Base of Players)
author: cleanapp
date: "2023-05-08"
category: Economics
tags: []
url: https://ethresear.ch/t/l2-economics-of-daily-airdrops-arbitrary-amounts-to-growing-base-of-players/15529
views: 1838
likes: 3
posts_count: 6
---

# L2 Economics of Daily Airdrops (Arbitrary Amounts to Growing Base of Players)

hi fam … we really need your help optimizing the cost of a daily airdrop-like distro for our game

in our game, players win different amounts of points each day

- at 19:45 UTC, everyone’s individual balance is calculated offchain (including some referral bonus points calcs) & a universal snapshot is taken: Player A = 59 points; Player B = 182 points; … Player N = 12 points.
- at 20:00 UTC, the token script ingests the snapshot & distributes ERC20 tokens commensurate with the Players’ daily accrued point balance
- from players’ POV, there is no “Claim” required; there is zero financial cost to play; we abstract blockchain away until such time as players want to interact with their ERC20 versions of their points & do whatever they’ll want to do with their points (tldr: CleanApp-the-game pays for the daily distro)
- we’re optimizing gameplay for maximum number of players (10M+), so need a scaling solution that’s cheap and secure

**Questions**:

- what’s the cheapest L2 for our game? (Mumbai to start (?); also considering Gnosischain, Scroll, Optimism, but could really use guidance + ecosystem support) - dms open, just @ us wherever you like to @, the handle’s the same everywhere
- obv, our goal is to optimize gas costs: what’s the state-of-the-art for recurring arbitrary token distros like the ones described above?
- @sg mentioned this optimization, and curious to learn about other approaches
- will xpost this in magicians as well, and suspect there are other WGs on this … could you pls give pointers … ty … xoxoxo

## Replies

**MicahZoltu** (2023-05-12):

Once a day publish a tree root (merkle or verkle or something) on-chain along with an IPFS hash for a file containing the full tree.  User clients would then be able to see their points by looking at the tree.  When the user is ready to do an on-chain withdraw or transfer, they would submit a tree proof and execute the withdraw.  As part of the withdraw, the tree proof would be validated and the amount withdrawn would be written on-chain.  The amount withdrawn is the amount in the tree minus any amount previously withdrawn.

In order to protect users from a dev rug, you could make it so the value in the trees can only increase, never decrease, by requiring the author of the tree provide a ZK Proof that the newly published tree only contains additions over the previous tree.  On-chain (once a day) they would publish the tree root + IPFS hash + proof on-chain and the transaction would reject if the proof was invalid.

The one remaining potential issue is data availability.  There isn’t a way to prove that the data is available on IPFS.  To deal with this, you can make it so people can choose to use any historical tree root for withdraws, so publishing a new root with an unavailable IPFS hash doesn’t prevent withdrawing from happening.

The UI should be designed such that this all is transparent to the user, the app would look for the most recent available IPFS hash when withdrawing and maybe give the user a little warning if they are withdrawing from a stale hash (but still allow it).

---

**parseb** (2023-05-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> There isn’t a way to prove that the data is available on IPFS.

Filecoin’s [FVM](https://docs.filecoin.io/smart-contracts/fundamentals/the-filecoin-virtual-machine/) might be able to do that for you. Probably also cheap.

---

**MicahZoltu** (2023-05-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/parseb/48/10942_2.png) parseb:

> Filecoin’s FVM might be able to do that for you. Probably also cheap.

I don’t think we can prove this on Ethereum in a trustless way?

---

**parseb** (2023-05-18):

No, not on Ethereum, not by default. Can’t informatively ponder over the possibility.

---

**cleanapp** (2023-05-18):

Thank you all for these insights. Extremely helpful.  Will post updates here on our chosen implementation as we move this part of the stack along.

