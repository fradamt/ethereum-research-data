---
source: ethresearch
topic_id: 15009
title: Anyone looking for a job oppportunity to work on an EVM innovation?
author: iulianivg
date: "2023-03-09"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/anyone-looking-for-a-job-oppportunity-to-work-on-an-evm-innovation/15009
views: 978
likes: 1
posts_count: 3
---

# Anyone looking for a job oppportunity to work on an EVM innovation?

Hi guys,

Working on implementing at EVM level a few cool, fun features. Doesn’t need to make it live or be super secure, as it’s just a fun, testnet implementation.

The idea is to start from a GETH POA (clique) base protocol. If you’re not familiar with it, that would be EIP-225 at [Clique PoA protocol & Rinkeby PoA testnet · Issue #225 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/issues/225)

We would then make changes at core level to add one easy task and one advanced one:

- From the gas fee, 40% goes to validator, 60% is burned
- Rebasing mechanism similar to an ERC20 token. E.g every 15 minutes, the entire supply in all wallets increases.

As far as I understand, the “easy” task (the fee split) will likely be affected by the more difficult task of rebasing. I am open to DMs for anyone interested. Also if anyone has already worked on this (rebasing, which I doubt), feel free to share your experience.

## Replies

**jiayaoqijia** (2023-03-09):

For the first one, it’s straightforward to change the destination addresses.

For the second one, it may take a lot of time to generate the entire trie state after the state changes for all accounts, especially there can be tons of millions of accounts.

---

**iulianivg** (2023-03-09):

I think the second one sounds worse than it may appear.

For instance, we can have a global variable known as “fragments”.

For each address there are two balances:

- an internal balance (what currently EVMs use to track)
- a display balance which in our case is the real balance multiplied by the fragments

Say when the chain starts I have 100 COIN balance, 0x123 has 50 COIN balance.

Then on rebase, the number of fragments increases to 0.1.

My new transferable balance is 100 + 100 x 0.1 = 110

0x123 is 50 x 50 x 0.1 = 55

For sure it’s not as straightforward to implement. Let me know what you think

