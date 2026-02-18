---
source: ethresearch
topic_id: 3482
title: "Wallet Shape Address Human-friendly Visualization of Wallet Address : Momcode"
author: drhus
date: "2018-09-22"
category: UI/UX
tags: []
url: https://ethresear.ch/t/wallet-shape-address-human-friendly-visualization-of-wallet-address-momcode/3482
views: 9186
likes: 6
posts_count: 34
---

# Wallet Shape Address Human-friendly Visualization of Wallet Address : Momcode

We both know, crypto wallet addresses are weird, complex, difficult to recognize or remember, that was our first impression when we first learned about bitcoin and today it is also the first, second and third impression of friends and family we are onboarding to crypto-land.

# The problem

- You can hardly memorize, recognize or distinguish this
0x6719a70e3b9652d0cd3d4cd28a93556497e2bf96
From
0x6719a25fd0b48da00cd865e1f45ea6216b90bf96
- You can hardly transmit the address or QR code via a voice channel

# Solution

Human brain has great capacity to recognize patterns and retain complex visual perceptions, when he can make sense of it, and the most recognizable *in this context* are geometric shapes & colors, what if the wallet address could be express (encoded) in Colorful Symbols string *(using basic 6 unambiguous colors and set of universally recognizable symbols like triangle, square, circle, star, heart arrow.. etc)*

So this address: 0x6719a70e3b9652d0cd3d4cd28a93556497e2bf96

[![Screenshot%20of%20Momcode%20summary%20-%20Google%20Docs](https://ethresear.ch/uploads/default/original/2X/d/de2547435971e9a8aca7c57a836afd78105db3cd.jpeg)Screenshot%20of%20Momcode%20summary%20-%20Google%20Docs638×568 56 KB](https://ethresear.ch/uploads/default/de2547435971e9a8aca7c57a836afd78105db3cd)

# Progress

In order to advance this research toward 1) final Encoding Dictionary 2) representation models *(string, square, QR overlapping.. etc)*

