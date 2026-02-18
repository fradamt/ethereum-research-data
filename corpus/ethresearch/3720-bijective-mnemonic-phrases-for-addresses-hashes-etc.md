---
source: ethresearch
topic_id: 3720
title: Bijective Mnemonic Phrases for addresses, hashes, etc
author: osolmaz
date: "2018-10-06"
category: UI/UX
tags: []
url: https://ethresear.ch/t/bijective-mnemonic-phrases-for-addresses-hashes-etc/3720
views: 3197
likes: 6
posts_count: 11
---

# Bijective Mnemonic Phrases for addresses, hashes, etc

I hope this is not too off-topic.

When doing data analysis on the blockchain, I have to deal with a lot of addresses. Trying to remember and discern them gives me headaches. I tried to offer a solution here:


      [Bijective Mnemonic Phrases](https://solmaz.io/bijective-mnemonics/)


    ![image]()

###

Mnemonic phrases for cryptographic keys, addresses etc.








I need your feedback on this.

There is also an issue with my proposal: the first word of most mnemonics start with the letter ‘a’, which kind of defeats the purpose. This is not due to an error, 20 byte addresses fall into a range where the base conversion results in this accumulation for the first word. I have a few solutions in mind, but first would like to hear your opinion.

## Replies

**osolmaz** (2018-10-06):

I now realize this is off-topic. I couldn’t delete the post, so you can do it if you’re a mod

---

**fubuloubu** (2018-10-07):

I quite like it actually! I really think a different set of words than BIP39 would be required. I cringe thinking about someone inadvertently copy/pasting their seed. I know you design it against that, but it WILL happen lol. At least an input field can reject the word list as invalid (although sizes do the same thing)

You proposal has checksums, right?

---

**fubuloubu** (2018-10-07):

If you do three words (like status does when verifying Transactions) you could probably stick that checksum word at the end, and it would enough entropy to be hard to spoof

Also, imagine if you check summed with colors?

---

**osolmaz** (2018-10-07):

Oh right, we do need to use a different word set if there is to be an app that takes phrases as input.

My main purpose was to increase readability. If people use this as a way of sharing public keys, e.g. on the phone, we have to make sure they don’t share seeds. I’m open to suggestions.

The proposal doesn’t have checksums. Do you mean computing the checksum of an entire phrase, and appending it at the end of its truncated version? Sounds interesting, is this to decrease the risk of collision?

---

**fubuloubu** (2018-10-07):

Decreases the risk of collision, but first and foremost protects against the user making a mistake flopping a word or using the wrong one. Capital and lowercase letters in hex addresses are used to to track the checksum of the address for this purpose.

---

**Cygnusfear** (2018-10-10):

By shuffling the word list I get slightly better visual checksumming:


      [Bijective Mnemonic Phrases](https://cygnusfear.github.io/bijective-mnemonics/)


    ![image]()

###

Mnemonic phrases for cryptographic keys, addresses etc.

---

**osolmaz** (2018-10-10):

[@Cygnusfear](/u/cygnusfear) Good idea, and simple too.

Still, the first word will be one of the first 100 from the list most of the time. I should try to find a bijective map that

- addresses this problem,
- keeps the same number of words/digits per hexadecimal number,
- is easy to compute.

Going to delve into the issue when I find the time.

---

**osolmaz** (2018-10-23):

[@fubuloubu](/u/fubuloubu) I created an alternative word list that can be used for public stuff. I gleaned the most commonly used English words online, and tried to find ones that aren’t used in BIP39.

It would be great if you could check whether there are words that shouldn’t be there and/or propose alternatives.


      [github.com](https://github.com/osolmaz/bijective-mnemonics/blob/9391d725e6ff0e74a061b0e1e5ac56850bd6048c/public_english_word_list.txt)




####

```txt
abdomen
abduct
abolish
abroad
abrupt
absence
absolute
absolve
abstain
abusive
academy
accent
accept
acclaim
accord
accurate
acorn
acrobat
acronym
activity
```

  This file has been truncated. [show original](https://github.com/osolmaz/bijective-mnemonics/blob/9391d725e6ff0e74a061b0e1e5ac56850bd6048c/public_english_word_list.txt)

---

**fubuloubu** (2018-10-23):

BIP39 has some extra stuff I think to make sure all words have at least the first 4 letters unique, so that you can type in and suggest the word after 3 letters, and that any 4 letter combo is enough to get the whole word.

---

**drhus** (2018-10-27):

[@osolmaz](/u/osolmaz) check out https://github.com/mbrubeck/mnemonic.js and

- RFC1751
- Mnemonic Phrase
- BIP-0039
- Trezor Mnemonics
- Phonetic Alphabet
- PGP word list
- singpolyma/mnemonicode
- RFC1760
- RFC2289

IMO we’ve in place decent work shortlisting a word list would presumably have a similar finality…

