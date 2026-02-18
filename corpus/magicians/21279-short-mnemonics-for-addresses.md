---
source: magicians
topic_id: 21279
title: Short mnemonics for addresses
author: superlouis.eth
date: "2024-10-06"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/short-mnemonics-for-addresses/21279
views: 142
likes: 5
posts_count: 6
---

# Short mnemonics for addresses

Hello!

I have been working on a protocol to map addresses to short mnemonic phrases, to make it easier and safer to handle them. The concept is simple: every address that “appears” on the chain (sends/receive a transaction, smart contract creation, etc…) is assigned a position number. This number is then converted to a mnemonic as BIP39 does it for seed phrases.

Since the number is still rather small (less than 300M addresses have been witnessed on mainnet), the resulting phrase is short. With 11 bits per word, 8 billion addresses could be “encoded” on 3 words.

A demo can be tested here. It also shows how this can be integrated with ENS and used on any wallet/explorer that supports ENS offchain resolution:


      ![](https://ethereum-magicians.org/uploads/default/original/2X/3/3d64c21d7c3be763817851c5b1d3eee8d2bd729b.png)

      [addr.id](https://addr.id)



    ![](https://ethereum-magicians.org/uploads/default/original/2X/f/f8beea1ddf8d3af20896b096e23b318a677d3f54.png)

###



Monique is an Ethereum address naming service










This demo reserves 4 bits for a checksum. I thought it would help lowering the risk of typing a wrong word and getting a different address. However, every bit of checksum divides the number of possible addresses by 2.

I considered using less bits for the checksum, and I’m wondering if I should use a checksum at all: most of the addresses are garbage (old wallets, spam…) and the risk of generating a close mnemonic to trick a user into sending funds to an attacker was low. Especially since the attacker must detect the address at its creation.

A bigger address space would help integrate Layer-2 addresses without overflowing to 4 words.

Note: mnemonics for 3 or more words are immutable, they will always point to the same address. I reserved the 2-words mnemonics for ENS-like registration that will be mutable and transferrable.

I would be happy to hear any feedback regarding this idea. Also, what would be your opinion on the checksum ?

Thank you!

## Replies

**Hugo0** (2024-10-10):

I think this is a great idea! I tweeted about this a while ago [here](https://x.com/uwwgo/status/1825622658735862017). Maybe the discussion is helpful

I don’t think having 2 words for special addresses helps, what3words doesn’t do that for a good reason.

---

**wjmelements** (2024-10-10):

As for the phrase itself, a sentence would be most memorable, and this can be done by restricting the 3 words to Subject Verb Object.

---

**Hugo0** (2024-10-10):

Alice: “what’s your address?”

Bob: “I love d**k”

Idk if Subject Verb Object is a good idea honestly ![:sweat_smile:](https://ethereum-magicians.org/images/emoji/twitter/sweat_smile.png?v=12)

---

**wjmelements** (2024-10-10):

There are sufficiently many english nouns that profanity can be avoided. However I do see a few grammatical issues for this unique to English so I agree it’s not great.

---

**superlouis.eth** (2024-10-11):

Thanks for the feedback! You’d be surprised to see how many 3-word combinations (from the default BIP39 list) make interesting (understand: funny and/or inappropriate) sentences. I thought I’d leave as little rules as possible and let randomness do its thing.

[@Hugo0](/u/hugo0) I originally named the project “eth3words” because it started from the exact same idea ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