I put together small test-lab [Momcode :: Deterministic Visual Identifier | Test Lab v0.6](https://momcode.io/lab/) which allows Hex Table manipulation and you forming your own Encoding Dictionary Proposal which you could export/share with URL link or PR on github [GitHub · Where software is built](https://github.com/drhus/momcode/milestones)

## Replies

**gluk64** (2018-09-23):

So, there are two distinct problems here:

1. we want something easy to visally recognize
2. we want something easy to transmit over voice

What do you think about identicons for the (1)? They are a de-facto standard already.

How about [BIP39 words](https://github.com/bitcoin/bips/blob/master/bip-0039/bip-0039-wordlists.md) for the (2)? 16 words will cover a 160 bit address.

---

**MaverickChow** (2018-09-23):

Aren’t those ‘robot faces’ that we get every time we generate new addresses from MyEtherWallet or MyCrypto good enough for the same purpose of memorization, recognition, and differentiation?

The ‘robot faces’ take up far less space and can sometimes look cute too.

I got one ‘robot face’ that looks like a cyclops sheep, while another one that looks like an innocent-looking smurf.

What will imitate / produce all the myriads of differing voices (assuming a holder has multiple addresses) for transmission? If it requires the press of a button, then what limitation do the ‘robot faces’ pose that technology cannot resolve?

**Or maybe we should find a way to scan those ‘robot faces’ for their corresponding addresses?**

**Then all we need is just carry our ‘robot faces’ around.**

Edit: My mistake for misunderstanding what author meant by voice transmission but now that I do, I still do not understand how superior / effective / efficient is “red scissor” to “nine six”, or “green speaker” to “six seven”. Neither do I understand in what situation would voice transmission be the only viable option.

---

**virgil** (2018-09-23):

[@drhus](/u/drhus) Please don’t add emoji to the title of your posts.  I removed them.

---

**Cygnusfear** (2018-09-23):

Hi everyone; [@drhus](/u/drhus) it seems you have stumbled upon something I have also been experimenting as a chrome extension so I hoped this comment thread could be of use to mention: [Feedback on "ETH Avatar Standard" Direction · Issue #928 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/issues/928#issuecomment-389439986)

My personal takeaways:

- There is a lot of added value in being able to recognise a hashed address (you cannot humanly/safely compare similar addresses)
- Colors are easier to distinguish/remember than symbols and shapes
- Emoji range has a lot of similar emoji. A LUT with select emoji is better than the whole range

PoC extension:

https://github.com/Cygnusfear/IdentiAddress

Argent wallet is using something resembling this concept for their key recovery:

https://medium.com/argenthq/decentralised-and-seedless-wallet-recovery-5fcf7dddd78d

Kind regards!

---

**drhus** (2018-09-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/gluk64/48/11557_2.png) gluk64:

> How about BIP39 words for the

BIP39 mnemonic is a fabulous gadget for generating deterministic keys (private key), but you can’t express your Wallet Address (public key) with that 2048 words. however [PGP word list](https://en.wikipedia.org/wiki/PGP_word_list) can do that, encode any hex hash in word list, and despite the fact it’s only English, Momcode Geometrical Shapes and Colors are to recognize, memorize, and highly recognizable across nations/languages

![](https://ethresear.ch/user_avatar/ethresear.ch/gluk64/48/11557_2.png) gluk64:

> identicons

![](https://ethresear.ch/user_avatar/ethresear.ch/maverickchow/48/2858_2.png) MaverickChow:

> ‘robot faces’

Do you remember your Identicons, or [Blockies](https://github.com/ethereum/blockies) of myEtherWallet, myCrypto, Ethereum wallet and Mist?

I do remember last 3 digits of my wallet address *(and i know widely people memorize first or last digits of their addresses)* but I can’t remember my Blockie icon at all, it’s just great for comparing and matching.

Secondly, all Identicon family including Blockies, MonsterID, Retro, Vash, Jdenticon, Jazzicon, IdentiHeart, and Robohash works beautifully as 1) avatar 2) comparing and matching,

but it is not transmittable via voice/phone and much harder online (for decoding)

it’s something you will have along-side your wallet address (will never replace it for day-to-day use)

While Momcode could be used with some adjustments as 1) replacement of Idneticion/blockies (avatar / matching and comparing 2) with Momcode keyboard *-something like emoji keyboard but for wallets-* can replace the address on day-to-day use completely 3) Scan on similar fashion to QR code

I would say Momcode could be seen as just **describable Identicon**, with higher recognizability and Memorability.

---

**drhus** (2018-09-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/maverickchow/48/2858_2.png) MaverickChow:

> understand how superior / effective / efficient is “red scissor” to “nine six”, or “green speaker” to “six seven”. Neither do I understand in what situation would voice transmission be the only viable option

I hear you, and I totally agree, green speaker 🕪 isn’t superior to 67

but as a string of arbitrary hex ex. **0xA3F0272F35** is inferior to ▲🞧🡅♥★ in terms of memorability, distinguishability and transmit-ability particularly for non-english speakers

Transmit-ability over voice channel is actually what triggered the research at first place, I’ve introduced and successfully installed wallets for friends and family, and had a hard time assisting (over the phone) my mom to send Ether from her smart-phone wallet. so we call it Momcode : p

*Important to mention particularly speaker, scissor, airplane, telephone aren’t necessarily going to be there on final version, it’s just on current lists today for experimental… and some characters like start, triangle, heart, square… i’m confident it will stay, but the idea of test-lab is to find the simplest unambiguous set 16 to 32 shapes to be used in combination with basic colors, and then sorted by frequency.*

---

**drhus** (2018-09-23):

[@Cygnusfear](/u/cygnusfear) your approach with IdentiAddress is very interesting, I look forward Etherscan has that kind of built-in instead of chrome extension, I’ve responded over there and your PoC inspired me to add new Encoding Dictionary for testing, check it out https://momcode.io/lab/

---

**gluk64** (2018-09-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/drhus/48/1798_2.png) drhus:

> Do you remember your Identicons, or Blockies of myEtherWallet, myCrypto, Ethereum wallet and Mist?

Hmm, actually I do. I don’t “remember” it in the sense that I can’t describe it, but I recognize it every time I see it. If I can’t recognize the image, I will know it. This is how visual pattern recognition works. I can not describe face of my sister to you, but I easily recognize her.

So a single complex picture is probably better for visual confirmation than a series of simpler ones.

Would be really interesting to see an alternative to blockies that better resembles faces.

![](https://ethresear.ch/user_avatar/ethresear.ch/drhus/48/1798_2.png) drhus:

> but it is not transmittable via voice/phone

Let’s narrow down the problem. You want to be able to transmit the whole address over phone? Or you want to make sure that the address you’ve sent over some digital channel is complete and untampered?

The former seems a really rare use-case: to send “internet money” address to somebody who doesn’t have internet? For the latter, the PGP word list would work just fine: one person reads the words aloud, the other one checks. We will apply the transformation to the hash of the address, so changing just one digit will change the entire series.

BIP39 words are less distinct on pronounciation, but since you only need to compare the phrases this will probably work. The upsides: 1) it’s a standard with multiple languages, 2) since a BIP39 word has higher entropy, you only need 16 of them to describe the address (as opposed to 20 words from the PGP list).

---

**Cygnusfear** (2018-09-24):

[@drhus](/u/drhus)

The lab is great! Is there a repository where I could submit a PR / tweak the encoding?

[@gluk64](/u/gluk64)

This proposal appears to address several goals/problems regarding addresses.

> Communicability: addresses are difficult to communicate verbally

Currently: very prone to human error and a horrible experience

> Identification: Replace the address with something that can be humanly verified / compared / hashed

Currently: Frequently occurring attack vector. URLs are actively targeted this way. Very prone to human error

Blockies only solve identification, there are some downsides to them:

- Downscaling Blockies really hurts their legibility/function (they merge into similar icons)
- Their implementation differs between implementers (metamask blockies are different from etherscan)
- They do not automatically appear for addresses ‘in the wild’ (this can only be done by a browser extension)
- Identification & recognition only works if people have the time to actually develop that pattern recognition (not very useful for new users)

I would prefer these problems to be remedied by ENS. This hinges on the pace of ENS adoption.

To me it appears that momcode appears to be an interim solution for ENS adoption. It addresses some of the shortcomings of Blockies but without large scale adoption suffers from the same adoption problem as ENS (and there are several implementation issues).

I’d say an npm package/library that implements either of these techniques is interesting and might help adoption; however if the implementation is left to the dApp then it creates a false sense of security for the user. All things considered, wallets may be the only third party to which the user can delegate such ‘trust’.

Quick thought:

- A simple website that converts address from and to emoticons would be a solution to the verbal communication problem (it basically delegates the problem to using an URL)

---

**MaverickChow** (2018-09-24):

Take note that the author tries to innovate the UI for older generations. ‘Momcode’ may be more practical to generations before us, but as younger generations come into the picture, such ‘momcode’ standard may not last. Besides, the older we get, the less likely for us to adapt to newer innovations to the extent that someone else need to go backward to accommodate us. Pattern recognition is an inherent self-evolving neural capability and need not be developed as of now by anyone except newborns. In my opinion, the identicons (thank you drhus for educating me on that, I had no idea what they are called before this) remain the most viable if we can find the solutions to scan them for both input and output purposes. So far I only see them being an output from a new address generation. If they can be scanned / analyzed as an input, then I think we can open up some possibilities to better UI/UX.

---

**jpitts** (2018-09-24):

The key is to understand the user, even if in a broad category such as “an elderly person”.

How would we do this? Well, as scientifically as possible. This means proposing a hypothesis, making sure the hypothesis can be disproven (Popper’s falsifiability), testing/validating the hypothesis, enabling peer review, enabling alternative hypotheses to be a part of the process.

What users actually need has to be established concretely, using an agreed-upon process, or we will imagine/speculate/guess, and end up with solutions that are not optimal.

---

**drhus** (2018-09-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/gluk64/48/11557_2.png) gluk64:

> since a BIP39 word has higher entropy, you only need 16 of them to describe the address (as opposed to 20 words from the PGP list).

I’m familiar with bip-39 seed phrase implementation for private key and derived addresses but not for public key, would you be so kind to refer me to a such implementation? a library that I could test to generate Bip39 mnemonic phrase of a wallet address.

![](https://ethresear.ch/user_avatar/ethresear.ch/cygnusfear/48/1139_2.png) Cygnusfear:

> The lab is great! Is there a repository where I could submit a PR / tweak the encoding?

sure [GitHub - drhus/MomCode: Test-Lab for Momcode, A Deterministic Human-friendly Visualization for Large Identifier (Wallet Shape Address)](https://github.com/drhus/Momcode)

[@Cygnusfear](/u/cygnusfear) do you mean by *a website to convert from and to emoticons*? an input (copy/past or with special keyboard) to decode the symbols back to hash address? It is something I was thinking about a lot, I don’t have an easy solution for copy/past but on the road-map a milestone for Momcode keyboard (16-32 symbols with 8 colors) which could be used on a website or integrated with Crypto Wallet (in a similar fashion to emoji keyboards), check out [Milestones - drhus/MomCode · GitHub](https://github.com/drhus/Momcode/milestones)

![](https://ethresear.ch/user_avatar/ethresear.ch/maverickchow/48/2858_2.png) MaverickChow:

> most viable if we can find the solutions to scan them for both input and output purposes. So far I only see them being an output from a new address generation. If they can be scanned / analyzed as an input, then I think we can open up some possibilities to better UI/UX.

You said it all ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

A Better UI/UX and Security! for 30-40 year we mainly used hashs for db/ssh/pgp and store it safely to be used once a while *copy/past*, Today with cryptocurrencies we’ve to transmit and use it in a daily base, not just me and you but people much less sensitive to all types of associated risk!

a deterministic (rule-based) visual linkage which serves in the capacity of identicon as distinguishable, +scannable and describable could replace both QR code and Identicon, and would provide a simpler and safer usage.

---

**gluk64** (2018-09-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/drhus/48/1798_2.png) drhus:

> I’m familiar with bip-39 seed phrase implementation for private key and derived addresses but not for public key, would you be so kind to refer me to a such implementation? a library that I could test to generate Bip39 mnemonic phrase of a wallet address.

I don’t know any implementation, but it’s easy to build one. What programming language do you use?

How it can work: you split the 160-bit address into 16 10-bit parts. Like PGP words, each part is appended with evenness bit (0 for even words in the phrase, 1 for odd ones). The resulting 11-bit number is the number of word in BIP39 list.

---

**kladkogex** (2018-09-25):

Good idea ))

I would use an adversarial neural network to generate a human face ))

---

**Cygnusfear** (2018-09-25):

One only needs to ask, Tenzorum released an easy way to associate an ENS subdomain to an address:

---

**drhus** (2018-09-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/gluk64/48/11557_2.png) gluk64:

> How it can work: you split the 160-bit address into 16 10-bit parts. Like PGP words, each part is appended with evenness bit (0 for even words in the phrase, 1 for odd ones). The resulting 11-bit number is the number of word in BIP39 list.

indeed, that works like a charm 16 words of already existing standard list multi-lang. a small online javascript gadget will definitely be useful, and the fact that it’s 16 words and Ethereum address has no checksum (but for case-sensitivity) we could add 4 bytes or 1 -2 words checksum later!

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> I would use an adversarial neural network to generate a human face ))

