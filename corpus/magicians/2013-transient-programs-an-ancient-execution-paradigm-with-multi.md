---
source: magicians
topic_id: 2013
title: Transient programs, an ancient execution paradigm (with multi-send example); and why storage clean-up doesn't happen
author: veox
date: "2018-11-25"
category: Magicians > Primordial Soup
tags: [ux, multisend, storage-cleanup, transient-program]
url: https://ethereum-magicians.org/t/transient-programs-an-ancient-execution-paradigm-with-multi-send-example-and-why-storage-clean-up-doesnt-happen/2013
views: 2367
likes: 3
posts_count: 3
---

# Transient programs, an ancient execution paradigm (with multi-send example); and why storage clean-up doesn't happen

This started out as a reply to [a message in another thread](https://ethereum-magicians.org/t/ethereum-1-dot-x-a-half-baked-roadmap-for-mainnet-improvements/1995/6), but boiled off into a rant.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/f04885/48.png)[Ethereum 1 dot X: a half-baked roadmap for mainnet improvements](https://ethereum-magicians.org/t/ethereum-1-dot-x-a-half-baked-roadmap-for-mainnet-improvements/1995/6)

> I was also wondering if setting non-zero values to zero could be not only subsidized but rewarded, as a way to incentivize clearing unused storage.

That has essentially [been answered](https://ethereum-magicians.org/t/ethereum-1-dot-x-a-half-baked-roadmap-for-mainnet-improvements/1995/12).

---

However, I’d like to add that the currently dominant contract architecture, coupled with wallet design tropes, prevents the `SSTORE`-refund incentive from being usable.

For people to want to clean up after themselves, the cleaning-up has to happen within the same transaction as some other “useful” work. But there is no way to “chain” the two.

GasToken currently [suggests using it from within other contracts](https://gastoken.io/#using-gst), but this puts users at the mercy of contract developers. Also, from observing the ecosystem for years, most (sane) developers are reluctant to put code into their contracts that is not strictly related to its business logic.

If we want to incentivise certain kinds of behaviour, we must incentivise the users, not the contract coders - as, ultimately, it is the users that are the initiators of transactions that result in storage increase; and coders all too often have the option of shifting costs onto users anyway, so tend to be less frugal.

---

I’ve been working recently on an alternative program execution paradigm, which I call *transient* programs (in comparison to *resident* programs, commonly known as “contracts”).

For a short (and wholly-incorrect) explanation of what it is, to people who are familiar with Solidity only: “it’s like stuffing everything into the constructor”.

Transient programs execute at the bottom of the call stack, and are calling nobody (leaving the `to` field empty).

An example of such a program, implementing ether multi-send, can be seen [on gitlab](https://gitlab.com/veox/lll-multisend/blob/002627e6aab9af4b375286d4daef16bc52053108/contracts/multisend-transient-ether.lll) (or, with minimal `lisp` syntax highlighting, [at the github backup](https://github.com/veox/lll-multisend/blob/ad4635212d44a12b0f1ae3efed6c64fc120f7f33/contracts/multisend-transient-ether.lll)).

(Also of interest is perhaps the [Python test case](https://gitlab.com/veox/lll-multisend/blob/002627e6aab9af4b375286d4daef16bc52053108/tests/test_multisend_transient_ether.py), which shows how a transaction using this can be constructed; and [this transaction on Ropsten](https://ropsten.etherscan.io/tx/0xf91c5211e2dbf219f7855171b8a20c7eb17ae0d97c0516ab6a9b731abd06b57b) showing a simple send to 2 recipients (wasteful).)

---

Using transient programs could remove the need for explicit GasToken support in end-contracts (as is currently suggested by GasToken crew), special “clean-up proxy contracts” (*proxy this proxy that ugh the word is as sickening by now as your lack of imagination get a dictionary*), `batchStuff()` functions that bloat contracts; and the general notion that for code to run, an authority has to deploy it first.

It could allow for vastly more to be “garbage-collected”; what comes to mind immediately is outdated ERC-20 allowances and ~~spam~~ naïve air-drop ERC-20 balances, both of which are relatively easy to track by wallet software.

---

I’ve called this execution paradigm “ancient” in the title, because that’s how ~~contracts~~ resident programs have been created since forever: a certain kind of a transient program claims a tiny bit of address space, where it pushes its payload.

However, development of *transients* seems to have stopped immediately afterwards; and *residents* are now completely entrenched.

I can’t start imagining how to convince wallet makers that this feature is one that they’d want to develop and support. Most wallets (all?..) don’t even have a way to deploy user-provided residents (they don’t allow leaving the `to` field empty).

---

Perhaps the above is too tongue-in-cheek; and this is a use pattern that no one thought of (not counting me sitting on my hands…). Indeed, some EVM design choices tend to suggest so.

If you followed either of the LLL links above, you’d have read that:

> In a transient program, both code and data must be passed in the same transaction field. Although called “transaction data” when viewed externally, it will be available as code in its entirety during execution.

In [the linked repository](https://github.com/veox/lll-multisend/tree/ad4635212d44a12b0f1ae3efed6c64fc120f7f33/contracts), it seems awkward that the resident variant accesses its data via `CALLDATALOAD`, whereas the transient has to resort to `BYTECODESIZE`.

The fact that leaving the `to` field empty results in increased gas use - by way of a `nonce`d account address assignment, instead of just using the EOA’s address and deferring the `nonce`-ing until an actual `CREATE` is requested, - suggests that “contract deployment” at this point is expected. (For this reason, the linked transient multi-send program only starts saving gas when having at least 5 recipients.)

---

I was thinking of having this ready around Devcon; for many reasons, a month later, it’s in a state as sorry as ever - so here you go, a rant for a `README`.

## Replies

**veox** (2018-11-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/veox/48/10_2.png) veox:

> It could allow for vastly more to be “garbage-collected”; what comes to mind immediately (…)

A slightly less universal example would be `SHARE`-backed orders on resolved Augur markets; and, generally speaking, losing shares - in markets and disputes (although perhaps these fall under the “ERC-20 balances” category).

I invite all to come up with more examples of garbage that you’d totally get rid of, if doing so ~~was useful~~ didn’t come at your own petty loss. Especially if it’s not related to ERC-20 tokens.

---

**veox** (2019-06-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/veox/48/10_2.png) veox:

> I invite all to come up with more examples of garbage that you’d totally get rid of, if doing so was useful didn’t come at your own petty loss. Especially if it’s not related to ERC-20 tokens.

The opposite of what I asked: transients *could* be used to mount efficient sybil exploitation of [these sorts of disgraceful “airdrop” contracts](https://www.reddit.com/r/ethereum/comments/bvkvuz/using_20_of_all_gas_atm_an_airdrop_contract_with/).

