---
source: magicians
topic_id: 20228
title: Test accounts need clear warnings
author: CedarMist
date: "2024-06-06"
category: Web > Wallets
tags: [wallet, testing, ux]
url: https://ethereum-magicians.org/t/test-accounts-need-clear-warnings/20228
views: 669
likes: 14
posts_count: 7
---

# Test accounts need clear warnings

Lots of us use accounts with well known keys for testing, such as the `test test test ... junk` Mnemonic which generates the `0xf39Fd`…, `0x70997`…, `0x3C44C`… etc. series of addresses.

**TL;DR these test accounts should have warnings in account lists & when signing using them**

However, these are rarely if ever clearly demarcated as being test wallets in Wallet UIs and other tools. See example from MetaMask:

[![image](https://ethereum-magicians.org/uploads/default/original/2X/2/22dd5dd586f1e6dc53f8d9f03823f9b3f71082c1.png)image365×422 20.9 KB](https://ethereum-magicians.org/uploads/default/22dd5dd586f1e6dc53f8d9f03823f9b3f71082c1)

As a developer that routinely spins up fresh local/ephemeral nodes as part of the testing process it’s a big frustration having to reconfigure my Web3 wallet(s) every time, so having the de-facto standard handful of accounts which are assumed to always be present and have gas is time-saving and convenient.

However, sometime this slips into the real-world by accident. The following story is that of a co-worker (non-developer). At some point he imported one of the test wallets into MetaMask while demoing an app to somebody at a conference, where it remained in his account list for a few months.

Then, needing a new wallet to setup Gnosis Pay, looked in his Metamask and there it was, sitting at the end of the account list after his Ledger and other routinely used accounts, proceeded to go through KYC, and enter that address in, tried to fund the card but the $20 test transaction didn’t seem to go through… strange he thought. Tried sending `0.1 ETH` … but that disappeared!

Initially he thought he’d been hacked, maybe it was malware, a keylogger, was his seed phrase brute forced? Fortunately… the wallet address was one of these test accounts and nothing more sinister, but up until that point there was no indication that basically every every Ethereum adjacent developer has used these accounts at one point or another.

This is yet another story to add onto the giant burning fire of user frustration, this is not the first time something like this has happened - far from it - and it certainly won’t be the last.

But, if we can do one simple thing in our apps, in our wallets, in our services, in our deterministic icon generators:

- Clearly demarcate test accounts with known keys and warn the users, as they may not realize until it’s too late

---

My suggestions:

- Deterministic icon generators: overlaid with a warning sign
- Account name auto-fill, instead of Account N, it could be Test Account!!! N
- When signing, include a big warning that it is a test account

## Replies

**plasmacorral** (2024-06-27):

Is there any reliable source of well known keys for testing, or would that be an implementation detail for each wallet to sort out?

---

**CedarMist** (2024-06-28):

The mnemonic `test test test test test test test test test test test junk` is the de-facto test BIP39 wallet.

These keys & addresses are everywhere in documentation for many many projects, e.g. [@dsnp/contracts - npm](https://www.npmjs.com/package/@dsnp/contracts#default-accounts)

---

**bumblefudge** (2024-09-11):

not everything has to be an EIP, but IMHO some day you’re feeling inspired that might make a great `Informational` EIP, showing the private key and address that `test test...junk` derives to, for example?

---

**CedarMist** (2024-09-13):

Here’s an outline for an EIP:


      ![](https://ethereum-magicians.org/uploads/default/original/2X/c/c2b74ef14ba10e3cb1468e5e7a306e4d85700ce9.png)

      [HackMD](https://hackmd.io/@CedarMist/S1h975-60)



    ![](https://hackmd.io/images/media/HackMD-neo-og.jpg)

###



A standard set of test addresses derived from a known mnemonic for use in Ethereum development frameworks

---

**mrnerdhair** (2024-09-20):

May I also suggest `all all all all all all all all all all all all`, commonly used in Trezor-derived hardware wallet test suites.

---

**wizard** (2024-11-02):

Thank you for bringing up such an interesting topic. I have a question.

Given the common use of well-known test accounts, how could wallet interfaces be further improved to prevent test accounts from being accidentally used in live scenarios? ![:smirk:](https://ethereum-magicians.org/images/emoji/twitter/smirk.png?v=12)

