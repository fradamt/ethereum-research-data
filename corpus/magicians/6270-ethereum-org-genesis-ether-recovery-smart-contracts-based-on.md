---
source: magicians
topic_id: 6270
title: "Ethereum.org: Genesis Ether Recovery Smart Contracts based on Oracles for Identity Proving"
author: mindey
date: "2021-05-18"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/ethereum-org-genesis-ether-recovery-smart-contracts-based-on-oracles-for-identity-proving/6270
views: 1032
likes: 3
posts_count: 6
---

# Ethereum.org: Genesis Ether Recovery Smart Contracts based on Oracles for Identity Proving

Ethereum Genesis pre-sale happened on `ethereum.org`, whereby people used the website (`github.com/tagawa/website`) to generate `encseed`. For example, I’ve contributed to Ethereum Genesis sale on `ethereum.org`, but lost access to the genesis wallets containing `3325.11 ETH`, as described in [[1]](https://github.com/ethereum/ethereum-org-website/issues/3069), and [[2]](https://discord.com/channels/595666850260713488/595701895700676644/844211170919186432). So, basically, I’ve contributed to the creation Ethereum, but I’m left with nothing.

I would like to create of a Genesis Ether recovery toolkit for `ethereum.org` website, that would allow an arbitrary Ethereum address holder to go into *smart contract with the `ethereum.org`* organization (where the Ether Sale happened), based on constructing a proof of one’s identity based on oracles, like Bitcoin, Cryptsy and Gmail, as I still hold passwords and access keys to those systems, and would like to use them to prove sameness of human identity.

I’d appreciate your thoughts on a protocol for Genesis Ether recovery based on external facts, because, as described in [1], [2], I had made the password really long (I guess approx 64 chars long), and split it into two parts, one part on a paper (that I still have), and another part on computer (that I lost irrecoverably). With such long passwords, I have no hope in direct cryptographic proof, and therefore the topic.

Thanks!

## Replies

**mindey** (2021-05-18):

I suppose, while such oracles-based proofs would likely be of lower statistical significance level than direct cryptographic proofs, but yet, they would still be of sufficiently high significance level for holding them valid for all practical purposes to distribute Ether to those who constructed them; and, considering that Ethereum has a way for community to decide about the inflation rate, perhaps specialized recovery fund tied to a smart contract for recovery could be created? How do you think?

---

**matt** (2021-05-18):

Hi [@mindey](/u/mindey), I’m sorry to hear you lost access to this wallet. Unfortunately, there isn’t anything that can be done. The topic of fund recovery has been discussed at length in the past (see [EIP-867](https://eips.ethereum.org/EIPS/eip-867)). There is no desire to introduce a mechanism into the protocol that allows for stuck funds to be recovered. This is for many reasons, but we shouldn’t rehash here. I recommend you read the prior discussions on the topic.

---

**mindey** (2021-05-19):

*// I also lost access to some of mine //*

[@Rose2161](/u/rose2161) hope not all of it!

*// What happened? //*

Since the communication between me and ether sale [website](https://web.archive.org/web/20140815223959/https://www.ethereum.org/) was already encrypted, and the whole generation happened on my browser, I assumed that I downloaded actual raw wallets, and, assumed that the password is just to prevent the e-mail providers from peeping into the backups, so I didn’t take as much care to make sure that long password is backed up twice.

There was no verification step asking to try to decrypt downloaded wallet on my computer to ensure the final product is in tact and decryptable, before closing the browser window. End result: I’ve got a paper note of 45 characters length password, that doesn’t work, and I’ve got a faint memory that there was more to it.

---

**stev69** (2022-07-24):

I’ve  also lost access to 2500 enjin coins . I brought them at  ico and mew has only made around 10 transactions total.  Almost all of those transactions are to my Binance account which is verified etc.  It’s undoubtedly me. there’s been no  transactions for 3 years I know my public address  , password . but back then mew encouraged you to access your account with your json file. so i did. Anyway long story short I lost the computer and therefore the private key.  It’s driving me mad.  IS THERE STILL NOTHING THAT CAN BE DONE???

thank you

---

**mindey** (2022-07-25):

The most deceptive thing was, that people who made the [ethereum.org](http://ethereum.org) sale site `(https://github.com/tagawa/website)`, had assumed that user’s machine and connection is compromised, and made us download encrypted private key, instead of decrypted… Basically, I trusted that what I had downloaded will be sufficient, and searched for the original download, but even after I found it, it was not sufficient. My immediate assumption was:

1. Ok, you ask me password for backups, because you’ll be sending those backups to my e-mail address – I can understand that, – to prevent mail provider from peeping into my wallet.
2. But, what I had saved directly from ethereum.org is the wallet in pure unencrypted form (cause, why would one need to encrypt something from me? I’m not the 3rd party like my mail provider is.)

The reality was:

1. They sent the encrypted wallets to mail provided.
2. They also encrypted the wallet before I could save it to my disk.

So, even after finding the original file, that I saved not from backup, but the very very original, I could not use it… ![:frowning:](https://ethereum-magicians.org/images/emoji/twitter/frowning.png?v=12) UX: I’m given the thing, where I thought I made password just for backups, but in reality, this password also was used to encrypt me the original. So, your generator never gave me the original private key! Which is, unfair… I paid for it, but did not get it.