tell me more about that..

![](https://ethresear.ch/user_avatar/ethresear.ch/cygnusfear/48/1139_2.png) Cygnusfear:

> Tenzorum released an easy way to associate an ENS subdomain to an address:

isn’t just as ENS now subdomains of https://enslisting.com ?

---

**gluk64** (2018-09-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/drhus/48/1798_2.png) drhus:

> we could add 4 bytes or 1 -2 words checksum later

If you prefer a checksum, then I think evenness bits are not necessary, so we can keep 16 words length with a 16 bit checksum. I’m not sure even that is necessary for our use-case of phrase verification, it’s just a way to create some redundancy.

---

**MihailoBjelic** (2018-09-26):

I believe all/majority of wallets/dApps will use name systems (such as ENS) in the future. That’s what we’re all used to, so I guess that’s the best choice if we want mass adoption.

However, your idea is interesting and I guess it could be worth exploring (along with similar ideas) for some alternative use cases. For example, crypto community is very inclusive and open (one of the reasons I like it so much), so it would be awesome if we have good UX solutions in place for people with disabilities, too.  ![:blue_heart:](https://ethresear.ch/images/emoji/facebook_messenger/blue_heart.png?v=9)

---

**Cygnusfear** (2018-09-26):

Yes, it’s an easy way to get an ENS now subdomain. It will help solve the ‘over the phone’ issue and is easy to manually check for correctness. So this a great solution to many of the problems we associate with public keys.

Many people I know have an @gmail or @icloud email address and do not buy their own domain. So it is similar to the user experience they are familiar with.

---

**drhus** (2018-09-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/gluk64/48/11557_2.png) gluk64:

> If you prefer a checksum, then I think evenness bits are not necessary, so we can keep 16 words length with a 16 bit checksum. I’m not sure even that is necessary for our use-case of phrase verification, it’s just a way to create some redundancy.

Oh yeah, I forgot we’re using 2 lists pgp style for error redundancy, IMO a proper checksum is defiantly a better than 2x tables. and this application could work universally across crypto addresses most Hex or encoding of hex, we add then base58check >> hash140 and would instantly work for bitcoin.

This might be the safest way to transmit a wallet address over the phone today with 16 words +distinguishable +checksum!

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> so it would be awesome if we have good UX solutions in place for people with disabilities, too

Great idea, I looked up the subject there is 8% of men with color blindness!

I’ve just added a Dictionary that supports color-blindless, and it dosn’t look bad at all!

ex. random 0xbdd8fe2a864cfa165b1266649996e976dcc99483 >>

![6%20(5)](https://ethresear.ch/uploads/default/original/2X/0/0c3b60e031409c4269b9c074b0dbc6f1f6d50174.jpeg)

or square

[![6%20(6)](https://ethresear.ch/uploads/default/original/2X/8/89a99d6f6969e3b47729e348fc08ff0911202471.jpeg)6%20(6)195×209 18.7 KB](https://ethresear.ch/uploads/default/89a99d6f6969e3b47729e348fc08ff0911202471)

here is how the entire new dictionary looks for people with Deuteranomaly (which is the most common type ~5% of total men has it)

[![6%20(7)](https://ethresear.ch/uploads/default/original/2X/e/e5e3c768ae4cac28fe7d45fed74775f1ee81ba30.jpeg)6%20(7)431×476 89.6 KB](https://ethresear.ch/uploads/default/e5e3c768ae4cac28fe7d45fed74775f1ee81ba30)

[Momcode :: Deterministic Visual Identifier | Test Lab v0.6](https://momcode.io/lab/) >> list #225b


*(13 more replies not shown)*
